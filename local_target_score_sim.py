import csv
import json
import time
from pathlib import Path

from simulator import (
    character_builds,
    build_selected_mainstats,
    build_selected_from_current_gear,
    simulate_until_total_score_for_custom_build,
)

OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)


def percentile(sorted_values, p):
    if not sorted_values:
        return None

    n = len(sorted_values)
    index = round((p / 100) * (n - 1))
    index = max(0, min(n - 1, index))
    return sorted_values[index]


def build_tail_percent_table(sorted_values):
    table = {
        "bottom": {},
        "top": {}
    }

    for i in range(1, 101):
        rate = i / 10
        table["bottom"][f"bottom_{rate:.1f}%"] = percentile(sorted_values, rate)
        table["top"][f"top_{rate:.1f}%"] = percentile(sorted_values, 100 - rate)

    return table


def save_attempts_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["trial", "reached", "attempts", "days", "best_score"]
        )
        writer.writeheader()
        writer.writerows(rows)


def build_safe_name(text):
    return (
        str(text)
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace("　", "_")
    )


def main():
    # =========================
    # ここを変えれば条件変更
    # =========================
    character_name = "フリーナ"
    build_name = "サポート"
    score_mode = "HP型"

    target_score = 180
    trials = 100000

    resin_per_day = 180
    max_days = 365

    elixir_interval = 0
    reroll_interval = 0
    reroll_times = 1

    strongbox_enabled = False
    strongbox_target_set = "セット1"

    current_gear = None

    # Noneならビルドの選択肢の先頭を使う
    clock_choice = None
    goblet_choice = None
    circlet_choice = None

    # =========================
    # 条件構築
    # =========================
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    if clock_choice is None:
        clock_choice = build_data["mainstat_options"]["時計"][0]
    if goblet_choice is None:
        goblet_choice = build_data["mainstat_options"]["杯"][0]
    if circlet_choice is None:
        circlet_choice = build_data["mainstat_options"]["冠"][0]

    selected_mainstats = build_selected_mainstats(
        build_data,
        clock_choice=clock_choice,
        goblet_choice=goblet_choice,
        circlet_choice=circlet_choice,
    )

    custom_build = {
        "mainstats": selected_mainstats,
        "elixir_fixed_substats": build_data["elixir_fixed_substats"],
        "score_weights": build_data["score_weight_options"][score_mode],
    }

    initial_selected = build_selected_from_current_gear(current_gear)

    runs_per_day = resin_per_day / 20
    max_attempts = int(max_days * runs_per_day)

    print("=== 目標スコア到達ローカルシミュ開始 ===")
    print(f"キャラ: {character_name}")
    print(f"ビルド: {build_name}")
    print(f"評価: {score_mode}")
    print(f"目標スコア: {target_score}")
    print(f"試行回数: {trials:,}")
    print(f"最大日数: {max_days}日")
    print(f"最大ドロップ回数: {max_attempts:,}")
    print(f"樹脂/日: {resin_per_day}")
    print(f"メインステ: {selected_mainstats}")
    print(f"廻聖: {'あり' if strongbox_enabled else 'なし'}")
    print("================================")

    start = time.time()

    rows = []
    reached_attempts = []
    reached_days = []
    reached_scores = []
    failed_count = 0

    for trial in range(1, trials + 1):
        count, best_total, best_selected = simulate_until_total_score_for_custom_build(
            build=custom_build,
            target_score=target_score,
            elixir_interval=elixir_interval,
            reroll_interval=reroll_interval,
            reroll_times=reroll_times,
            max_attempts=max_attempts,
            initial_selected=initial_selected,
            strongbox_enabled=strongbox_enabled,
            strongbox_target_set=strongbox_target_set,
        )

        reached = count is not None

        if reached:
            days = count / runs_per_day if runs_per_day > 0 else None
            reached_attempts.append(count)
            reached_days.append(days)
            reached_scores.append(best_total)
        else:
            days = None
            failed_count += 1

        rows.append({
            "trial": trial,
            "reached": reached,
            "attempts": count if reached else "",
            "days": round(days, 3) if days is not None else "",
            "best_score": best_total if best_total is not None else "",
        })

        if trial % 1000 == 0:
            elapsed_now = time.time() - start
            print(f"{trial:,}/{trials:,} 完了 / 経過 {elapsed_now:.1f}秒")

    elapsed = time.time() - start

    sorted_attempts = sorted(reached_attempts)
    sorted_days = sorted(reached_days)

    success_rate = len(reached_attempts) / trials * 100 if trials > 0 else 0
    failed_rate = failed_count / trials * 100 if trials > 0 else 0

    summary = {
        "meta": {
            "character_name": character_name,
            "build_name": build_name,
            "score_mode": score_mode,
            "target_score": target_score,
            "trials": trials,
            "resin_per_day": resin_per_day,
            "runs_per_day": runs_per_day,
            "max_days": max_days,
            "max_attempts": max_attempts,
            "elapsed_seconds": elapsed,
            "selected_mainstats": selected_mainstats,
            "elixir_interval": elixir_interval,
            "reroll_interval": reroll_interval,
            "reroll_times": reroll_times,
            "strongbox_enabled": strongbox_enabled,
            "strongbox_target_set": strongbox_target_set,
        },
        "summary": {
            "success_count": len(reached_attempts),
            "failed_count": failed_count,
            "success_rate": success_rate,
            "failed_rate": failed_rate,

            "attempts_average": sum(reached_attempts) / len(reached_attempts) if reached_attempts else None,
            "attempts_median": percentile(sorted_attempts, 50),
            "attempts_bottom_10%": percentile(sorted_attempts, 90),
            "attempts_top_10%": percentile(sorted_attempts, 10),
            "attempts_bottom_1%": percentile(sorted_attempts, 99),
            "attempts_top_1%": percentile(sorted_attempts, 1),

            "days_average": sum(reached_days) / len(reached_days) if reached_days else None,
            "days_median": percentile(sorted_days, 50),
            "days_bottom_10%": percentile(sorted_days, 90),
            "days_top_10%": percentile(sorted_days, 10),
            "days_bottom_1%": percentile(sorted_days, 99),
            "days_top_1%": percentile(sorted_days, 1),
        },
        "days_tail_percent_table": build_tail_percent_table(sorted_days),
        "attempts_tail_percent_table": build_tail_percent_table(sorted_attempts),
    }

    safe_character = build_safe_name(character_name)
    safe_build = build_safe_name(build_name)
    safe_score = build_safe_name(score_mode)

    base_name = (
        f"{safe_character}_{safe_build}_{safe_score}_"
        f"target{target_score}_{max_days}maxdays_{trials}trials"
    )

    csv_path = OUTPUT_DIR / f"{base_name}_target_attempts.csv"
    summary_path = OUTPUT_DIR / f"{base_name}_target_summary.json"

    save_attempts_csv(csv_path, rows)

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n=== 完了 ===")
    print(f"所要時間: {elapsed:.1f}秒")
    print(f"CSV: {csv_path}")
    print(f"JSON: {summary_path}")
    print("\n--- 主要結果 ---")
    print(f"到達率: {success_rate:.2f}%")
    print(f"未到達率: {failed_rate:.2f}%")
    print(f"中央値日数: {summary['summary']['days_median']}")
    print(f"上位10%日数: {summary['summary']['days_top_10%']}")
    print(f"下位10%日数: {summary['summary']['days_bottom_10%']}")
    print(f"上位1%日数: {summary['summary']['days_top_1%']}")
    print(f"下位1%日数: {summary['summary']['days_bottom_1%']}")


if __name__ == "__main__":
    main()