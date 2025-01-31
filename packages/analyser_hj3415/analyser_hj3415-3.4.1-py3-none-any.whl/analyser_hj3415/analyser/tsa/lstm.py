import os
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional, Tuple
import plotly.graph_objs as go
from plotly.offline import plot
import matplotlib.pyplot as plt  # Matplotlib 수동 임포트
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
from tensorflow.keras import Input # type: ignore
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from dataclasses import dataclass

from utils_hj3415 import tools, setup_logger
from db_hj3415 import myredis
from analyser_hj3415.analyser import MIs, tsa

mylogger = setup_logger(__name__,'WARNING')
expire_time = tools.to_int(os.getenv('DEFAULT_EXPIRE_TIME_H', 48)) * 3600


@dataclass
class LSTMData:
    """
    LSTM 모델에서 사용할 데이터를 저장하는 데이터 클래스.

    속성:
        ticker (str): 주식 티커(symbol).
        data_2d (np.ndarray): 원본 종가 데이터를 저장한 2차원 배열.
        train_size (int): 학습 데이터 크기.
        train_data_2d (np.ndarray): 학습 데이터 2차원 배열.
        test_data_2d (np.ndarray): 테스트 데이터 2차원 배열.
        X_train_3d (np.ndarray): 학습 데이터 3차원 배열.
        X_test_3d (np.ndarray): 테스트 데이터 3차원 배열.
        y_train_1d (np.ndarray): 학습 정답 데이터 1차원 배열.
        y_test_1d (np.ndarray): 테스트 정답 데이터 1차원 배열.
    """
    ticker: str

    data_2d: np.ndarray
    train_size: int
    train_data_2d: np.ndarray
    test_data_2d: np.ndarray

    X_train_3d: np.ndarray
    X_test_3d: np.ndarray
    y_train_1d: np.ndarray
    y_test_1d: np.ndarray


@dataclass
class LSTMGrade:
    """
    LSTM 모델 학습 결과를 평가하기 위한 데이터 클래스.

    속성:
        ticker (str): 주식 티커(symbol).
        train_mse (float): 학습 데이터에 대한 평균 제곱 오차(MSE).
        train_mae (float): 학습 데이터에 대한 평균 절대 오차(MAE).
        train_r2 (float): 학습 데이터에 대한 결정 계수(R²).
        test_mse (float): 테스트 데이터에 대한 평균 제곱 오차(MSE).
        test_mae (float): 테스트 데이터에 대한 평균 절대 오차(MAE).
        test_r2 (float): 테스트 데이터에 대한 결정 계수(R²).
    """
    ticker: str
    train_mse: float
    train_mae: float
    train_r2: float
    test_mse: float
    test_mae: float
    test_r2: float


