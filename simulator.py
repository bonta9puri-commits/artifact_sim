import random

parts = ["花", "羽", "時計", "杯", "冠"]

mainstat_weights = {
    "花": {"HP": 100},
    "羽": {"攻撃力": 100},
    "時計": {
        "HP%": 26.66,
        "攻撃%": 26.66,
        "防御%": 26.67,
        "元素チャージ効率": 10,
        "元素熟知": 10
    },
    "杯": {
        "HP%": 19.25,
        "攻撃%": 19.25,
        "防御%": 19,
        "元素熟知": 2.5,
        "炎ダメージ": 5,
        "水ダメージ": 5,
        "雷ダメージ": 5,
        "氷ダメージ": 5,
        "風ダメージ": 5,
        "岩ダメージ": 5,
        "草ダメージ": 5,
        "物理ダメージ": 5
    },
    "冠": {
        "HP%": 22,
        "攻撃%": 22,
        "防御%": 22,
        "元素熟知": 10,
        "会心率": 10,
        "会心ダメージ": 10,
        "治療効果": 4
    }
}

substats_pool = [
    "会心率",
    "会心ダメージ",
    "攻撃%",
    "攻撃実数",
    "HP%",
    "HP実数",
    "防御%",
    "防御実数",
    "元素熟知",
    "元素チャージ効率"
]

substat_values = {
    "会心率": [2.7, 3.1, 3.5, 3.9],
    "会心ダメージ": [5.4, 6.2, 7.0, 7.8],
    "攻撃%": [4.1, 4.7, 5.3, 5.8],
    "攻撃実数": [14, 16, 18, 19],
    "HP%": [4.1, 4.7, 5.3, 5.8],
    "HP実数": [209, 239, 269, 299],
    "防御%": [5.1, 5.8, 6.6, 7.3],
    "防御実数": [16, 19, 21, 23],
    "元素熟知": [16, 19, 21, 23],
    "元素チャージ効率": [4.5, 5.2, 5.8, 6.5]
}

target_mainstats = {
    "花": "HP",
    "羽": "攻撃力",
    "時計": "元素チャージ効率",
    "杯": "HP%",
    "冠": "会心ダメージ"
}

character_builds = {
    "フリーナ": {
        "element": "水",
        "weapon": "片手剣",
        "role": "サブアタッカー",
        "mainstats": {
            "花": "HP",
            "羽": "攻撃力",
            "時計": "元素チャージ効率",
            "杯": "HP%",
            "冠": "会心ダメージ"
        },
        "elixir_fixed_substats": {
            "花": ["会心率", "会心ダメージ"],
            "羽": ["会心率", "会心ダメージ"],
            "時計": ["会心率", "会心ダメージ"],
            "杯": ["会心率", "会心ダメージ"],
            "冠": ["会心率", "HP%"]
        },
        "target_score": 180,
        "label": "実用ライン"
    },

    "ヌヴィレット": {
        "element": "水",
        "weapon": "法器",
        "role": "メインアタッカー",
        "mainstats": {
            "花": "HP",
            "羽": "攻撃力",
            "時計": "HP%",
            "杯": "水ダメージ",
            "冠": "会心ダメージ"
        },
        "elixir_fixed_substats": {
            "花": ["会心率", "会心ダメージ"],
            "羽": ["会心率", "会心ダメージ"],
            "時計": ["会心率", "会心ダメージ"],
            "杯": ["会心率", "会心ダメージ"],
            "冠": ["会心率", "HP%"]
        },
        "target_score": 180,
        "label": "実用ライン"
    },

    "雷電将軍": {
        "element": "雷",
        "weapon": "長柄武器",
        "role": "メインアタッカー",
        "mainstats": {
            "花": "HP",
            "羽": "攻撃力",
            "時計": "元素チャージ効率",
            "杯": "雷ダメージ",
            "冠": "会心率"
        },
        "elixir_fixed_substats": {
            "花": ["会心率", "会心ダメージ"],
            "羽": ["会心率", "会心ダメージ"],
            "時計": ["会心率", "会心ダメージ"],
            "杯": ["会心率", "会心ダメージ"],
            "冠": ["会心ダメージ", "攻撃%"]
        },
        "target_score": 180,
        "label": "実用ライン"
    }

}
elixir_fixed_substats = {
    "花": ["会心率", "会心ダメージ"],
    "羽": ["会心率", "会心ダメージ"],
    "時計": ["会心率", "会心ダメージ"],
    "杯": ["会心率", "会心ダメージ"],
    "冠": ["会心率", "HP%"]
}

