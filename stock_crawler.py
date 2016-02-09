import re
import numpy as np
import pandas as pd
import requests

items = pd.read_csv("./items.cp.csv", index_col=0)
max_item_ind = items.index.size

if "stock_count" not in items.columns:
    items["stock_count"] = np.tile([-1], items.shape[0])

if "user_id" not in items.columns:
    items["user_id"] = np.tile([""], items.shape[0])

i_start = (items["stock_count"] != -1).sum()

for i in range(i_start, items.index.size):
    ind = items.index[i]
    res = requests.get("http://qiita.com/items/" + ind)
    ma = re.search("\"js\-stocksCount\">(\d+)<", res.text)
    ma2 = re.search("qiita.com/([^/]+)/items", res.url)

    if ma is None:
        items["stock_count"][i] = 0
    else:
        items["stock_count"][i] = int(ma.group(1))

    if ma is None:
        items["user_id"][i] = "NOT_FOUND"
    else:
        items["user_id"][i] = ma2.group(1)

    print(i, ind)

    if i % 50 == 0:
        items.to_csv("./items.cp.csv")
        items.to_csv("./items.csv")
        print("saved successfully.")
