from zb_pandas import expected_range, calculate_stats
import pandas as pd

# read test data
df = pd.read_csv('static/MES.csv')


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
