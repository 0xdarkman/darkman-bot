from app.modules.indicator import Indicator


def get_ma_indicator(df):
    return Indicator.ma(df, col="Weighted_Price", n=15)
