from kbostadium.info_sta import info_sta
import pandas as pd
import pytest

def test_info():
    row_count = 3
    is_asc = True
    df = info_sta(keyword="좌석수", asc=is_asc, rcnt=row_count)
    assert isinstance(df,pd.DataFrame)
   # assert

def test_info2():
    row_count = 11
    # When
    df = info_sta(keyword="좌석수", asc=True, rcnt=row_count)
    # assert
    assert isinstance(df, pd.DataFrame) 
    assert len(df) < row_count
    assert df.iloc[0]["구단"] == "키움 히어로즈"