def generate_mainstat(part):
    choices = list(mainstat_weights[part].keys())
    weights = list(mainstat_weights[part].values())
    return random.choices(choices, weights=weights, k=1)[0]

def generate_substats(mainstat):
    num_subs = random.choice([3, 4])
    pool = [s for s in substats_pool if s != mainstat]
    chosen = random.sample(pool, num_subs)

    substats = {}
    for stat in chosen:
        substats[stat] = random.choice(substat_values[stat])

    return substats

def upgrade_artifact(substats, mainstat):
    substats = substats.copy()

    if len(substats) == 3:
        pool = [s for s in substats_pool if s not in substats and s != mainstat]
        new_stat = random.choice(pool)
        substats[new_stat] = random.choice(substat_values[new_stat])

    for _ in range(4):
        stat = random.choice(list(substats.keys()))
        substats[stat] += random.choice(substat_values[stat])

    return substats

def calc_score(substats):
    return substats.get("会心率", 0) * 2 + substats.get("会心ダメージ", 0)+ substats.get("HP％", 0)

def generate_artifact(part):
    mainstat = generate_mainstat(part)
    base_substats = generate_substats(mainstat)
    upgraded_substats = upgrade_artifact(base_substats, mainstat)

    return {
        "部位": part,
        "メイン": mainstat,
        "初期サブ": base_substats.copy(),
        "サブ": upgraded_substats,
        "スコア": round(calc_score(upgraded_substats), 1)
    }

def reroll_upgrade_only(artifact, reroll_times=10):
    mainstat = artifact["メイン"]
    original_base_substats = artifact["初期サブ"]

    best_substats = artifact["サブ"]
    best_score = artifact["スコア"]

    for _ in range(reroll_times):
        rerolled_substats = upgrade_artifact(original_base_substats, mainstat)
        rerolled_score = round(calc_score(rerolled_substats), 1)

        if rerolled_score > best_score:
            best_score = rerolled_score
            best_substats = rerolled_substats

    return {
        "部位": artifact["部位"],
        "メイン": artifact["メイン"],
        "初期サブ": original_base_substats.copy(),
        "サブ": best_substats,
        "スコア": best_score
    }

def generate_elixir_artifact(part, mainstat, fixed_substats):
    remaining_pool = [
        s for s in substats_pool
        if s != mainstat and s not in fixed_substats
    ]

    base_substats = {}

    for stat in fixed_substats:
        base_substats[stat] = random.choice(substat_values[stat])

    extra_subs = random.sample(remaining_pool, 2)
    for stat in extra_subs:
        base_substats[stat] = random.choice(substat_values[stat])

    upgraded_substats = upgrade_artifact(base_substats, mainstat)

    return {
        "部位": part,
        "メイン": mainstat,
        "初期サブ": base_substats.copy(),
        "サブ": upgraded_substats,
        "スコア": round(calc_score(upgraded_substats), 1)
    }

def simulate_until_total_score(
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000
):
    selected = {p: None for p in parts}
    reinforce_count = 0

    while reinforce_count < max_attempts:
        part = random.choice(parts)
        artifact = generate_artifact(part)
        reinforce_count += 1

        # その部位が未所持、または今の装備より強ければ更新
        if selected[part] is None or artifact["スコア"] > selected[part]["スコア"]:
            selected[part] = artifact

        # エリクシル処理
        if elixir_interval > 0 and reinforce_count % elixir_interval == 0:
            if all(selected[p] is not None for p in parts):
                weakest_part = min(parts, key=lambda p: selected[p]["スコア"])

                elixir_artifact = generate_elixir_artifact(
                    weakest_part,
                    target_mainstats[weakest_part],
                    elixir_fixed_substats[weakest_part]
                )

                if elixir_artifact["スコア"] > selected[weakest_part]["スコア"]:
                    selected[weakest_part] = elixir_artifact

        # リロール処理
        if reroll_interval > 0 and reinforce_count % reroll_interval == 0:
            if all(selected[p] is not None for p in parts):
                weakest_part = min(parts, key=lambda p: selected[p]["スコア"])

                rerolled_artifact = reroll_upgrade_only(
                    selected[weakest_part],
                    reroll_times=reroll_times
                )

                if rerolled_artifact["スコア"] > selected[weakest_part]["スコア"]:
                    selected[weakest_part] = rerolled_artifact

        # 合計スコア判定
        if all(selected[p] is not None for p in parts):
            total_score = round(sum(selected[p]["スコア"] for p in parts), 1)
            if total_score >= target_score:
                return reinforce_count, total_score, selected

    return None, None, selected


