# import os
# import re
# import pandas as pd
# import numpy as np
# import scipy as sp
# import tushare as ts


# df=ts.get_hist_data('600848','2018-01-01','2018-12-31')


# def get_high_t(df,col_name):
#     for idx,value in enumerate(df[col_name]):
#         if idx == 0:
#             continue
#         elif idx == len(df[col_name]) - 1:
#             break
#         high = df[col_name][idx - 1] + df[col_name][idx] + df[col_name][idx + 1]
#         print(high)

# get_high_t(df,'high')

def s(n):
    if n == 0:
        return 0
    else:
        return n + s(n-1)

print(s(2))