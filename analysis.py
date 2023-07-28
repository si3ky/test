import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean

# 文字化け対応
plt.rcParams['font.family'] = "MS Gothic"

# csvファイル読込
df = pd.read_csv("tokyo_tintai_data.csv", index_col=0,encoding="shift jis")
# 市区情報追加
df["市区"] = df["アドレス"].apply(lambda x: re.split("[都県市区]", x)[1])
df['家賃(万円)'] = df['家賃'].apply(lambda x: float(re.split('[万円]', x)[0]))

# 地域毎の物件数
grouped = df.groupby("市区")["名称"].count().sort_values(ascending= True)
# 物件数(水平棒グラフ)
grouped.plot(kind="barh", fontsize=16, color="blue")
plt.title("京王線沿物件数")
plt.xlabel("物件数")
plt.xticks(np.arange(0, 600, step=100))
plt.grid()
plt.show()


""" 地域毎の賃金
grouped_price = df.groupby('市区')['家賃(万円)'].mean().sort_values(ascending=False)
# 家賃(水平棒グラフ)
grouped_price.plot(kind='barh', fontsize=16, color='blue')
plt.title('市区町村別賃金（万円）')
plt.xlabel('平均賃金(万円)')
plt.ylabel('市区町村名')
plt.xticks(np.arange(0, 14, step=1))
plt.grid()
plt.show()
"""

# 図として保存
#plt.savefig("物件数グラフ.png")

