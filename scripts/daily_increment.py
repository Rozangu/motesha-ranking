import json
import random
import math
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ranking.json")

# 都道府県別人口（重み計算に使用。増分の大きさも人口比に緩く比例させる）
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

max_pop = max(population.values())

# 実データ切り替えの閾値（この件数を超えたら実データ運用に切り替える想定。
# 実データ集計の仕組み自体は別途必要で、ここではまだ疑似データ生成のみ）
REAL_DATA_THRESHOLD = 500


def daily_increment(pref, current_value):
    """
    その県の人口規模に応じて、0〜数件のランダムな増分を返す。
    人口が多い県ほど増分の期待値が大きい。
    人口が少ない県は稀に増分0の日があってもよい（不自然な一律増加を避けるため）。
    """
    pop_ratio = population[pref] / max_pop  # 0〜1
    # 増分の期待値：人口比が高いほど大きく、最大でも1日5件程度に抑える
    expected = 0.5 + pop_ratio * 4.5
    increment = max(0, round(random.gauss(expected, expected * 0.4)))
    return increment


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for pref, counts in data.items():
        for gender in ("female", "male"):
            if counts[gender] >= REAL_DATA_THRESHOLD:
                # 閾値を超えた区分は疑似増分を止める
                # （実データ集計に切り替える運用は別スクリプトで対応する前提）
                continue
            counts[gender] += daily_increment(pref, counts[gender])

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("ranking.json を更新しました")


if __name__ == "__main__":
    main()
