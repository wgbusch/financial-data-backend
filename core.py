# Raw Package
import datetime
import json
import multiprocessing
import os
import re
import sys
from typing import List

import numpy as np
import pandas as pd
# Data Source
import yfinance as yf
from joblib import Parallel, delayed, parallel_backend
# Data viz
from tqdm import tqdm

model = ["Open", "High", "Low", "Close", "Adj Close", "Volume", "Symbol", "Name", "Is_ETF"]
pd.options.mode.chained_assignment = None

class mainObj:
    SLICE = 100
    NUMBER_OF_COLUMNS = 0

    exclude = re.compile("^\$[A-Z]$")

    def __init__(self):
        pass

    def main_func(self):
        pass

if __name__ == '__main__':
    mainObj().main_func()
