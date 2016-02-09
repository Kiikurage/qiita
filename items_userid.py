import math
import pandas as pd
import requests
import urllib


API_ROOT = "https://qiita.com/api/v2"
TOKEN = "4d6f93ef2c87e2a2ed4d20dfc2d75fc72e98ef31"

items = pd.read_csv("./items.csv", index_col=0)
tags = items["tag"].copy().drop_duplicates()
i_max = tags.index.size

i = 266
p = 1

while i < i_max:
    tag_id = tags[i]
    max_item_count = (items["tag"] == tag_id).sum()
    p_max = math.ceil(max_item_count / 100)

    print("tag_index={0}:{1}({2})".format(i, tag_id, max_item_count))

    while p <= p_max:
        print("page={0}".format(p))

        r = requests.get(API_ROOT + "/tags/{0}/items".format(urllib.parse.quote(tag_id)),
                         params={
                            "page": p,
                            "per_page": 100
                         },
                         headers={
                             "Authorization": "Bearer {}".format(TOKEN)
                         })
        json = r.json()

        item_ids = [item["id"] for item in json]
        user_ids = [item["user"]["id"] for item in json]

        for item_id, user_id in zip(item_ids, user_ids):
            if item_id in items.index:
                items.loc[item_id, "user_id"] = user_id

        p += 1
        if p % 10 == 0:
            items.to_csv("./items.csv")
            items.to_csv("./items.cp.csv")
            print("saved successfully")

    items.to_csv("./items.csv")
    items.to_csv("./items.cp.csv")
    print("saved successfully")

    p = 1
    i += 1
