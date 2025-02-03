import abc
from typing import Union
from pymongo import MongoClient
import pandas as pd
import json
import pytz
from datetime import datetime, timedelta, date
from ..utils import StatsDateTime, StatsProcessor, YoY_Calculator
import yaml


class StatsFetcher:

    def __init__(self, ticker, db_client):
        self.ticker = ticker
        self.db = db_client["company"]    # Replace with your database name
        self.collection = self.db["twse_stats"]

        self.timezone = pytz.timezone("Asia/Taipei")

        self.target_metric_dict = {
            'value': ['value'],
            'value_and_percentage': ['value', 'percentage'],
            'percentage': ['percentage'],
            'grand_total': ['grand_total'],
            'grand_total_values': ['grand_total', 'grand_total_percentage'],
            'grand_total_percentage': ['grand_total_percentage'],
            'growth': [f'YoY_{i}' for i in [1, 3, 5, 10]],
            'grand_total_growth': [f"YoY_{i}" for i in [1, 3, 5, 10]]
        }

    def prepare_query(self):
        return [
            {
                "$match": {
                    "ticker": self.ticker,
                }
            },
        ]

    def collect_data(self, start_date, end_date):
        pipeline = self.prepare_query()

        fetched_data = list(self.collection.aggregate(pipeline))

        return fetched_data[0]

    def str_to_datetime(self, date_str):
        year, month, day = [int(num) for num in date_str.split("-")]

        date = datetime.strptime(date_str, "%Y-%m-%d")
        date = self.timezone.localize(date)

        season = (month - 1) // 3 + 1

        return StatsDateTime(date, year, month, day, season)

    def has_required_columns(self, df: pd.DataFrame, required_cols=None):
        """
        Check if the required columns are present in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to check.
            required_cols (list, optional): List of required column names. 
                                            Defaults to ['date', 'open', 'high', 'low', 'close', 'volume'].

        Returns:
            bool: True if all required columns are present, False otherwise.
        """
        if required_cols is None:
            required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']

        return all(col in df.columns for col in required_cols)


class BaseTEJFetcher(abc.ABC):

    @abc.abstractmethod
    def get(self):
        pass

    def get_latest_data_time(self, ticker):
        latest_data = self.collection.find_one(
            {"ticker": ticker}, {
                "last_update": 1,
                "_id": 0
            })

        try:
            latest_date = latest_data['last_update']["latest_data_date"]
        except Exception as e:
            latest_date = None

        return latest_date

    def cal_YoY(
            self, data_dict: dict, start_year: int, end_year: int, season: int):
        year_shifts = [1, 3, 5, 10]
        return_dict = {}
        for year in range(start_year, end_year + 1):
            try:
                year_data = data_dict[f"{year}Q{season}"].copy()
            except KeyError as e:
                continue

            year_keys = list(year_data.keys())
            for key in year_keys:
                if (key in 'season'):
                    continue

                if (isinstance(year_data[key], (int, float))):
                    temp_dict = {"value": year_data[key]}

                    for shift in year_shifts:
                        this_value = year_data[key]
                        try:
                            past_year = year - shift
                            last_value = data_dict[f"{past_year}Q{season}"][key]
                            temp_dict[
                                f"YoY_{shift}"] = YoY_Calculator.cal_growth(
                                    this_value, last_value, delta=shift)
                        except Exception as e:
                            temp_dict[f"YoY_{shift}"] = None

                    year_data[key] = temp_dict

                else:
                    year_data.pop(key)

            return_dict[f"{year}Q{season}"] = year_data

        return return_dict

    def cal_QoQ(self, data_dict):
        return_dict = {}
        for i, time_index in enumerate(data_dict.keys()):
            year, season = time_index.split("Q")
            year = int(year)
            season = int(season)
            if (season == 1):
                last_year = year - 1
                last_season = 4
            else:
                last_year = year
                last_season = season - 1

            this_data = data_dict[time_index]
            this_keys = list(this_data.keys())
            for key in this_keys:
                if (key in 'season'):
                    continue

                this_value = this_data[key]

                if (isinstance(this_value, (int, float))):
                    temp_dict = {"value": this_value}

                    try:
                        last_value = data_dict[f"{last_year}Q{last_season}"][
                            key]['value']

                        temp_dict['growth'] = YoY_Calculator.cal_growth(
                            this_value, last_value, delta=1)
                    except Exception as e:
                        temp_dict['growth'] = None

                    this_data[key] = temp_dict

                else:
                    this_data.pop(key)
            return_dict[time_index] = this_data
        return return_dict

    def get_dict_of_df(self, data_dict):
        """
        dict[dict] -> dict[df]
        """
        for key in data_dict.keys():
            data_dict[key] = pd.DataFrame.from_dict(data_dict[key])
        return data_dict

    def set_time_shift(self, date: Union[str, datetime], period: str):
        if (isinstance(date, str)):
            date = datetime.strptime(date, "%Y-%m-%d")
        if (period == '1d'):
            return date - timedelta(days=1)

        elif (period == '7d'):
            return date - timedelta(days=7)

        elif (period == '1m'):
            return date - timedelta(days=30)

        elif (period == '3m'):
            return date - timedelta(days=90)

        elif (period == '1y'):
            return date - timedelta(days=365)

        elif (period == '3y'):
            return date - timedelta(days=365 * 3)

        elif (period == '5y'):
            return date - timedelta(days=365 * 5)

        elif (period == '10y'):
            return date - timedelta(days=365 * 10)

        elif (period == 'all'):
            return datetime.strptime("1991-01-01", "%Y-%m-%d")
