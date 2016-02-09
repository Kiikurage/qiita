import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

items_all = pd.read_csv("./items.cp.csv", index_col=0)
tags = pd.read_csv("./tags.csv", index_col=0)

fig = plt.figure()
axis = fig.add_subplot(111)
handles = []

for i in range(0, 4 + 1):
    tag = tags.ix[i]
    items = items_all[items_all["tag"] == tag["id"]]
    created = items["created"]
    res = pd.DataFrame()

    for year in range(2012, 2015 + 1):
        for month in range(1, 12 + 1):
            next_month = 1 if month == 12 else month + 1
            next_year = year + 1 if month == 12 else year

            d_from = datetime.datetime(year, month, 1).timestamp()
            d_to = datetime.datetime(next_year, next_month, 1).timestamp()
            count = np.bitwise_and(d_from <= created, created < d_to).sum()
            res = pd.concat((res, pd.DataFrame(
                    data=[["{0}/{1}".format(year, month), count]],
                    columns=["label", "count"]
            )))

    h = axis.plot(np.arange(res.index.size), res["count"],
                  label=tag["id"])
    handles.append(h[0])

mask = np.arange(res.index.size) % 4 == 3
axis.set_xticks(np.arange(res.index.size)[mask])
axis.set_xticklabels(res["label"].values[mask], rotation=90)
axis.legend(handles=handles, loc="best")
axis.set_ylabel("number of items")
fig.savefig("./fig.png")