class MyLSTM:
    """
    주가 데이터를 기반으로 LSTM 모델을 생성, 학습 및 예측하는 클래스.

    속성:
        future_days (int): 미래 예측할 일 수. 기본값은 30.
        scaler (MinMaxScaler): 데이터 정규화를 위한 MinMaxScaler.
        _ticker (str): 주식 티커(symbol).
        raw_data (pd.DataFrame): 원본 주가 데이터.
        lstm_data (LSTMData): LSTM 학습에 사용할 데이터.
    """
    # 미래 몇일을 예측할 것인가?
    future_days = 30

    def __init__(self, ticker: str):
        mylogger.info(f'set up ticker : {ticker}')
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self._ticker = ticker

        self.raw_data = pd.DataFrame()
        self.lstm_data = LSTMData(
                ticker=self.ticker,
                data_2d=np.array([]),
                train_size=0,
                train_data_2d=np.array([]),
                test_data_2d=np.array([]),
                X_train_3d=np.array([]),
                X_test_3d=np.array([]),
                y_train_1d=np.array([]),
                y_test_1d=np.array([]),
            )

    @property
    def ticker(self) -> str:
        return self._ticker

    @ticker.setter
    def ticker(self, ticker: str):
        mylogger.info(f'change ticker : {self.ticker} -> {ticker}')
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self._ticker = ticker

        self.raw_data = pd.DataFrame()
        self.lstm_data = LSTMData(
            ticker=self.ticker,
            data_2d=np.array([]),
            train_size=0,
            train_data_2d=np.array([]),
            test_data_2d=np.array([]),
            X_train_3d=np.array([]),
            X_test_3d=np.array([]),
            y_train_1d=np.array([]),
            y_test_1d=np.array([]),
        )

    def initializing(self):
        """
        LSTM 모델 학습을 위한 데이터를 준비합니다.

        Yahoo Finance에서 주가 데이터를 가져와 정규화, 학습 및 테스트 데이터로 분리,
        LSTM 모델 입력 형식으로 변환합니다. `get_final_predictions` 메서드 실행 전에
        반드시 호출해야 합니다.
        """
        def get_raw_data() -> pd.DataFrame:
            """
            야후에서 해당 종목의 4년간 주가 raw data를 받아온다.
            :return:
            """
            # 오늘 날짜 가져오기
            today = datetime.today()

            # 4년 전 날짜 계산 (4년 = 365일 * 4)
            four_years_ago = today - timedelta(days=365 * 4)
            mylogger.info(
                f"Get raw data from yfinance - start: {four_years_ago.strftime('%Y-%m-%d')}, end: {today.strftime('%Y-%m-%d')}")

            df = yf.download(
                tickers=self.ticker,
                start=four_years_ago.strftime('%Y-%m-%d'),
                end=today.strftime('%Y-%m-%d')
            )
            df.index = df.index.tz_localize(None)
            mylogger.debug(df)
            return df

        def preprocessing_for_lstm() -> LSTMData:
            """
            lstm이 사용할 수 있도록 데이터 준비(정규화 및 8:2 훈련데이터 검증데이터 분리 및 차원변환)
            :return:
            """
            mylogger.info("lstm이 사용할 수 있도록 데이터 준비(정규화 및 8:2 훈련데이터 검증데이터 분리 및 차원변환)")
            # 필요한 열만 선택 (종가만 사용) - 2차웜 배열로 변환
            data_2d = self.raw_data['Close'].values.reshape(-1, 1)
            mylogger.debug(f"종가데이터 2차원베열값[:5] : {data_2d[:5]}")

            # 데이터 정규화 (0과 1 사이로 스케일링)
            scaled_data_2d = self.scaler.fit_transform(data_2d)

            # 학습 데이터 생성
            # 주가 데이터를 80%는 학습용, 20%는 테스트용으로 분리하는 코드
            train_size = int(len(scaled_data_2d) * 0.8)
            train_data_2d = scaled_data_2d[:train_size]
            test_data_2d = scaled_data_2d[train_size:]
            mylogger.info(f'총 {len(data_2d)}개 데이터, train size : {train_size}')

            # 학습 데이터에 대한 입력(X)과 정답(y)를 생성
            def create_dataset(data, time_step=60):
                X, y = [], []
                for i in range(len(data) - time_step):
                    X.append(data[i:i + time_step, 0])
                    y.append(data[i + time_step, 0])
                return np.array(X), np.array(y)

            X_train, y_train_1d = create_dataset(train_data_2d)
            X_test, y_test_1d = create_dataset(test_data_2d)
            mylogger.debug(f"훈련데이터 shape (입력, 정답) / {X_train.shape}")
            mylogger.debug(f"테스트데이터 shape (입력, 정답) / {X_test.shape}")

            try:
                mylogger.debug("2차원 데이터를 3차원으로 변환합니다.")
                # LSTM 모델 입력을 위해 데이터를 3차원으로 변환
                X_train_3d = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
                X_test_3d = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
            except IndexError:
                return LSTMData(
                    ticker=self.ticker,
                    data_2d=np.array([]),
                    train_size=0,
                    train_data_2d=np.array([]),
                    test_data_2d=np.array([]),
                    X_train_3d=np.array([]),
                    X_test_3d=np.array([]),
                    y_train_1d=np.array([]),
                    y_test_1d=np.array([]),
                )

            mylogger.debug(
                f'차원 - X_train_3d : {X_train_3d.ndim}, X_test_3d : {X_test_3d.ndim}, y_train : {y_train_1d.ndim}, y_test : {y_test_1d.ndim}')
            mylogger.debug(
                f'len - X_train_3d : {len(X_train_3d)}, X_test_3d : {len(X_test_3d)}, y_train : {len(y_train_1d)}, y_test : {len(y_test_1d)}')

            return LSTMData(
                ticker=self.ticker,
                data_2d=data_2d,
                train_size=train_size,
                train_data_2d=train_data_2d,
                test_data_2d=test_data_2d,
                X_train_3d=X_train_3d,
                X_test_3d=X_test_3d,
                y_train_1d=y_train_1d,
                y_test_1d=y_test_1d,
            )

        self.scaler = MinMaxScaler(feature_range=(0, 1))

        self.raw_data = get_raw_data()
        self.lstm_data = preprocessing_for_lstm()

    def ensemble_training(self, num) -> Tuple[list, LSTMGrade]:
        """
        앙상블 LSTM 모델을 훈련하고, 예측 결과를 생성 및 평가합니다.

        매개변수:
            num (int): 앙상블에 포함할 모델의 수.

        반환값:
            Tuple[list, LSTMGrade]: 미래 예측 값 리스트와 학습 결과 평가 데이터.

        예외:
            IndexError: 모델 훈련을 위한 데이터가 부족한 경우 경고 로그를 출력합니다.
        """
        def model_training() -> Sequential:
            # LSTM 모델 생성 - 유닛과 드롭아웃의 수는 테스트로 최적화 됨.
            model = Sequential()
            mylogger.debug(f"훈련 데이터 shape - {self.lstm_data.X_train_3d.shape}")
            try:
                # Input(shape=(50, 1))는 50개의 타임스텝을 가지는 입력 데이터를 처리하며, 각 타임스텝에 1개의 특성이 있다는 것을 의미
                model.add(Input(shape=(self.lstm_data.X_train_3d.shape[1], 1)))  # 입력 레이어에 명시적으로 Input을 사용
            except IndexError:
                mylogger.error("모델 트레이닝을 위한 자료가 부족합니다.")
                return model

            model.add(LSTM(units=150, return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(units=75, return_sequences=False))
            model.add(Dropout(0.2))
            model.add(Dense(units=25))
            model.add(Dropout(0.3))
            model.add(Dense(units=1))

            # 모델 요약 출력
            model.summary()

            # 모델 컴파일 및 학습
            model.compile(optimizer='adam', loss='mean_squared_error')

            # 조기 종료 설정
            early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

            # 모델 학습 - 과적합 방지위한 조기종료 세팅
            model.fit(self.lstm_data.X_train_3d, self.lstm_data.y_train_1d,
                      epochs=75, batch_size=32, validation_data=(self.lstm_data.X_test_3d, self.lstm_data.y_test_1d),
                      callbacks=[early_stopping])
            return model

        def prediction(model_in: Sequential, data: np.ndarray) -> np.ndarray:
            """
            훈련될 모델을 통해 예측을 시행하여 정규화를 복원하고 결과 반환한다.
            :param model_in:
            :param data:
            :return:
            """
            predictions_2d = model_in.predict(data)
            predictions_scaled_2d = self.scaler.inverse_transform(predictions_2d)  # 스케일링 복원
            mylogger.info(
                f'predictions_scaled_2d : ndim - {predictions_scaled_2d.ndim} len - {len(predictions_scaled_2d)}')  # numpy.ndarray 타입
            mylogger.debug(f'predictions_scaled_2d[:5] :{predictions_scaled_2d[:5]}')
            return predictions_scaled_2d

        def grading(train_predictions: list, test_predictions: list) -> LSTMGrade:
            """
            딥러닝 결과를 분석하기 위한 함수
            :param train_predictions:
            :param test_predictions:
            :return:
            """
            if len(train_predictions) == 0 or len(test_predictions) == 0:
                mylogger.warning("딥러닝 결과가 없어서 LSTMGrade 데이터를 비워서 반환합니다.")
                return LSTMGrade(
                    ticker=self.ticker,
                    train_mse=float('nan'),
                    train_mae=float('nan'),
                    train_r2=float('nan'),
                    test_mse=float('nan'),
                    test_mae=float('nan'),
                    test_r2=float('nan'),
                )

            # 예측값을 평균내서 최종 예측값 도출
            mean_train_prediction_2d = np.mean(train_predictions, axis=0)
            mean_test_predictions_2d = np.mean(test_predictions, axis=0)

            # y값(정답) 정규화 해제
            y_train_scaled_2d = self.scaler.inverse_transform(self.lstm_data.y_train_1d.reshape(-1, 1))
            y_test_scaled_2d = self.scaler.inverse_transform(self.lstm_data.y_test_1d.reshape(-1, 1))

            # 평가 지표 계산
            train_mse = mean_squared_error(y_train_scaled_2d, mean_train_prediction_2d)
            train_mae = mean_absolute_error(y_train_scaled_2d, mean_train_prediction_2d)
            train_r2 = r2_score(y_train_scaled_2d, mean_train_prediction_2d)

            test_mse = mean_squared_error(y_test_scaled_2d, mean_test_predictions_2d)
            test_mae = mean_absolute_error(y_test_scaled_2d, mean_test_predictions_2d)
            test_r2 = r2_score(y_test_scaled_2d, mean_test_predictions_2d)

            # 평가 결과 출력
            print("Training Data:")
            print(f"Train MSE: {train_mse}, Train MAE: {train_mae}, Train R²: {train_r2}")
            print("\nTesting Data:")
            print(f"Test MSE: {test_mse}, Test MAE: {test_mae}, Test R²: {test_r2}")
            # mse, mae는 작을수록 좋으며 R^2은 0-1 사이값 1에 가까울수록 정확함
            # 과적합에 대한 평가는 train 과 test를 비교하여 test가 너무 않좋으면 과적합 의심.

            return LSTMGrade(
                ticker=self.ticker,
                train_mse=train_mse,
                train_mae=train_mae,
                train_r2=train_r2,
                test_mse=test_mse,
                test_mae=test_mae,
                test_r2=test_r2,
            )

        ensemble_train_predictions_2d = []
        ensemble_test_predictions_2d = []
        ensemble_future_predictions_2d = []

        for i in range(num):
            print(f"Training model {i + 1}/{num}...")
            model = model_training()

            if len(model.layers) == 0:
                mylogger.warning("이 모델은 빈 Sequential() 입니다.")
                return [], grading([],[])
            else:
                mylogger.info("레이어가 있는 모델입니다.")

                # 훈련 데이터 예측
                train_predictions_scaled_2d = prediction(model, self.lstm_data.X_train_3d)
                ensemble_train_predictions_2d.append(train_predictions_scaled_2d)

                # 테스트 데이터 예측
                test_predictions_scaled_2d = prediction(model, self.lstm_data.X_test_3d)
                ensemble_test_predictions_2d.append(test_predictions_scaled_2d)

                # 8. 미래 30일 예측
                # 마지막 60일간의 데이터를 기반으로 미래 30일을 예측

                last_60_days_2d = self.lstm_data.test_data_2d[-60:]
                last_60_days_3d = last_60_days_2d.reshape(1, -1, 1)

                future_predictions = []
                for _ in range(self.future_days):
                    predicted_price_2d = model.predict(last_60_days_3d)
                    future_predictions.append(predicted_price_2d[0][0])

                    # 예측값을 다시 입력으로 사용하여 새로운 예측을 만듦
                    predicted_price_reshaped = np.reshape(predicted_price_2d, (1, 1, 1))  # 3D 배열로 변환
                    last_60_days_3d = np.append(last_60_days_3d[:, 1:, :], predicted_price_reshaped, axis=1)

                # 예측된 주가를 다시 스케일링 복원
                future_predictions_2d = np.array(future_predictions).reshape(-1, 1)
                future_predictions_scaled_2d = self.scaler.inverse_transform(future_predictions_2d)
                ensemble_future_predictions_2d.append(future_predictions_scaled_2d)

        lstm_grade = grading(ensemble_train_predictions_2d, ensemble_test_predictions_2d)

        return ensemble_future_predictions_2d, lstm_grade

    def get_final_predictions(self, refresh: bool, num=5) -> Tuple[dict, LSTMGrade]:
        """
        LSTM 모델을 사용하여 미래 주가를 예측하고 평가 데이터를 반환합니다.

        매개변수:
            refresh (bool): 데이터 새로고침 여부.
            num (int): 앙상블 모델의 수. 기본값은 5.

        반환값:
            Tuple[dict, LSTMGrade]: 날짜별 예측 주가와 모델 평가 데이터.

        로그:
            - 캐시 데이터 검색 및 새 데이터 생성 과정 출력.
            - 예측 값의 증가 추세를 분석하여 캐시에 저장.
        """
        print("**** Start get_final_predictions... ****")
        redis_name = f'{self.ticker}_mylstm_predictions'

        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def caching_is_lstm_up(future_data_in: dict):
            """
            날짜(str)를 키, 수치(float)를 값으로 갖는 딕셔너리를
            선형회귀분석(최소제곱법)을 통해 추세가 우상향인지 판별.

            Returns:
                bool: 기울기가 양수이면 True, 아니면 False
            """

            print("**** Caching is_lstm_up ... ****")
            redis_name = f'{self.ticker}_is_lstm_up'
            print(f"redisname: '{redis_name}' / expire_time : {expire_time / 3600}h")

            is_up = tsa.common.is_up_by_OLS(future_data_in)
            mylogger.debug(f"is_up: {is_up}")
            myredis.Base.set_value(redis_name, is_up, expire_time)

        def fetch_final_predictions(num_in) -> tuple:
            """
            앙상블법으로 딥러닝을 모델을 반복해서 평균을 내서 미래를 예측한다. 평가는 래시스 캐시로 반환하기 어려워 일단 디버그 용도로만 사용하기로
            :param num_in:
            :return:
            """
            def make_future_data_dict(future_predictions) -> dict:
                # 시각화를 위한 준비 - 날짜 생성 (미래 예측 날짜), 미래예측값 평균
                mylogger.debug(self.raw_data)
                last_date = self.raw_data.index[-1]
                mylogger.debug(f'last_date : {last_date}')
                future_dates = pd.date_range(last_date, periods=self.future_days + 1).tolist()[1:]
                mylogger.debug(f'future_dates : {future_dates}')
                final_future_predictions = np.mean(future_predictions, axis=0).tolist()
                mylogger.debug(f'final_future_predictions(예측주가 리스트) : {final_future_predictions}')

                assert len(future_dates) == len(
                    final_future_predictions), "future_dates 와 final_future_predictions 개수가 일치하지 않습니다."

                data = {}
                for i in range(len(future_dates)):
                    data[future_dates[i].strftime("%Y-%m-%d")] = final_future_predictions[i][0]
                return data

            self.initializing()
            # 앙상블 트레이닝 시행
            future_predictions_2d, lstm_grade = self.ensemble_training(num=num_in)
            mylogger.debug(f'future_predictions_2d[:5] : {future_predictions_2d[:5]}')
            mylogger.debug(f'lstm grade(학습결과평과) : {lstm_grade}')
            if len(future_predictions_2d) == 0:
                return {}, lstm_grade

            # {날짜(유닉스타임): 예측주가} 형식으로 딕서너리로 제작
            future_data = make_future_data_dict(future_predictions_2d)
            mylogger.debug(f'future_data : {future_data}')

            return future_data, lstm_grade

        future_data, lstm_grade = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_final_predictions, num, timer=expire_time)

        # 증가 추세인지 아닌지 레디스 캐시에 저장
        caching_is_lstm_up(future_data)

        return future_data, lstm_grade

    def export(self, refresh=False, to="html", num=5) -> Optional[str]:
        """
        과거 및 예측된 주가 데이터를 기반으로 시각화를 생성하고 저장합니다.

        매개변수:
            refresh (bool): 데이터 새로고침 여부. 기본값은 False.
            to (str): 그래프 출력 형식 ('hrml', 'png', 'file'). 기본값은 'html'.
            num (int): 예측 모델 수. 기본값은 5.

        반환값:
            Optional[str]: HTML 형식의 그래프 문자열(`to='html'`인 경우).
            None: PNG 또는 HTML 파일로 저장된 경우.

        예외:
            Exception: 잘못된 `to` 값이 주어졌을 때 발생.
        """
        def prepare_past_data(past_days) -> tuple:
            # 데이터 준비
            raw_data_copied = self.raw_data.reset_index()
            data = raw_data_copied[['Date', 'Close']][-past_days:].reset_index(drop=True)

            # 'Date'와 'Close' 열 추출
            past_dates = pd.to_datetime(data['Date'])
            past_prices = data['Close']

            # 'past_prices'가 Series인지 확인
            if isinstance(past_prices, pd.DataFrame):
                past_prices = past_prices.squeeze()

            # 'Close' 열의 데이터 타입 변경
            past_prices = past_prices.astype(float)
            return past_dates, past_prices

        def prepare_future_data(refresh_in, num_in) -> tuple:
            future_data, lstm_grade = self.get_final_predictions(refresh=refresh_in, num=num_in)

            # 예측 데이터 준비
            future_dates = pd.to_datetime(list(future_data.keys()))

            future_prices = pd.Series(future_data.values(), index=range(len(future_data.values()))).astype(float)
            return future_dates, future_prices

        self.initializing()
        past_dates, past_prices = prepare_past_data(past_days=120)
        future_dates, future_prices = prepare_future_data(refresh_in=refresh, num_in=num)

        # 그래프 생성
        fig = go.Figure()

        # 실제 데이터 추가
        fig.add_trace(go.Scatter(
            x=past_dates,
            y=past_prices,
            mode='markers',
            name='실제주가'
        ))

        # 예측 데이터 추가
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_prices,
            mode='lines+markers',
            name='예측치(30일)'
        ))

        # 레이아웃 업데이트
        fig.update_layout(
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis=dict(
                tickformat='%Y/%m',
            ),
            yaxis=dict(
                tickformat=".0f",
            ),
            showlegend=True,
        )

        mylogger.debug(f"past_dates({len(past_dates)}) - {past_dates}")
        mylogger.debug(f"past_prices({len(past_prices)} - {past_prices}")
        mylogger.debug(f"future_dates({len(future_dates)}) - {future_dates}")
        mylogger.debug(f"future_prices({len(future_prices)}) - {future_prices}")

        fig.update_layout(
            # title=f'{self.code} {self.name} 주가 예측 그래프(prophet)',
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis=dict(
                tickformat='%Y/%m',  # X축을 '연/월' 형식으로 표시
            ),
            yaxis=dict(
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
            fig.write_image(f"myLSTM_{self.ticker}.png")
            return None
        elif to == 'file':
            # 그래프를 HTML로 저장
            plot(fig, filename=f'myLSTM_{self.ticker}.html', auto_open=False)
            return None
        else:
            Exception("to 인자가 맞지 않습니다.")

    def visualization(self, refresh=True):
        """
        실제 주가와 예측 주가를 시각화합니다.

        매개변수:
            refresh (bool): 예측 데이터를 새로고침할지 여부. 기본값은 True.

        반환값:
            None: 시각화를 출력합니다.
        """
        self.initializing()
        future_data, _ = self.get_final_predictions(refresh=refresh)
        mylogger.debug(f'future_data : {future_data}')
        future_dates = pd.to_datetime(list(future_data.keys()))
        mylogger.debug(f'future_dates : {future_dates}')
        future_prices = pd.Series(future_data.values(), index=range(len(future_data.values()))).astype(float)
        mylogger.debug(f'future_prices : {future_prices}')

        # 시각화1
        plt.figure(figsize=(10, 6))

        # 실제 주가
        plt.plot(self.raw_data.index, self.raw_data['Close'], label='Actual Price')

        # 미래 주가 예측
        plt.plot(future_dates, future_prices, label='Future Predicted Price', linestyle='--')

        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.title(f'{self.ticker} Stock Price Prediction with LSTM')
        plt.show()

        """# 시각화2
        plt.figure(figsize=(10, 6))
        plt.plot(self.raw_data.index[self.lstm_data.train_size + 60:], self.lstm_data.data_2d[self.lstm_data.train_size + 60:], label='Actual Price')
        plt.plot(self.raw_data.index[self.lstm_data.train_size + 60:], lstm_grade.mean_test_predictions_2d, label='Predicted Price')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.title('Stock Price Prediction with LSTM Ensemble')
        plt.show()"""

    def is_lstm_up(self) -> bool:
        """
        LSTM 모델의 추세가 상승인지 여부를 확인합니다.

        반환값:
            bool: 추세가 상승 상태(True) 또는 추세가 하락 상태(False).
        """
        return myredis.Base.get_value(f'{self.ticker}_is_lstm_up')


class CorpLSTM(MyLSTM):
    """
    특정 기업 코드를 기반으로 주가를 예측하는 LSTM 클래스.

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


class MILSTM(MyLSTM):
    """
    특정 MI 타입에 따라 주가를 예측하는 LSTM 클래스.

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

