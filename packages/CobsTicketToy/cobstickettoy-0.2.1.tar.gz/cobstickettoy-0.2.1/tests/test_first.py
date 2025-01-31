from cobstickettoy.cobstickettoy import aj_count
import pandas as pd

def test_ajc():
    df = aj_count("black toe" , False,"average_sale_price" )
    assert isinstance(df,pd.DataFrame)
    assert len(df) >= 1
    assert df.iat[0,2] >= df.iat[1,2]
