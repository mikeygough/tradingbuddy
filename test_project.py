from project import db_download_data, expected_range, calculate_stats, create_plot
import pandas as pd
from pandas import Timestamp
import matplotlib.pyplot as plt

# read test data
df = pd.read_csv('static/MES.csv')


def test_db_download_data_shape():
    assert db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False).shape == (78, 7)


def test_db_download_data_type():
    assert isinstance(db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False), pd.DataFrame) == True


def test_db_download_data_date_min():
    assert db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False).index.min() == Timestamp('2022-03-01 00:00:00+0000', tz='UTC')


def test_db_download_data_date_max():
    assert db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False).index.max() == Timestamp('2022-05-31 00:00:00+0000', tz='UTC')


def test_calculate_stats_keys():
    stats_dict = calculate_stats(df)
    keys = []
    for key, value in stats_dict.items():
        keys.append(key)
    assert keys == ['close', 'high', 'low', 'return', 'one_sd', 'two_sd',
                    'three_sd', 'historical_vol', 'upper_1', 'upper_2', 
                    'upper_3', 'upper_4', 'upper_5', 'lower_1', 'lower_2',
                    'lower_3', 'lower_4', 'lower_5']


def test_expected_range():
    assert int(expected_range(s=1915.5,
                              v=0.2236,
                              dte=1,
                              y=365)) == 22


def test_create_plot_name():
    assert create_plot(df).__name__ == 'matplotlib.pyplot'
