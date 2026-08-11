import json
import math
import os

# 都道府県別人口（2024年推計、万人単位で概算）
population = {
    "北海道": 508, "青森県": 118, "岩手県": 116, "宮城県": 226, "秋田県": 91,
    "山形県": 102, "福島県": 175, "茨城県": 284, "栃木県": 190, "群馬県": 190,
    "埼玉県": 733, "千葉県": 626, "東京都": 1403, "神奈川県": 922, "新潟県": 213,
    "富山県": 100, "石川県": 108, "福井県": 74, "山梨県": 79, "長野県": 198,
    "岐阜県": 191, "静岡県": 355, "愛知県": 749, "三重県": 170, "滋賀県": 140,
    "京都府": 250, "大阪府": 878, "兵庫県": 530, "奈良県": 128, "和歌山県": 87,
    "鳥取県": 53, "島根県": 64, "岡山県": 184, "広島県": 271, "山口県": 128,
    "徳島県": 68, "香川県": 92, "愛媛県": 128, "高知県": 66, "福岡県": 510,
    "佐賀県": 79, "長崎県": 124, "熊本県": 168, "大分県": 109, "宮崎県": 104,
    "鹿児島県": 152, "沖縄県": 146,
}

TOP_VALUE = 100   # 東京都（人口最多）の初期値
MIN_VALUE = 8     # 人口最少県でも保証する下限

max_pop = max(population.values())
min_pop = min(population.values())

def weighted_value(pop):
    # 平方根で圧縮した比率を 0〜1 に正規化し、MIN〜TOP の範囲に線形マッピング
    sqrt_ratio = (math.sqrt(pop) - math.sqrt(min_pop)) / (math.sqrt(max_pop) - math.sqrt(min_pop))
    return round(MIN_VALUE + sqrt_ratio * (TOP_VALUE - MIN_VALUE))

data = {}
for pref, pop in population.items():
    base = weighted_value(pop)
    data[pref] = {
        "female": base,          # 女性にモテた数
        "male": round(base * 0.85)  # 男性部門はやや控えめ（恣意的な差ではなく初期演出上の目安。要調整）
    }

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ranking.json")
with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 確認用に上位・下位を表示
sorted_data = sorted(data.items(), key=lambda x: -x[1]["female"])
print("=== 上位5件 ===")
for pref, v in sorted_data[:5]:
    print(f"{pref}: 女性 {v['female']} / 男性 {v['male']}")
print("=== 下位5件 ===")
for pref, v in sorted_data[-5:]:
    print(f"{pref}: 女性 {v['female']} / 男性 {v['male']}")

print(f"\n合計区分数: {len(data) * 2}")
