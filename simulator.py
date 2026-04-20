import random

# キャラデータ読み込み
from character_data import character_builds

# 部位
parts = ["花", "羽", "時計", "杯", "冠"]

# =========================
# サブステ候補
# =========================
substat_pool = [
    "会心率",
    "会心ダメージ",
    "攻撃%",
    "HP%",
    "防御%",
    "元素熟知",
    "元素チャージ効率"
]

# =========================
# サブステの伸び幅
# =========================
substat_values = {
    "会心率": [2.7, 3.1, 3.5, 3.9],
    "会心ダメージ": [5.4, 6.2, 7.0, 7.8],
    "攻撃%": [4.1, 4.7, 5.3, 5.8],
    "HP%": [4.1, 4.7, 5.3, 5.8],
    "防御%": [5.1, 5.8, 6.6, 7.3],
    "元素熟知": [16, 19, 21, 23],
    "元素チャージ効率": [4.5, 5.2, 5.8, 6.5]
}

# =========================
# メインステ候補
# =========================
mainstat_options = {
    "花": ["HP"],
    "羽": ["攻撃力"],
    "時計": ["攻撃%", "HP%", "防御%", "元素熟知", "元素チャージ効率"],
    "杯": ["攻撃%", "HP%", "防御%", "元素熟知", "各元素ダメージ"],
    "冠": ["会心率", "会心ダメージ", "攻撃%", "HP%", "防御%", "元素熟知"]
}

# =========================
# 聖遺物生成
# =========================
def generate_artifact(part):
    main = random.choice(mainstat_options[part])

    # 初期サブステ（3 or 4）
    num_substats = random.choice([3, 4])
    subs = random.sample(substat_pool, num_substats)

    substats = {}
    for s in subs:
        substats[s] = random.choice(substat_values[s])

    # 強化回数（3OPなら4回、4OPなら5回）
    upgrades = 4 if num_substats == 3 else 5

    for _ in range(upgrades):
        s = random.choice(list(substats.keys()))
        substats[s] += random.choice(substat_values[s])

    return {
        "部位": part,
        "メイン": main,
        "サブ": substats,
        "スコア": 0  # 後で計算
    }

# =========================
# メインステ構築（UI選択用）
# =========================
def build_selected_mainstats(build_data, clock_choice, goblet_choice, circlet_choice):
    mainstats = dict(build_data["fixed_mainstats"])
    mainstats["時計"] = clock_choice
    mainstats["杯"] = goblet_choice
    mainstats["冠"] = circlet_choice
    return mainstats

# =========================
# 重み付きスコア
# =========================
def calc_weighted_score(substats, weights):
    score = 0
    for stat, weight in weights.items():
        score += substats.get(stat, 0) * weight
    return score

# =========================
# エリクシル生成（固定サブステ付き）
# =========================
def generate_elixir_artifact(part, mainstat, fixed_substats):
    substats = {}

    # 固定サブステ
    for s in fixed_substats:
        substats[s] = random.choice(substat_values[s])

    # 残りサブステをランダム追加（最大4個）
    remaining = [s for s in substat_pool if s not in substats]
    while len(substats) < 4:
        s = random.choice(remaining)
        substats[s] = random.choice(substat_values[s])
        remaining.remove(s)

    # 強化5回
    for _ in range(5):
        s = random.choice(list(substats.keys()))
        substats[s] += random.choice(substat_values[s])

    return {
        "部位": part,
        "メイン": mainstat,
        "サブ": substats,
        "スコア": 0
    }


# =========================
# 振り直し（アップグレードだけ再抽選）
# =========================
def reroll_upgrade_only(artifact, reroll_times=10):
    best = artifact

    for _ in range(reroll_times):
        new_sub = dict(artifact["サブ"])

        for _ in range(5):
            s = random.choice(list(new_sub.keys()))
            new_sub[s] += random.choice(substat_values[s])

        candidate = {
            "部位": artifact["部位"],
            "メイン": artifact["メイン"],
            "サブ": new_sub,
            "スコア": 0
        }

        if candidate["スコア"] > best["スコア"]:
            best = candidate

    return best


# =========================
# カスタムビルド用シミュ
# =========================
def simulate_until_total_score_for_custom_build(
    build,
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000
):
    selected = {p: None for p in parts}
    reinforce_count = 0

    mainstats = build["mainstats"]
    fixed_substats = build["elixir_fixed_substats"]
    score_weights = build["score_weights"]

    while reinforce_count < max_attempts:
        part = random.choice(parts)
        artifact = generate_artifact(part)
        reinforce_count += 1

        # メイン一致チェック
        if artifact["メイン"] == mainstats[part]:
            artifact["スコア"] = round(
                calc_weighted_score(artifact["サブ"], score_weights), 1
            )

            current = selected[part]
            if current is None or artifact["スコア"] > current["スコア"]:
                selected[part] = artifact

        # エリクシル
        if elixir_interval > 0 and reinforce_count % elixir_interval == 0:
            if all(selected[p] is not None for p in parts):
                weakest = min(parts, key=lambda p: selected[p]["スコア"])

                elixir = generate_elixir_artifact(
                    weakest,
                    mainstats[weakest],
                    fixed_substats[weakest]
                )

                elixir["スコア"] = round(
                    calc_weighted_score(elixir["サブ"], score_weights), 1
                )

                if elixir["スコア"] > selected[weakest]["スコア"]:
                    selected[weakest] = elixir

        # 振り直し
        if reroll_interval > 0 and reinforce_count % reroll_interval == 0:
            if all(selected[p] is not None for p in parts):
                weakest = min(parts, key=lambda p: selected[p]["スコア"])

                rerolled = reroll_upgrade_only(
                    selected[weakest],
                    reroll_times=reroll_times
                )

                rerolled["スコア"] = round(
                    calc_weighted_score(rerolled["サブ"], score_weights), 1
                )

                if rerolled["スコア"] > selected[weakest]["スコア"]:
                    selected[weakest] = rerolled

        # 完成チェック
        if all(selected[p] is not None for p in parts):
            total = round(sum(selected[p]["スコア"] for p in parts), 1)
            if total >= target_score:
                return reinforce_count, total, selected

    return None, None, selected


# =========================
# 複数回シミュ
# =========================
def run_custom_build_simulation(
    character_name,
    build_name,
    selected_mainstats,
    score_mode,
    trials=100,
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000
):
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    custom_build = {
        "mainstats": selected_mainstats,
        "elixir_fixed_substats": build_data["elixir_fixed_substats"],
        "score_weights": build_data["score_weight_options"][score_mode]
    }

    results = []
    success_count = 0

    for _ in range(trials):
        count, _, _ = simulate_until_total_score_for_custom_build(
            build=custom_build,
            target_score=target_score,
            elixir_interval=elixir_interval,
            reroll_interval=reroll_interval,
            reroll_times=reroll_times,
            max_attempts=max_attempts
        )

        if count is not None:
            results.append(count)
            success_count += 1

    if not results:
        return {
            "average": None,
            "median": None,
            "top10": None,
            "bottom10": None,
            "results": [],
            "success_rate": 0
        }

    results.sort()
    n = len(results)

    avg = sum(results) / n
    median = results[n // 2] if n % 2 else (results[n//2-1] + results[n//2]) / 2
    top10 = results[int(n * 0.1)]
    bottom10 = results[int(n * 0.9)]

    return {
        "average": round(avg, 1),
        "median": median,
        "top10": top10,
        "bottom10": bottom10,
        "results": results,
        "success_rate": success_count / trials
    }