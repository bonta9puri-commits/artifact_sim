import random
from itertools import product

# キャラデータ読み込み
from character_data import character_builds

# 部位
parts = ["花", "羽", "時計", "杯", "冠"]
set_names = ["セット1", "セット2"]

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
    "元素チャージ効率",
    "攻撃",
    "HP",
    "防御"
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
    "元素チャージ効率": [4.5, 5.2, 5.8, 6.5],
    "攻撃":[14,16,18,19],
    "HP":[209,239,269,299],
    "防御":[16,19,21,23]
}

# =========================
# メインステ候補
# =========================
mainstat_options = {
    "花": ["HP"],
    "羽": ["攻撃力"],
    "時計": ["攻撃%", "HP%", "防御%", "元素熟知", "元素チャージ効率"],
    "杯": ["攻撃%", "HP%", "防御%", "元素熟知", "炎ダメージ", "水ダメージ", "氷ダメージ", "雷ダメージ", "風ダメージ", "岩ダメージ", "草ダメージ", "物理ダメージ" ],
    "冠": ["会心率", "会心ダメージ", "攻撃%", "HP%", "防御%", "元素熟知","治療効果"]
}


mainstat_weights = {
    "花": {
        "HP": 100
    },
    "羽": {
        "攻撃力": 100
    },
    "時計": {
        "攻撃%": 26.68,
        "HP%": 26.66,
        "防御%": 26.66,
        "元素熟知": 10.00,
        "元素チャージ効率": 10.00
    },
    "杯": {
        "攻撃%": 19.25,
        "HP%": 19.25,
        "防御%": 19.00,
        "元素熟知": 2.50,
        "炎ダメージ":5.00,
        "水ダメージ":5.00, 
        "氷ダメージ":5.00, 
        "雷ダメージ":5.00,
        "風ダメージ":5.00, 
        "岩ダメージ":5.00,
        "草ダメージ":5.00,
        "物理ダメージ":5.00 
    },
    "冠": {
        "会心率": 10.00,
        "会心ダメージ": 10.00,
        "治療効果": 4.00,
        "攻撃%": 22.00,
        "HP%": 22.00,
        "防御%": 22.00,
        "元素熟知": 10.00
    }
}

def get_forbidden_substat(mainstat):
    if mainstat == "会心率":
        return "会心率"
    elif mainstat == "会心ダメージ":
        return "会心ダメージ"
    elif mainstat == "攻撃%":
        return "攻撃%"
    elif mainstat == "HP%":
        return "HP%"
    elif mainstat == "防御%":
        return "防御%"
    elif mainstat == "元素熟知":
        return "元素熟知"
    elif mainstat == "元素チャージ効率":
        return "元素チャージ効率"
    else:
        return None

def generate_artifact(part, score_weights=None):
    candidates = list(mainstat_weights[part].keys())
    weights = list(mainstat_weights[part].values())
    main = random.choices(candidates, weights=weights, k=1)[0]

    artifact_set = random.choice(set_names)

    num_substats = random.choices([3, 4], weights=[80, 20], k=1)[0]

    forbidden_sub = get_forbidden_substat(main)
    available_substats = [s for s in substat_pool if s != forbidden_sub]

    subs = random.sample(available_substats, num_substats)

    substats = {}
    for s in subs:
        substats[s] = random.choice(substat_values[s])

    initial_substats = substats.copy()

    upgrades = 4 if num_substats == 3 else 5

    for _ in range(upgrades):
        s = random.choice(list(substats.keys()))
        substats[s] += random.choice(substat_values[s])

    if score_weights is None:
        score_weights = {
            "会心率": 2.0,
            "会心ダメージ": 1.0,
            "攻撃%": 1.0
        }

    score = round(calc_weighted_score(substats, score_weights), 1)

    return {
        "部位": part,
        "セット": artifact_set,
        "メイン": main,
        "初期サブ": initial_substats,
        "サブ": substats,
        "スコア": score
    }
