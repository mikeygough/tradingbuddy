from za_databento import db_download_data
import pandas as pd
from pandas import Timestamp


def test_shape():
    assert db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False).shape == (78, 7)


def test_type():
    assert isinstance(db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False), pd.DataFrame) == True


def test_date_min():
    assert db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False).index.min() == Timestamp('2022-03-01 00:00:00+0000', tz='UTC')


def test_date_max():
    assert db_download_data(SYMBOLS=["ES.n.0"],
                            SCHEMA="ohlcv-1d",
                            START="2022-03-01T00:00",
                            END="2022-05-31T00:10",
                            safety=False).index.max() == Timestamp('2022-05-31 00:00:00+0000', tz='UTC')
