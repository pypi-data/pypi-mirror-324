import os
from collections import OrderedDict
from typing import Union
from dataclasses import dataclass

from db_hj3415 import myredis
from utils_hj3415 import tools, setup_logger

from analyser_hj3415.analyser import tsa, eval, MIs

mylogger = setup_logger(__name__,'WARNING')
expire_time = tools.to_int(os.getenv('DEFAULT_EXPIRE_TIME_H', 48)) * 3600

@dataclass
class MICompileData:
    """
    MI(Market Index) 데이터를 컴파일하여 저장하는 데이터 클래스.

    속성:
        mi_type (str): 시장 지수 유형.
        prophet_data (tsa.ProphetData): Prophet 예측 데이터.
        lstm_grade (tsa.LSTMGrade): LSTM 등급 데이터.
        is_lstm_up (bool): LSTM 상승 여부.
        is_prophet_up (bool): Prophet 상승 여부.
        lstm_html (str): LSTM 시각화 HTML.
        prophet_html (str): Prophet 시각화 HTML.
    """
    mi_type: str

    prophet_data: tsa.ProphetData
    lstm_grade: tsa.LSTMGrade

    is_lstm_up: bool = False
    is_prophet_up: bool = False

    lstm_html: str = ''
    prophet_html: str = ''


class MICompile:
    """
    MI(Market Index) 데이터를 컴파일하는 클래스.

    메서드:
        get(refresh=False) -> MICompileData:
            MI 데이터를 컴파일하거나 캐시에서 가져옵니다.

        analyser_lstm_all_mi(refresh: bool):
            모든 MI에 대해 LSTM 예측 및 초기화 수행.
    """
    def __init__(self, mi_type: str):
        """
        MICompile 객체를 초기화합니다.

        매개변수:
            mi_type (str): 시장 지수 유형.
        """
        assert mi_type in MIs._fields, f"Invalid MI type ({MIs._fields})"
        self._mi_type = mi_type

    @property
    def mi_type(self) -> str:
        """
        MI 유형을 반환합니다.

        반환값:
            str: MI 유형.
        """
        return self._mi_type

    @mi_type.setter
    def mi_type(self, mi_type: str):
        """
        MI 유형을 변경합니다.

        매개변수:
            mi_type (str): 새로 설정할 MI 유형.
        """
        assert mi_type in MIs._fields, f"Invalid MI type ({MIs._fields})"
        self._mi_type = mi_type

    def get(self, refresh=False) -> MICompileData:
        """
        MI 데이터를 컴파일하거나 캐시에서 가져옵니다.

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.

        반환값:
            MICompileData: 컴파일된 MI 데이터.
        """
        print(f"{self.mi_type}의 compiling을 시작합니다.")
        redis_name = self.mi_type + '_mi_compile'
        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time / 3600}h")

        def fetch_mi_compile_data() -> MICompileData:
            prophet = tsa.MIProphet(self.mi_type)
            lstm = tsa.MILSTM(self.mi_type)

            data = MICompileData(
                mi_type=self.mi_type,
                prophet_data=prophet.generate_data(refresh=refresh),
                lstm_grade=lstm.get_final_predictions(refresh=refresh)[1],
            )
            data.is_lstm_up = lstm.is_lstm_up()
            data.is_prophet_up = prophet.is_prophet_up(refresh=False)
            data.lstm_html = lstm.export(refresh=False)
            data.prophet_html = prophet.export()
            return data

        mi_compile_data = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_mi_compile_data, timer=expire_time)
        return mi_compile_data

    @staticmethod
    def caching_mi_compile_all(refresh: bool):
        """
        모든 MI(Market Index)에 대해 MICompileData를 캐싱합니다..

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.
        """
        mi_compile = MICompile('WTI')
        print(f"*** MICompileData caching Market Index items ***")
        for mi_type in MIs._fields:
            mi_compile.mi_type = mi_type
            print(f"{mi_type}")
            mi_compile_data = mi_compile.get(refresh=refresh)
            print(mi_compile_data)


@dataclass
class CorpCompileData:
    """
    기업 데이터를 컴파일하여 저장하는 데이터 클래스.

    속성:
        code (str): 기업 코드.
        name (str): 기업 이름.
        red_data (eval.RedData): RED 분석 데이터.
        mil_data (eval.MilData): MIL 분석 데이터.
        prophet_data (tsa.ProphetData): Prophet 예측 데이터.
        lstm_grade (tsa.LSTMGrade): LSTM 등급 데이터.
        is_lstm_up (bool): LSTM 상승 여부.
        is_prophet_up (bool): Prophet 상승 여부.
        lstm_html (str): LSTM 시각화 HTML.
        prophet_html (str): Prophet 시각화 HTML.
    """
    code: str
    name: str

    red_data: eval.RedData
    mil_data: eval.MilData

    prophet_data: tsa.ProphetData
    lstm_grade: tsa.LSTMGrade

    is_lstm_up: bool = False
    is_prophet_up: bool = False

    lstm_html: str = ''
    prophet_html: str = ''