st.caption("簡易スコア: 会心率×2 + 会心ダメージ×1 + 攻撃%×1")
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

    forbidden_sub = get_forbidden_substat(mainstat)

    # 固定サブステ
    for s in fixed_substats:
        if s in substat_values and s != forbidden_sub:
            substats[s] = random.choice(substat_values[s])

    # 残りサブステをランダム追加（最大4個）
    remaining = [s for s in substat_pool if s not in substats and s != forbidden_sub]
    while len(substats) < 4 and remaining:
        s = random.choice(remaining)
        substats[s] = random.choice(substat_values[s])
        remaining.remove(s)

    initial_substats = substats.copy()

    # 強化5回
    for _ in range(5):
        s = random.choice(list(substats.keys()))
        substats[s] += random.choice(substat_values[s])

    return {
        "部位": part,
        "メイン": mainstat,
        "初期サブ": initial_substats,
        "サブ": substats,
        "スコア": 0
    }
# =========================
# 振り直し（アップグレードだけ再抽選）
# =========================
def find_best_valid_combo(selected, required_set="セット1", min_count=4):
    choices_per_part = []

    for p in parts:
        candidates = []

        for set_name in set_names:
            artifact = selected[p][set_name]
            if artifact is not None:
                candidates.append(artifact)

        if not candidates:
            return None, None

        choices_per_part.append(candidates)

    best_total = None
    best_combo = None

    for combo in product(*choices_per_part):
        required_count = sum(1 for a in combo if a["セット"] == required_set)

        if required_count >= min_count:
            total = round(sum(a["スコア"] for a in combo), 1)

            if best_total is None or total > best_total:
                best_total = total
                best_combo = combo

    return best_total, best_combo
def reroll_upgrade_only(artifact, reroll_times=10, score_weights=None):
    best = {
        "部位": artifact["部位"],
        "セット": artifact.get("セット"),
        "メイン": artifact["メイン"],
        "初期サブ": dict(artifact.get("初期サブ", artifact["サブ"])),
        "サブ": dict(artifact["サブ"]),
        "スコア": artifact.get("スコア", 0)
    }

    base_sub = dict(artifact.get("初期サブ", artifact["サブ"]))

    for _ in range(reroll_times):
        new_sub = dict(base_sub)

        # 3OP/4OPを厳密に持っていないので簡易的に5回振り直し
        for _ in range(5):
            s = random.choice(list(new_sub.keys()))
            new_sub[s] += random.choice(substat_values[s])

        candidate_score = 0
        if score_weights is not None:
            candidate_score = round(calc_weighted_score(new_sub, score_weights), 1)

        candidate = {
            "部位": artifact["部位"],
            "セット": artifact.get("セット"),
            "メイン": artifact["メイン"],
            "初期サブ": dict(base_sub),
            "サブ": new_sub,
            "スコア": candidate_score
        }

        if candidate["スコア"] > best.get("スコア", 0):
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
    selected = {
        p: {
            "セット1": None,
            "セット2": None
        }
        for p in parts
    }

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

            artifact_set = artifact["セット"]
            current = selected[part][artifact_set]

            if current is None or artifact["スコア"] > current["スコア"]:
                selected[part][artifact_set] = artifact

        # エリクシル
        if elixir_interval > 0 and reinforce_count % elixir_interval == 0:
            best_total, best_combo = find_best_valid_combo(selected)

            if best_combo is not None:
                weakest_artifact = min(best_combo, key=lambda a: a["スコア"])
                weakest_part = weakest_artifact["部位"]
                weakest_set = weakest_artifact["セット"]

                elixir = generate_elixir_artifact(
                    weakest_part,
                    mainstats[weakest_part],
                    fixed_substats[weakest_part]
                )

                # エリクシルでもセットは維持
                elixir["セット"] = weakest_set
                elixir["スコア"] = round(
                    calc_weighted_score(elixir["サブ"], score_weights), 1
                )

                current = selected[weakest_part][weakest_set]
                if current is None or elixir["スコア"] > current["スコア"]:
                    selected[weakest_part][weakest_set] = elixir

        # 振り直し
        if reroll_interval > 0 and reinforce_count % reroll_interval == 0:
            best_total, best_combo = find_best_valid_combo(selected)

            if best_combo is not None:
                weakest_artifact = min(best_combo, key=lambda a: a["スコア"])
                weakest_part = weakest_artifact["部位"]
                weakest_set = weakest_artifact["セット"]

                rerolled = reroll_upgrade_only(
                    weakest_artifact,
                    reroll_times=reroll_times,
                    score_weights=score_weights
                )

                rerolled["セット"] = weakest_set

                current = selected[weakest_part][weakest_set]
                if current is None or rerolled["スコア"] > current["スコア"]:
                    selected[weakest_part][weakest_set] = rerolled

        # 完成チェック
        best_total, best_combo = find_best_valid_combo(selected)

        if best_total is not None and best_total >= target_score:
            best_selected = {artifact["部位"]: artifact for artifact in best_combo}
            return reinforce_count, best_total, best_selected

    return None, None, selected