def run_multiple_simulations(
    trials=100,
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000
):
    results = []
    success_count = 0

    for _ in range(trials):
        count, _, _ = simulate_until_total_score(
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
            "success_count": 0,
            "success_rate": 0.0,
            "average": None,
            "median": None,
            "top10": None,
            "bottom10": None,
            "results": []
        }

    results.sort()
    n = len(results)

    average = sum(results) / n
    if n % 2 == 1:
        median = results[n // 2]
    else:
        median = (results[n // 2 - 1] + results[n // 2]) / 2

    top10 = results[min(n - 1, int(n * 0.1))]
    bottom10 = results[min(n - 1, int(n * 0.9))]

    return {
        "success_count": success_count,
        "success_rate": success_count / trials,
        "average": round(average, 1),
        "median": median,
        "top10": top10,
        "bottom10": bottom10,
        "results": results
    }

def simulate_until_total_score_for_build(
    build,
    target_score=None,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000
):
    selected = {p: None for p in parts}
    reinforce_count = 0

    mainstats = build["mainstats"]
    fixed_substats = build["elixir_fixed_substats"]

    if target_score is None:
        target_score = build["target_score"]

    while reinforce_count < max_attempts:
        part = random.choice(parts)
        artifact = generate_artifact(part)
        reinforce_count += 1

        # 指定メインだけ採用
        if artifact["メイン"] == mainstats[part]:
            current = selected[part]
            if current is None or artifact["スコア"] > current["スコア"]:
                selected[part] = artifact

        # エリクシル
        if elixir_interval > 0 and reinforce_count % elixir_interval == 0:
            if all(selected[p] is not None for p in parts):
                weakest_part = min(parts, key=lambda p: selected[p]["スコア"])

                elixir_artifact = generate_elixir_artifact(
                    weakest_part,
                    mainstats[weakest_part],
                    fixed_substats[weakest_part]
                )

                if elixir_artifact["スコア"] > selected[weakest_part]["スコア"]:
                    selected[weakest_part] = elixir_artifact

        # 振り直し
        if reroll_interval > 0 and reinforce_count % reroll_interval == 0:
            if all(selected[p] is not None for p in parts):
                weakest_part = min(parts, key=lambda p: selected[p]["スコア"])

                rerolled_artifact = reroll_upgrade_only(
                    selected[weakest_part],
                    reroll_times=reroll_times
                )

                if rerolled_artifact["スコア"] > selected[weakest_part]["スコア"]:
                    selected[weakest_part] = rerolled_artifact

        # 完成判定
        if all(selected[p] is not None for p in parts):
            total_score = round(sum(selected[p]["スコア"] for p in parts), 1)
            if total_score >= target_score:
                return reinforce_count, total_score, selected

    return None, None, selected

def run_character_simulation(
    character_name,
    trials=100,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000
):
    build = character_builds[character_name]
    target_score = build["target_score"]

    results = []
    success_count = 0

    for _ in range(trials):
        count, _, _ = simulate_until_total_score_for_build(
            build=build,
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
            "character": character_name,
            "label": build["label"],
            "target_score": target_score,
            "success_count": 0,
            "success_rate": 0.0,
            "average": None,
            "median": None,
            "top10": None,
            "bottom10": None,
            "results": [],
            "mainstats": build["mainstats"]
        }

    results.sort()
    n = len(results)

    average = sum(results) / n

    if n % 2 == 1:
        median = results[n // 2]
    else:
        median = (results[n // 2 - 1] + results[n // 2]) / 2

    top10 = results[min(n - 1, int(n * 0.1))]
    bottom10 = results[min(n - 1, int(n * 0.9))]

    return {
        "character": character_name,
        "label": build["label"],
        "target_score": target_score,
        "success_count": success_count,
        "success_rate": success_count / trials,
        "average": round(average, 1),
        "median": median,
        "top10": top10,
        "bottom10": bottom10,
        "results": results,
        "mainstats": build["mainstats"]
    }