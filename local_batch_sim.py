import json
import csv
import time
from pathlib import Path

from simulator import (
    character_builds,
    build_selected_mainstats,
    run_fixed_period_build_simulation,
)

OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)


def percentile(sorted_values, p):
    """
    sorted_values: 昇順ソート済みリスト
    p: 0〜100
    """
    if not sorted_values:
        return None

    n = len(sorted_values)
    index = round((p / 100) * (n - 1))
    return sorted_values[index]


def build_tail_percent_table(sorted_scores):
    """
    下位0.1%〜10.0%、上位0.1%〜10.0%を0.1%刻みで保存する。
    sorted_scores: 昇順ソート済みスコア
    """
    table = {
        "bottom": {},
        "top": {}
    }

    for i in range(1, 101):
        rate = i / 10  # 0.1, 0.2, ... 10.0

        # 下位 rate%
        table["bottom"][f"bottom_{rate:.1f}%"] = percentile(sorted_scores, rate)

        # 上位 rate% = percentile 100-rate
        table["top"][f"top_{rate:.1f}%"] = percentile(sorted_scores, 100 - rate)

    return table


def save_scores_csv(path, scores):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["score"])
        for score in scores:
            writer.writerow([score])


def main():
    # ===== ここを変えれば条件変更 =====
    character_name = "フリーナ"
    build_name = "サポート"
    score_mode = "HP型"

    days = 90
    resin_per_day = 180
    trials = 100000

    elixir_interval = 0
    reroll_interval = 0
    reroll_times = 1

    strongbox_enabled = False
    strongbox_target_set = "セット1"

    target_scores = [160, 180, 200, 220]

    build_data = character_builds[character_name]["builds"][build_name]

    selected_mainstats = build_selected_mainstats(
        build_data,
        clock_choice=build_data["mainstat_options"]["時計"][0],
        goblet_choice=build_data["mainstat_options"]["杯"][0],
        circlet_choice=build_data["mainstat_options"]["冠"][0],
    )

    start = time.time()

    result = run_fixed_period_build_simulation(
        character_name=character_name,
        build_name=build_name,
        selected_mainstats=selected_mainstats,
        score_mode=score_mode,
        days=days,
        resin_per_day=resin_per_day,
        trials=trials,
        elixir_interval=elixir_interval,
        reroll_interval=reroll_interval,
        reroll_times=reroll_times,
        current_gear=None,
        strongbox_enabled=strongbox_enabled,
        strongbox_target_set=strongbox_target_set,
    )

    elapsed = time.time() - start

    scores = result["results"]
    sorted_scores = sorted(scores)

    summary = {
        "meta": {
            "character_name": character_name,
            "build_name": build_name,
            "score_mode": score_mode,
            "days": days,
            "resin_per_day": resin_per_day,
            "total_attempts": result["total_attempts"],
            "trials": trials,
            "elapsed_seconds": elapsed,
            "selected_mainstats": selected_mainstats,
            "elixir_interval": elixir_interval,
            "reroll_interval": reroll_interval,
            "reroll_times": reroll_times,
            "strongbox_enabled": strongbox_enabled,
            "strongbox_target_set": strongbox_target_set,
        },
        "summary": {
            "average": result["average"],
            "median": result["median"],
            "bottom_1%": percentile(sorted_scores, 1),
            "bottom_10%": percentile(sorted_scores, 10),
            "top_10%": percentile(sorted_scores, 90),
            "top_1%": percentile(sorted_scores, 99),
            "min": sorted_scores[0],
            "max": sorted_scores[-1],
        },
        "target_success_rates": {
            str(target): sum(score >= target for score in scores) / len(scores) * 100
            for target in target_scores
        },
        "tail_percent_table": build_tail_percent_table(sorted_scores),
    }

    base_name = f"{character_name}_{build_name}_{days}days_{trials}trials"

    save_scores_csv(OUTPUT_DIR / f"{base_name}_scores.csv", scores)

    with open(OUTPUT_DIR / f"{base_name}_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("完了")
    print(f"条件: {character_name} / {build_name} / {days}日 / {trials:,}回")
    print(f"所要時間: {elapsed:.1f}秒")
    print(f"中央値: {summary['summary']['median']}")
    print(f"上位10%: {summary['summary']['top_10%']}")
    print(f"上位1%: {summary['summary']['top_1%']}")
    print(f"スコア180到達率: {summary['target_success_rates'].get('180', 0):.2f}%")


if __name__ == "__main__":
    main()