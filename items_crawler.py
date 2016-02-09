import math

import dateutil.parser
import pandas as pd
import requests
import urllib


API_ROOT = "https://qiita.com/api/v2"
TOKEN = "4d6f93ef2c87e2a2ed4d20dfc2d75fc72e98ef31"

tags = pd.read_csv("./tags.csv", index_col=0)
data = pd.read_csv("./items.csv", index_col=0)
i_max = tags.index.size

last_data = data.ix[data.index[-1]]
last_tag_id = last_data["tag"]
i = tags.index[tags["id"] == last_tag_id].values[0]
p = 1 + math.floor((data["tag"] == last_tag_id).sum() / 100)

while i < i_max:
    tag_id = tags["id"][i]
    max_item_count = tags["items_count"][i]
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

        for item in json:
            user = item["user"]

            if item["id"] in data.index:
                continue

            created = dateutil.parser.parse(item["created_at"])
            data_add = pd.DataFrame(
                index=[item["id"]],
                data={
                    "body_length": len(item["body"]),
                    "line_count": len(item["body"].split("<br")),
                    "created": created.timestamp(),
                    "created_hour": created.hour,
                    "created_weekday": created.weekday(),
                    "tags_count": len(item["tags"]),
                    "tag": tag_id,
                    "title": item["title"],
                    "user_id": user["id"],
                    "user_follower_count": user["followers_count"],
                    "user_followee_count": user["followees_count"],
                    "user_items_count": user["items_count"]
                })

            data = pd.concat(data_add, axis=0)  # type: pd.DataFrame

        p += 1

    data.to_csv("./items.csv")
    data.to_csv("./items.cp.csv")
    p = 1
    i += 1
