import pandas as pd

from dataclasses import dataclass
from typing import Union, Optional, List, Sequence
from app.settings.config import HIST_BTCUSD_4H_PKL


@dataclass
class LoadHist:
    file_path: str = HIST_BTCUSD_4H_PKL

    def __post_init__(self):
        df = self.load_pickle()

    def load_pickle(self):
        return pd.read_pickle(HIST_BTCUSD_4H_PKL)