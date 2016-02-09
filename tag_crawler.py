import requests
import pandas as pd
import numpy as np

API_ROOT = "https://qiita.com/api/v2"
TOKEN = "4d6f93ef2c87e2a2ed4d20dfc2d75fc72e98ef31"
data = None
cols = ["followers_count", "icon_url", "id", "items_count"]

for p in range(1, 100 + 1):
    print("page={}".format(p))

    r = requests.get(API_ROOT + "/tags?per_page=100&sort=count&page={}".format(p),
                     headers={
                         "Authorization": "Bearer {}".format(TOKEN)
                     })
    json = r.json()
    if data is None:
        data = [[j["followers_count"], j["icon_url"], j["id"], j["items_count"]] for j in json]
    else:
        data = np.vstack([data, [[j["followers_count"], j["icon_url"], j["id"], j["items_count"]] for j in json]])

    pd.DataFrame(data, columns=cols).to_csv("./tags.csv")