# =========================
# 単体シミュ用の簡易デフォルトビルド
# =========================
def simulate_until_total_score(
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000
):
    default_build = {
        "mainstats": {
            "花": "HP",
            "羽": "攻撃力",
            "時計": "攻撃%",
            "杯": "攻撃%",
            "冠": "会心ダメージ"
        },
        "elixir_fixed_substats": {
            "花": ["会心率", "会心ダメージ"],
            "羽": ["会心率", "会心ダメージ"],
            "時計": ["会心率", "会心ダメージ"],
            "杯": ["会心率", "会心ダメージ"],
            "冠": ["会心率", "会心ダメージ"]
        },
        "score_weights": {
            "会心率": 2.0,
            "会心ダメージ": 1.0,
            "攻撃%": 1.0
        }
    }

    return simulate_until_total_score_for_custom_build(
        build=default_build,
        target_score=target_score,
        elixir_interval=elixir_interval,
        reroll_interval=reroll_interval,
        reroll_times=reroll_times,
        max_attempts=max_attempts
    )

# =========================
# 複数回シミュ
# =========================
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
            "success_rate": 0,
            "average": None,
            "median": None,
            "top10": None,
            "bottom10": None,
            "results": []
        }

    results.sort()
    n = len(results)

    avg = sum(results) / n
    median = results[n // 2] if n % 2 else (results[n // 2 - 1] + results[n // 2]) / 2
    top10 = results[int(n * 0.1)]
    bottom10 = results[int(n * 0.9)]

    return {
        "success_count": success_count,
        "success_rate": success_count / trials,
        "average": round(avg, 1),
        "median": median,
        "top10": top10,
        "bottom10": bottom10,
        "results": results
    }

# =========================
# カスタムビルド複数回シミュ
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
            "character": character_name,
            "label": build_name,
            "target_score": target_score,
            "mainstats": selected_mainstats,
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
    median = results[n // 2] if n % 2 else (results[n // 2 - 1] + results[n // 2]) / 2
    top10 = results[int(n * 0.1)]
    bottom10 = results[int(n * 0.9)]

    return {
        "character": character_name,
        "label": build_name,
        "target_score": target_score,
        "mainstats": selected_mainstats,
        "average": round(avg, 1),
        "median": median,
        "top10": top10,
        "bottom10": bottom10,
        "results": results,
        "success_rate": success_count / trials
    }

# =========================
# キャラ用簡易シミュ
# =========================
def run_character_simulation(
    character_name,
    build_name,
    trials=100,
    elixir_interval=0,
    reroll_interval=0,
    reroll_times=1,
    max_attempts=100000
):
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    selected_mainstats = dict(build_data["fixed_mainstats"])
    selected_mainstats["時計"] = build_data["mainstat_options"]["時計"][0]
    selected_mainstats["杯"] = build_data["mainstat_options"]["杯"][0]
    selected_mainstats["冠"] = build_data["mainstat_options"]["冠"][0]

    score_mode = list(build_data["score_weight_options"].keys())[0]

    result = run_custom_build_simulation(
        character_name=character_name,
        build_name=build_name,
        selected_mainstats=selected_mainstats,
        score_mode=score_mode,
        trials=trials,
        target_score=build_data["default_target_score"],
        elixir_interval=elixir_interval,
        reroll_interval=reroll_interval,
        reroll_times=reroll_times,
        max_attempts=max_attempts
    )

    result["build_name"] = build_name
    result["element"] = character_data.get("element", "-")
    result["weapon"] = character_data.get("weapon", "-")

    return result