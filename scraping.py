from retry import retry
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 東京 京王線地域URL(suumo)
base_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&rn=0280&ek=028016280&ek=028021960&ek=028039030&ek=028018140&ek=028016130&ek=028009130&ek=028030710&ek=028041450&ek=028024130&ek=028021360&ek=028024850&ek=028017580&ek=028014740&ek=028034190&ek=028024440&ek=028029060&ek=028026310&ek=028023640&ek=028032330&ek=028034340&ek=028021020&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&pc=50&page={}"
@retry(tries=3, delay=10, backoff=2)
def get_html(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup

all_data = []
# 最大ページ数
max_page = 302

for page in range(1, max_page+1):
    url = base_url.format(page)
    soup = get_html(url)
    # 対象ページのアイテム取得
    items = soup.findAll("div", {"class": "cassetteitem"})
    print("page", page, "items", len(items))
    # 各物件要素取得
    for item in items:
        stations = item.findAll("div", {"class": "cassetteitem_detail-text"})

        for station in stations:
            base_data = {}

            # 基礎情報取得
            base_data["名称"] = item.find("div", {"class": "cassetteitem_content-title"}).getText().strip()
            base_data["カテゴリー"] = item.find("div", {"class": "cassetteitem_content-label"}).getText().strip()
            base_data["アドレス"] = item.find("li", {"class": "cassetteitem_detail-col1"}).getText().strip()
            base_data["アクセス"] = station.getText().strip()
            base_data["築年数"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[0].getText().strip()
            base_data["構造"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[1].getText().strip()

            tbodys = item.find("table", {"class": "cassetteitem_other"}).findAll("tbody")

            for tbody in tbodys:
                data = base_data.copy()

                data["階数"] = tbody.findAll("td")[2].getText().strip()
                data["家賃"] = tbody.findAll("td")[3].findAll("li")[0].getText().strip()
                data["管理費"] = tbody.findAll("td")[3].findAll("li")[1].getText().strip()
                data["敷金"] = tbody.findAll("td")[4].findAll("li")[0].getText().strip()
                data["礼金"] = tbody.findAll("td")[4].findAll("li")[1].getText().strip()
                data["間取り"] = tbody.findAll("td")[5].findAll("li")[0].getText().strip()
                data["面積"] = tbody.findAll("td")[5].findAll("li")[1].getText().strip()
                data["URL"] = "https://suumo.jp" + tbody.findAll("td")[8].find("a").get("href")

                all_data.append(data)

df = pd.DataFrame(all_data)
# csv出力
df.to_csv("tokyo_tintai_data.csv",encoding="shift jis")