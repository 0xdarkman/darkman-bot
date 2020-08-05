from dataclasses import dataclass

from app.modules.handlers import get_ma_indicator
from app.settings.config import HIST_BTCUSD_4H_WEIGHTED_PKL
from app.strategies.simple import SimpleMAStrategy
from app.util.df_utils import load_pickle, filter_frame_by_dt_range, change_col_type


@dataclass
class PipeSimpleMA:
    def __post_init__(self):
        self.df = (
            load_pickle(file_path=HIST_BTCUSD_4H_WEIGHTED_PKL)
                .pipe(filter_frame_by_dt_range, start="2020-01-01", end="2020-04-01")
                .pipe(change_col_type, col="Weighted_Price", set_type="float")
                .pipe(get_ma_indicator)
        )
        SimpleMAStrategy(self.df)




