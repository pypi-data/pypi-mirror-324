from .base import BaseTEJFetcher
from datetime import datetime
from enum import Enum
import pandas as pd
from pymongo import MongoClient
from .tech import TechProcessor
from ..utils import StatsProcessor, YoY_Calculator
import warnings
import yaml


class FinanceReportFetcher(BaseTEJFetcher):

    class FetchMode(Enum):
        YOY = 1
        QOQ = 2
        YOY_NOCAL = 3
        QOQ_NOCAL = 4

    def __init__(
            self,
            mongo_uri,
            db_name=".company",
            collection_name="TWN/AINVFQ1"
        ):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        index_dict = StatsProcessor.load_yaml("tej_db_index.yaml")
        self.check_index = set(index_dict[collection_name])

    def get(
            self,
            ticker,
            fetch_mode: FetchMode = FetchMode.QOQ_NOCAL,
            start_date: str = None,
            end_date: str = None,
            report_type: str = "Q",
            indexes: list = []):
        """
        基礎的query function
        ticker(str): 股票代碼
        start_date(str):  開頭日期範圍
        end_date(str):  = 結束日期範圍
        report_type(str): 報告型態 {"A", "Q", "TTM"}  
        fetch_mode(class FetchMode): 
           YoY : 起始日期到結束日期範圍內，特定該季的資料
           QoQ : 起始日期到結束日期內，每季的資料(與上一季成長率)
        indexes(List): 指定的index
        """
        # 確認indexes中是否有錯誤的index，有的話回傳warning
        if (indexes and self.check_index):
            indexes = set(indexes)
            difference = indexes - self.check_index
            if (difference):
                warnings.warn(
                    f"{list(difference)} 沒有出現在資料表中，請確認column名稱是否正確",
                    UserWarning)

        if (not start_date):
            start_date = datetime.strptime("2005-01-01", "%Y-%m-%d")
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if (fetch_mode in {self.FetchMode.QOQ, self.FetchMode.QOQ_NOCAL}):

            if (not end_date):
                end_date = datetime.today()
            else:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")

            assert (start_date <= end_date)

            start_year = start_date.year
            start_season = (start_date.month - 1) // 4 + 1
            end_year = end_date.year
            end_season = (end_date.month - 1) // 4 + 1

            if (fetch_mode == self.FetchMode.QOQ):
                use_cal = True
            else:
                use_cal = False

            data_df = self.get_QoQ_data(
                ticker=ticker,
                start_year=start_year,
                start_season=start_season,
                end_year=end_year,
                end_season=end_season,
                report_type=report_type,
                indexes=indexes,
                use_cal=use_cal)

            return data_df

        elif (fetch_mode in {self.FetchMode.YOY, self.FetchMode.YOY_NOCAL}):
            start_year = start_date.year
            end_date = self.get_latest_data_time(ticker)
            if (not end_date):
                end_date = datetime.today()

            end_year = end_date.year
            season = (end_date.month - 1) // 4 + 1

            if (fetch_mode == self.FetchMode.YOY):
                use_cal = True
            else:
                use_cal = False

            data_df = self.get_YoY_data(
                ticker=ticker,
                start_year=start_year,
                end_year=end_year,
                season=season,
                report_type=report_type,
                indexes=indexes,
                use_cal=use_cal)

            return data_df

    def get_QoQ_data(
            self,
            ticker,
            start_year,
            start_season,
            end_year,
            end_season,
            report_type="Q",
            indexes=[],
            use_cal=False):
        """
            取得時間範圍內每季資料
        """
        if (use_cal):
            if (start_season == 1):
                lower_bound_year = start_year - 1
                lower_bound_season = 4

            else:
                lower_bound_year = start_year
                lower_bound_season = start_season - 1

        else:
            lower_bound_year = start_year,
            lower_bound_season = start_season

        if (not indexes):    # 沒有指定 -> 取全部
            pipeline = [
                {
                    "$match": {
                        "ticker": ticker
                    }
                }, {
                    "$unwind": "$data"
                }, {
                    "$match": {
                        "$or": [
                            {
                                "data.year": {
                                    "$gt": start_year,
                                    "$lt": end_year
                                }
                            }, {
                                "data.year": start_year,
                                "data.season": {
                                    "$gte": start_season
                                }
                            }, {
                                "data.year": end_year,
                                "data.season": {
                                    "$lte": end_season
                                }
                            }, {
                                "data.year": lower_bound_year,
                                "data.season": lower_bound_season
                            }
                        ]
                    }
                }, {
                    "$project": {
                        "data.year": 1,
                        "data.season": 1,
                        f"data.{report_type}": 1,
                        "_id": 0
                    }
                }
            ]

        else:    # 取指定index
            project_stage = {"data.year": 1, "data.season": 1}
            for index in indexes:
                project_stage[f"data.{report_type}.{index}"] = 1

            pipeline = [
                {
                    "$match": {
                        "ticker": ticker
                    }
                }, {
                    "$unwind": "$data"
                }, {
                    "$match": {
                        "$or": [
                            {
                                "data.year": {
                                    "$gt": start_year,
                                    "$lt": end_year
                                }
                            }, {
                                "data.year": start_year,
                                "data.season": {
                                    "$gte": start_season
                                }
                            }, {
                                "data.year": end_year,
                                "data.season": {
                                    "$lte": end_season
                                }
                            }, {
                                "data.year": lower_bound_year,
                                "data.season": lower_bound_season
                            }
                        ]
                    }
                }, {
                    "$project": project_stage
                }
            ]

        fetched_data = self.collection.aggregate(pipeline).to_list()
        data_dict = StatsProcessor.list_of_dict_to_dict(
            fetched_data,
            keys=["year", "season"],
            delimeter="Q",
            data_key=report_type)

        if (use_cal):
            data_with_QoQ = self.cal_QoQ(data_dict)
            data_df = pd.DataFrame.from_dict(data_with_QoQ)
            data_df = data_df.iloc[:, 1:]
            data_df = data_df.iloc[:, ::-1].T
            data_dict = data_df.to_dict()
            data_dict = self.get_dict_of_df(data_dict)
            return data_dict
        else:
            data_df = pd.DataFrame.from_dict(data_dict)
            data_df = data_df.iloc[:, ::-1]
            return data_df

    def get_YoY_data(
            self,
            ticker,
            start_year,
            end_year,
            season,
            report_type="Q",
            indexes=[],
            use_cal=False):
        """
        取得某季歷年資料
        """
        if (use_cal):
            select_year = set()

            for year in range(start_year, end_year + 1):
                year_shifts = {year, year - 1, year - 3, year - 5, year - 10}

                select_year = select_year.union(year_shifts)

            select_year = sorted(list(select_year), reverse=True)
        else:
            select_year = [year for year in range(start_year, end_year + 1)]

        if (not indexes):    # 沒有指定 -> 取全部
            pipeline = [
                {
                    "$match": {
                        "ticker": ticker
                    }
                }, {
                    "$unwind": "$data"
                }, {
                    "$match": {
                        "$or": [
                            {
                                "$and": [
                                    {
                                        "data.year": {
                                            "$in": select_year
                                        }
                                    }, {
                                        "data.season": {
                                            "$eq": season
                                        }
                                    }
                                ]
                            },
                        ]
                    }
                }, {
                    "$project": {
                        "data.year": 1,
                        "data.season": 1,
                        f"data.{report_type}": 1,
                        "_id": 0
                    }
                }
            ]

        else:    # 取指定index
            project_stage = {"data.year": 1, "data.season": 1}
            for index in indexes:
                project_stage[f"data.{report_type}.{index}"] = 1

            pipeline = [
                {
                    "$match": {
                        "ticker": ticker
                    }
                }, {
                    "$unwind": "$data"
                }, {
                    "$match": {
                        "$and": [
                            {
                                "data.year": {
                                    "$in": select_year
                                }
                            }, {
                                "data.season": {
                                    "$eq": season
                                }
                            }
                        ]
                    }
                }, {
                    "$project": project_stage
                }
            ]

        fetched_data = self.collection.aggregate(pipeline).to_list()

        # 處理計算YoY
        data_dict = StatsProcessor.list_of_dict_to_dict(
            fetched_data,
            keys=['year', 'season'],
            data_key=report_type,
            delimeter='Q')

        if (use_cal):
            data_with_YoY = self.cal_YoY(
                data_dict, start_year, end_year, season)
            data_df = pd.DataFrame.from_dict(data_with_YoY)
            data_df = data_df.iloc[:, ::-1].T
            data_dict = data_df.to_dict()
            data_dict = self.get_dict_of_df(data_dict)
            return data_dict
        else:
            data_df = pd.DataFrame.from_dict(data_dict)
            data_df = data_df.iloc[:, ::-1]
            return data_df


