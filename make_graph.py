import json
import matplotlib.pyplot as plt

files = {
    30: "results/フリーナ_サポート_30days_100000trials_summary.json",
    90: "results/フリーナ_サポート_90days_100000trials_summary.json",
    180: "results/フリーナ_サポート_180days_100000trials_summary.json",
}

days_list = []
bottom10 = []
median = []
top10 = []

for days, path in files.items():
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days_list.append(days)
    bottom10.append(data["summary"]["bottom_10%"])
    median.append(data["summary"]["median"])
    top10.append(data["summary"]["top_10%"])

plt.figure(figsize=(8, 5))
plt.plot(days_list, bottom10, marker="o", label="下位10%")
plt.plot(days_list, median, marker="o", label="中央値")
plt.plot(days_list, top10, marker="o", label="上位10%")
plt.xlabel("日数")
plt.ylabel("スコア")
plt.title("日数ごとのスコア分布")
plt.legend()
plt.tight_layout()
plt.savefig("results/furina_score_band_by_days.png", dpi=200)
plt.show()