class CorpCompile:
    """
    기업 데이터를 컴파일하는 클래스.

    메서드:
        get(refresh=False) -> CorpCompileData:
            기업 데이터를 컴파일하거나 캐시에서 가져옵니다.

        red_ranking(expect_earn: float = 0.06, refresh=False) -> OrderedDict:
            RED 데이터를 기반으로 기업 순위를 계산합니다.

        prophet_ranking(refresh=False, top: Union[int, str]='all') -> OrderedDict:
            Prophet 데이터를 기반으로 기업 순위를 계산합니다.

        analyse_lstm_topn(refresh: bool, top=40):
            상위 N개의 기업에 대해 LSTM 예측 수행.
    """
    def __init__(self, code: str, expect_earn=0.06):
        """
        CorpCompile 객체를 초기화합니다.

        매개변수:
            code (str): 기업 코드.
            expect_earn (float, optional): 예상 수익률. 기본값은 0.06.
        """
        assert tools.is_6digit(code), f'Invalid value : {code}'
        self._code = code
        self.expect_earn = expect_earn

    @property
    def code(self) -> str:
        """
        기업 코드를 반환합니다.

        반환값:
            str: 기업 코드.
        """
        return self._code

    @code.setter
    def code(self, code: str):
        """
        기업 코드를 변경합니다.

        매개변수:
            code (str): 새로 설정할 기업 코드.
        """
        assert tools.is_6digit(code), f'Invalid value : {code}'
        mylogger.info(f'change code : {self.code} -> {code}')
        self._code = code

    def get(self, refresh=False) -> CorpCompileData:
        """
        기업 데이터를 컴파일하여 캐시에 저장하거나 캐시에서 가져옵니다.

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.

        반환값:
            CorpCompileData: 컴파일된 기업 데이터.
        """
        print(f"{self.code}의 compiling을 시작합니다.")
        redis_name = self.code + '_corp_compile'
        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def fetch_corp_compile_data() -> CorpCompileData:
            prophet = tsa.CorpProphet(self.code)
            lstm = tsa.CorpLSTM(self.code)

            data = CorpCompileData(
                code=self.code,
                name=myredis.Corps(self.code,'c101').get_name(data_from='mongo'),
                red_data=eval.Red(self.code, self.expect_earn).get(refresh=refresh, verbose=False),
                mil_data=eval.Mil(self.code).get(refresh=refresh, verbose=False),
                prophet_data=prophet.generate_data(refresh=refresh),
                lstm_grade=lstm.get_final_predictions(refresh=refresh)[1],
            )

            data.is_lstm_up = lstm.is_lstm_up()
            data.is_prophet_up = prophet.is_prophet_up(refresh=False)
            data.lstm_html = lstm.export(refresh=False)
            data.prophet_html = prophet.export()
            return data

        corp_compile_data = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_corp_compile_data, timer=expire_time)
        return corp_compile_data

    @staticmethod
    def red_ranking(expect_earn: float = 0.06, refresh=False) -> OrderedDict:
        """
        RED 데이터를 기반으로 기업 순위를 계산합니다.

        매개변수:
            expect_earn (float, optional): 예상 수익률. 기본값은 0.06.
            refresh (bool): 데이터를 새로 가져올지 여부.

        반환값:
            OrderedDict: RED 점수를 기준으로 정렬된 기업 순위.
        """
        redis_name = 'red_ranking_prev_expect_earn'
        pee = tools.to_float(myredis.Base.get_value(redis_name))
        if pee != expect_earn:
            mylogger.warning(
                f"expect earn : {expect_earn} / prev expect earn : {pee} 두 값이 달라 refresh = True"
            )
            myredis.Base.set_value(redis_name, str(expect_earn))
            refresh = True

        print("**** Start red_ranking... ****")
        redis_name = 'red_ranking'
        print(
            f"redisname: '{redis_name}' / expect_earn: {expect_earn} / refresh : {refresh} / expire_time : {expire_time / 3600}h")

        def fetch_ranking(refresh_in: bool) -> dict:
            data = {}
            red = eval.Red(code='005930', expect_earn=expect_earn)
            for i, code in enumerate(myredis.Corps.list_all_codes()):
                red.code = code
                red_score = red.get(refresh=refresh_in, verbose=False).score
                if red_score > 0:
                    data[code] = red_score
                    print(f"{i}: {red} - {red_score}")
            return data

        data_dict = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_ranking, refresh, timer=expire_time)

        return OrderedDict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))

    @staticmethod
    def prophet_ranking(refresh=False, top: Union[int, str]='all') -> OrderedDict:
        """
        Prophet 데이터를 기반으로 기업 순위를 계산합니다.

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.
            top (Union[int, str], optional): 상위 기업 개수. 'all'이면 전체 반환. 기본값은 'all'.

        반환값:
            OrderedDict: Prophet 점수를 기준으로 정렬된 기업 순위.
        """
        print("**** Start Compiling scores and sorting... ****")
        redis_name = 'prophet_ranking'

        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def fetch_prophet_ranking() -> dict:
            data = {}
            c = tsa.CorpProphet('005930')
            for code in myredis.Corps.list_all_codes():
                try:
                    c.code = code
                except ValueError:
                    mylogger.error(f'prophet ranking error : {code}')
                    continue
                score= c.generate_data(refresh=refresh).score
                print(f'{code} compiled : {score}')
                data[code] = score
            return data

        data_dict = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_prophet_ranking, timer=expire_time)

        ranking = OrderedDict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))

        if top == 'all':
            return ranking
        else:
            if isinstance(top, int):
                return OrderedDict(list(ranking.items())[:top])
            else:
                raise ValueError("top 인자는 'all' 이나 int형 이어야 합니다.")

    @staticmethod
    def caching_corp_compile_topn(refresh: bool, top=40):
        """
        상위 N개의 기업에 대해 CorpCompileData를 수집합니다..

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.
            top (int, optional): 상위 기업 개수. 기본값은 40.
        """
        ranking_topn = CorpCompile.prophet_ranking(refresh=False, top=top)
        mylogger.info(ranking_topn)
        corp_compile = CorpCompile('005930')
        print(f"*** CorpCompile redis cashing top{top} items ***")
        for i, (code, _) in enumerate(ranking_topn.items()):
            corp_compile.code = code
            print(f"{i + 1}. {code}")
            corp_compile_data = corp_compile.get(refresh=refresh)
            print(corp_compile_data)