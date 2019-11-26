import pandas as pd
from acquire import get_log

def irregular_prep(df):
    codeup_ips = ['97.105.19.58', '97.105.19.61']
    df = df.reset_index()