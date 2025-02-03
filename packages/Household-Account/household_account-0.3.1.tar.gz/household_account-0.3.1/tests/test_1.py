import pytest
import pandas as pd
from household_account.where_now import hha

def test_hha(): 
    
#given
  df = hha(10000, "식비")
 

#when
#then
  assert df.iloc[0]["지출"] == 10000
  assert df.iloc[0]["카테고리"] == "식비"
