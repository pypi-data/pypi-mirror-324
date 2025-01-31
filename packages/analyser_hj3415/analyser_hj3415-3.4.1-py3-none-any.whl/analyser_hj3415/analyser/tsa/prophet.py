from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import yfinance as yf
import pandas as pd
from prophet import Prophet
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt  # Matplotlib 수동 임포트
import plotly.graph_objs as go
from plotly.offline import plot
from dataclasses import dataclass
import os

from utils_hj3415 import tools, setup_logger
from db_hj3415 import myredis

from analyser_hj3415.analyser import eval, MIs, tsa


mylogger = setup_logger(__name__,'WARNING')
expire_time = tools.to_int(os.getenv('DEFAULT_EXPIRE_TIME_H', 48)) * 3600


@dataclass
class ProphetData:
    ticker: str

    date: datetime.date
    price: float
    yhat: float
    yhat_upper: float
    yhat_lower: float
    forecast_data: List[dict]

    trading_action: str = ''
    score: int = None


class MyProphet:
    def __init__(self, ticker: str):
        mylogger.info(f'set up ticker : {ticker}')
        self.scaler = StandardScaler()
        self.model = Prophet()
        self._ticker = ticker

        self.raw_data = pd.DataFrame()
        self.df_real = pd.DataFrame()
        self.df_forecast = pd.DataFrame()

    @property
    def ticker(self) -> str:
        """
        현재 설정된 티커를 반환합니다.

        반환값:
            str: 현재 티커 값.
        """
        return self._ticker

    @ticker.setter
    def ticker(self, ticker: str):
        """
        티커 값을 변경하고 관련 데이터를 초기화합니다.

        매개변수:
            ticker (str): 새로 설정할 티커 값.
        """
        mylogger.info(f'change ticker : {self.ticker} -> {ticker}')
        self.scaler = StandardScaler()
        self.model = Prophet()
        self._ticker = ticker

        self.raw_data = pd.DataFrame()
        self.df_real = pd.DataFrame()
        self.df_forecast = pd.DataFrame()

    def initializing(self):
        """
        Prophet 모델 사용을 위한 데이터를 초기화합니다.

        - Yahoo Finance에서 데이터를 가져옵니다.
        - 데이터를 Prophet 형식에 맞게 전처리합니다.
        - Prophet 모델을 사용하여 예측 데이터를 생성합니다.
        """
        def get_raw_data() -> pd.DataFrame:
            """
            Yahoo Finance에서 4년간의 주가 데이터를 가져옵니다.

            반환값:
                pd.DataFrame: 가져온 주가 데이터프레임.
            """
            # 오늘 날짜 가져오기
            today = datetime.today()

            # 4년 전 날짜 계산 (4년 = 365일 * 4)
            four_years_ago = today - timedelta(days=365 * 4)

            return yf.download(
                tickers=self.ticker,
                start=four_years_ago.strftime('%Y-%m-%d'),
                end=today.strftime('%Y-%m-%d')
            )

        def preprocessing_for_prophet() -> pd.DataFrame:
            """
            Prophet 모델에서 사용할 수 있도록 데이터를 준비합니다.

            - 'Close'와 'Volume' 열을 사용.
            - 날짜를 'ds', 종가를 'y', 거래량을 'volume'으로 변경.
            - 거래량 데이터를 정규화하여 'volume_scaled' 열 추가.

            반환값:
                pd.DataFrame: Prophet 모델 입력 형식에 맞게 처리된 데이터프레임.
            """
            df = self.raw_data[['Close', 'Volume']].reset_index()
            df.columns = ['ds', 'y', 'volume']  # Prophet의 형식에 맞게 열 이름 변경

            # ds 열에서 타임존 제거
            df['ds'] = df['ds'].dt.tz_localize(None)

            # 추가 변수를 정규화
            df['volume_scaled'] = self.scaler.fit_transform(df[['volume']])
            mylogger.debug('_preprocessing_for_prophet')
            mylogger.debug(df)
            return df

        def make_forecast() -> pd.DataFrame:
            """
            Prophet 모델을 사용하여 향후 180일간 주가를 예측합니다.

            - 거래량 데이터('volume_scaled')를 추가 변수로 사용.
            - 예측 결과를 데이터프레임으로 반환.

            반환값:
                pd.DataFrame: 예측 결과를 포함한 데이터프레임.
            """
            # 정규화된 'volume_scaled' 변수를 외부 변수로 추가
            self.model.add_regressor('volume_scaled')

            self.model.fit(self.df_real)

            # 향후 180일 동안의 주가 예측
            future = self.model.make_future_dataframe(periods=180)
            mylogger.debug('_make_forecast_future')
            mylogger.debug(future)

            # 미래 데이터에 거래량 추가 (평균 거래량을 사용해 정규화)
            future_volume = pd.DataFrame({'volume': [self.raw_data['Volume'].mean()] * len(future)})
            future['volume_scaled'] = self.scaler.transform(future_volume[['volume']])

            forecast = self.model.predict(future)
            mylogger.debug('_make_forecast')
            mylogger.debug(forecast)
            return forecast

        print("Initializing data for MyProphet")

        self.scaler = StandardScaler()
        self.model = Prophet()

        self.raw_data = get_raw_data()
        self.df_real = preprocessing_for_prophet()
        self.df_forecast = make_forecast()

    def generate_data(self, refresh: bool) -> ProphetData:
        """
        ProphetData 객체를 생성하거나 캐시된 데이터를 반환합니다.

        매개변수:
            refresh (bool): 데이터를 새로 생성할지 여부.

        반환값:
            ProphetData: 생성된 ProphetData 객체.
        """
        print("**** Start generate_data... ****")
        redis_name = f'{self.ticker}_myprophet_data'

        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time / 3600}h")

        def fetch_generate_prophet_data() -> ProphetData:
            def scoring(price: float, yhat_lower: float, yhat_upper: float, method: str = 'sigmoid') -> Tuple[str, int]:
                """
                주어진 가격과 임계값을 기준으로 매매 행동('buy', 'sell', 'hold')과 점수를 결정합니다.

                매개변수:
                    price (float): 자산의 현재 가격.
                    yhat_lower (float): 가격 예측의 하한 임계값.
                    yhat_upper (float): 가격 예측의 상한 임계값.
                    method (str, optional): 점수를 계산하는 방법 ('sigmoid' 또는 'log'). 기본값은 'sigmoid'.

                반환값:
                    Tuple[str, int]: 매매 행동('buy', 'sell', 'hold')과 관련 점수로 이루어진 튜플.

                예외:
                    ValueError: 지원되지 않는 점수 계산 방법이 제공된 경우 발생.
                """

                def calculate_score(deviation: float, method_in: str) -> int:
                    if method_in == 'sigmoid':
                        return tools.to_int(eval.Tools.sigmoid_score(deviation))
                    elif method_in == 'log':
                        return tools.to_int(eval.Tools.log_score(deviation))
                    else:
                        raise ValueError(f"Unsupported scoring method: {method}")

                buying_deviation = eval.Tools.cal_deviation(price, yhat_lower)
                buying_score = calculate_score(buying_deviation, method)
                if price >= yhat_lower:
                    buying_score = -buying_score

                selling_deviation = eval.Tools.cal_deviation(price, yhat_upper)
                selling_score = calculate_score(selling_deviation, method)
                if price <= yhat_upper:
                    selling_score = -selling_score

                if buying_score > 0:
                    return 'buy', buying_score
                elif selling_score > 0:
                    return 'sell', selling_score
                else:
                    return 'hold', 0

            self.initializing()
            latest_row = self.df_real.iloc[-1]
            latest_yhat = \
            self.df_forecast.loc[self.df_forecast['ds'] == latest_row['ds'], ['ds', 'yhat_lower', 'yhat_upper', 'yhat']].iloc[
                0].to_dict()

            data = ProphetData(
                ticker=self.ticker,
                date=latest_row['ds'].date(),
                price=latest_row['y'],
                yhat=latest_yhat['yhat'],
                yhat_lower=latest_yhat['yhat_lower'],
                yhat_upper=latest_yhat['yhat_upper'],
                forecast_data=self.df_forecast.to_dict(orient='records'),
            )

            data.trading_action, data.score = scoring(data.price, data.yhat_lower, data.yhat_upper)
            return data


        prophet_data = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_generate_prophet_data, timer=expire_time)

        return prophet_data

    def visualization(self):
        """
        Prophet 모델의 예측 결과를 시각화합니다.

        - Matplotlib를 사용하여 예측 결과 및 추세/계절성을 그래프로 출력.
        """
        self.initializing()
        # 예측 결과 출력
        print(self.df_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        # 예측 결과 시각화 (Matplotlib 사용)
        fig = self.model.plot(self.df_forecast)
        # 추세 및 계절성 시각화
        fig2 = self.model.plot_components(self.df_forecast)
        plt.show()  # 시각화 창 띄우기

    def export(self, to="html") -> Optional[str]:
        """
        예측 결과를 시각화하여 다양한 형식으로 내보냅니다.

        매개변수:
            refresh (bool): 데이터를 새로 생성할지 여부.
            to (str): 내보낼 형식 ('html', 'png', 'file').

        반환값:
            Optional[str]: HTML 문자열로 반환하거나 PNG/HTML 파일로 저장합니다.

        예외:
            Exception: 지원되지 않는 형식의 경우 예외 발생.
        """
        self.initializing()
        # Plotly를 사용한 시각화
        fig = go.Figure()

        # 실제 데이터
        fig.add_trace(go.Scatter(x=self.df_real['ds'], y=self.df_real['y'], mode='markers', name='실제주가'))
        # 예측 데이터
        fig.add_trace(go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat'], mode='lines', name='예측치'))

        # 상한/하한 구간
        fig.add_trace(
            go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat_upper'], fill=None, mode='lines', name='상한'))
        fig.add_trace(
            go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat_lower'], fill='tonexty', mode='lines', name='하한'))

        fig.update_layout(
            # title=f'{self.code} {self.name} 주가 예측 그래프(prophet)',
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis = dict(
                tickformat='%Y/%m',  # X축을 '연/월' 형식으로 표시
            ),
            yaxis = dict(
                tickformat=".0f",  # 소수점 없이 원래 숫자 표시
            ),
            showlegend=False,
        )

        if to == 'html':
            # 그래프 HTML로 변환 (string 형식으로 저장)
            graph_html = plot(fig, output_type='div')
            return graph_html
        elif to == 'png':
            # 그래프를 PNG 파일로 저장
            fig.write_image(f"myprophet_{self.ticker}.png")
            return None
        elif to == 'file':
            # 그래프를 HTML 파일로 저장
            plot(fig, filename=f'myprophet_{self.ticker}.html', auto_open=False)
            return None
        else:
            Exception("to 인자가 맞지 않습니다.")

    def is_prophet_up(self, refresh: bool) -> bool:
        """
        Prophet 예측이 상승 추세인지 여부를 확인합니다.

        매개변수:
            refresh (bool): 데이터를 새로 생성할지 여부.

        반환값:
            bool: 상승 추세 여부.
        """
        print("**** Caching is_prophet_up ... ****")
        redis_name = f'{self.ticker}_is_prophet_up'
        print(f"redisname: '{redis_name}' / expire_time : {expire_time / 3600}h")

        def fetch_is_prophet_up():
            self.initializing()
            yhat_dict = self.df_forecast.set_index('ds')['yhat'].to_dict()
            return tsa.common.is_up_by_OLS(yhat_dict)

        return myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_is_prophet_up, timer=expire_time)

    @staticmethod
    def is_valid_date(date_string):
        """
        주어진 문자열이 'YYYY-MM-DD' 형식의 유효한 날짜인지 확인합니다.

        매개변수:
            date_string (str): 확인할 날짜 문자열.

        반환값:
            bool: 유효한 날짜 형식이면 True, 그렇지 않으면 False.
        """
        try:
            # %Y-%m-%d 형식으로 문자열을 datetime 객체로 변환 시도
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            # 변환이 실패하면 ValueError가 발생, 형식이 맞지 않음
            return False



class CorpProphet(MyProphet):
    """
    기업 코드를 기반으로 주가를 예측하는 Prophet 모델 클래스.

    속성:
        code (str): 기업 코드.
        name (str): 기업명.
    """
    def __init__(self, code: str):
        assert tools.is_6digit(code), f'Invalid value : {code}'
        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        super().__init__(ticker=self.code + '.KS')

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert tools.is_6digit(code), f'Invalid value : {code}'
        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        self.ticker = self.code + '.KS'


class MIProphet(MyProphet):
    """
    특정 MI(Market Indicator) 타입에 따라 주가를 예측하는 Prophet 모델 클래스.

    속성:
        mi_type (str): MI 타입.
    """
    def __init__(self, mi_type: str):
        assert mi_type in MIs._fields, f"Invalid MI type ({MIs._fields})"
        self._mi_type = mi_type
        super().__init__(ticker=getattr(MIs, mi_type))

    @property
    def mi_type(self) -> str:
        return self._mi_type

    @mi_type.setter
    def mi_type(self, mi_type: str):
        assert mi_type in MIs._fields, f"Invalid MI type ({MIs._fields})"
        self._mi_type = mi_type
        self.ticker = getattr(MIs, mi_type)