class TEJStockPriceFetcher(BaseTEJFetcher):

    def __init__(
            self,
            mongo_uri,
            db_name: str = "company",
            collection_name: str = None):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name

        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

        self.check_period = ['1d', '7d', '1m', '3m', '1y', '3y', '5y', '10y', 'all']

    def get(
            self,
            ticker: str = "2330",
            start_date: str = "2024-10-01",
            period: str = None
        ):
        """
        取得開高低收資料
        start_date: str: 起始的日期
        period: 指定日期範圍(E.g. 1天, 7天...etc)
        如果宣告period, 以period為優先
        """

        assert (
            period is None or period in self.check_period
        ), f"period should be None or {','.join(self.check_period)}"

        if (period is not None):
            latest_date = self.get_latest_data_time(ticker)
            start_date = self.set_time_shift(date=latest_date, period=period)
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        pipeline = [
            {
                "$match": {
                    "ticker": ticker
                }
            }, {
                "$unwind": "$data"
            }, {
                "$match": {
                    "data.mdate": {
                        "$gt": start_date
                    }
                }
            }, {
                "$project": {
                    "ticker": 1,
                    "data": 1,
                    "_id": 0
                }
            }
        ]
        datas = self.collection.aggregate(pipeline).to_list()

        elements = [element['data'] for element in datas]

        data_df = pd.DataFrame(elements).set_index('mdate')

        return data_df