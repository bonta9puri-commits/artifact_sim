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


mainstat_final_values = {
    "花": {"HP": 4780},
    "羽": {"攻撃力": 311},
    "時計": {
        "攻撃%": 46.6,
        "HP%": 46.6,
        "防御%": 58.3,
        "元素熟知": 187,
        "元素チャージ効率": 51.8
    },
    "杯": {
        "攻撃%": 46.6,
        "HP%": 46.6,
        "防御%": 58.3,
        "元素熟知": 187,
        "炎ダメージ": 46.6,
        "水ダメージ": 46.6,
        "氷ダメージ": 46.6,
        "雷ダメージ": 46.6,
        "風ダメージ": 46.6,
        "岩ダメージ": 46.6,
        "草ダメージ": 46.6,
        "物理ダメージ": 58.3
    },
    "冠": {
        "会心率": 31.1,
        "会心ダメージ": 62.2,
        "攻撃%": 46.6,
        "HP%": 46.6,
        "防御%": 58.3,
        "元素熟知": 187,
        "治療効果": 35.9
    }
}


def sum_selected_stats(selected_artifacts, include_mainstats=True):
    total = {}

    if not selected_artifacts:
        return total

    for artifact in selected_artifacts.values():
        if artifact is None:
            continue

        for stat, value in artifact.get("サブ", {}).items():
            total[stat] = total.get(stat, 0) + value

        if include_mainstats:
            part = artifact.get("部位")
            mainstat = artifact.get("メイン")

            if part in mainstat_final_values and mainstat in mainstat_final_values[part]:
                value = mainstat_final_values[part][mainstat]
                total[mainstat] = total.get(mainstat, 0) + value

    return total
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
        "治療効果": 10.00,
        "攻撃%": 22.00,
        "HP%": 22.00,
        "防御%": 22.00,
        "元素熟知": 4.00
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

def generate_artifact(part, score_weights=None, forced_set=None):
    candidates = list(mainstat_weights[part].keys())
    weights = list(mainstat_weights[part].values())
    main = random.choices(candidates, weights=weights, k=1)[0]

    artifact_set = forced_set if forced_set is not None else random.choice(set_names)

    num_substats = random.choices([3, 4], weights=[80, 20], k=1)[0]

    forbidden_sub = get_forbidden_substat(main)
    available_substats = [s for s in substat_pool if s != forbidden_sub]

    subs = random.sample(available_substats, num_substats)

    substats = {}
    for s in subs:
        substats[s] = random.choice(substat_values[s])

    initial_substats = substats.copy()

    if num_substats == 3:
        remaining_subs = [s for s in available_substats if s not in substats]
        new_sub = random.choice(remaining_subs)
        substats[new_sub] = random.choice(substat_values[new_sub])

        for _ in range(4):
            s = random.choice(list(substats.keys()))
            substats[s] += random.choice(substat_values[s])
    else:
        for _ in range(5):
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
        "初期OP数": num_substats,
        "スコア": score
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

def sum_selected_substats(selected_artifacts):
    total = {}

    if not selected_artifacts:
        return total

    for artifact in selected_artifacts.values():
        if artifact is None:
            continue

        for stat, value in artifact.get("サブ", {}).items():
            total[stat] = total.get(stat, 0) + value

    return total


def calc_effective_crit_score(
    substats,
    base_crit_rate=5.0,
    base_crit_damage=50.0,
    crit_rate_cap=100.0,
    overflow_mode="to_cd",
    overflow_ratio=1.0
):
    total_cr = base_crit_rate + substats.get("会心率", 0)
    total_cd = base_crit_damage + substats.get("会心ダメージ", 0)

    overflow_cr = max(total_cr - crit_rate_cap, 0.0)
    effective_cr = min(total_cr, crit_rate_cap)

    adjusted_cd = total_cd
    if overflow_mode == "to_cd":
        adjusted_cd += overflow_cr * overflow_ratio

    expected_crit_value = (effective_cr / 100.0) * adjusted_cd

    return {
        "total_cr": round(total_cr, 1),
        "effective_cr": round(effective_cr, 1),
        "overflow_cr": round(overflow_cr, 1),
        "total_cd": round(total_cd, 1),
        "adjusted_cd": round(adjusted_cd, 1),
        "expected_crit_value": round(expected_crit_value, 2)
    }

def calc_resistance_multiplier(resistance_percent):
    r = resistance_percent / 100.0

    if r < 0:
        return 1 - r / 2
    elif r < 0.75:
        return 1 - r
    else:
        return 1 / (1 + 4 * r)


def calc_defense_multiplier(character_level=90, enemy_level=100, defense_reduction=0.0, defense_ignore=0.0):
    # defense_reduction, defense_ignore は 0.0 ~ 1.0 想定
    effective_enemy_def = (enemy_level + 100) * (1 - defense_reduction) * (1 - defense_ignore)
    return (character_level + 100) / ((character_level + 100) + effective_enemy_def)

def calc_damage_index(
    substats,
    base_stat,
    stat_type="攻撃",
    base_crit_rate=5.0,
    base_crit_damage=50.0,
    dmg_bonus=0.0,
    flat_bonus=0.0,
    crit_rate_cap=100.0,
    overflow_mode="to_cd",
    overflow_ratio=1.0,
    character_level=90,
    enemy_level=100,
    enemy_resistance=10.0,
    defense_reduction=0.0,
    defense_ignore=0.0,
    talent_multiplier=100.0
):

    percent_key_map = {
        "攻撃": "攻撃%",
        "HP": "HP%",
        "防御": "防御%"
    }

    flat_key_map = {
        "攻撃": "攻撃",
        "HP": "HP",
        "防御": "防御"
    }

    percent_key = percent_key_map[stat_type]
    flat_key = flat_key_map[stat_type]

    stat_percent = substats.get(percent_key, 0)
    flat_stat = substats.get(flat_key, 0) + flat_bonus

    final_stat = base_stat * (1 + stat_percent / 100.0) + flat_stat

    crit_result = calc_effective_crit_score(
        substats=substats,
        base_crit_rate=base_crit_rate,
        base_crit_damage=base_crit_damage,
        crit_rate_cap=crit_rate_cap,
        overflow_mode=overflow_mode,
        overflow_ratio=overflow_ratio
    )

    dmg_bonus_multiplier = 1 + dmg_bonus / 100.0
    talent_multiplier_value = talent_multiplier / 100.0
    resistance_multiplier = calc_resistance_multiplier(enemy_resistance)
    defense_multiplier = calc_defense_multiplier(
        character_level=character_level,
        enemy_level=enemy_level,
        defense_reduction=defense_reduction,
        defense_ignore=defense_ignore
    )

    non_crit_index = final_stat * talent_multiplier_value * dmg_bonus_multiplier
    crit_index = non_crit_index * (1 + crit_result["adjusted_cd"] / 100.0)
    expected_index = non_crit_index * (
        1 + (crit_result["effective_cr"] / 100.0) * (crit_result["adjusted_cd"] / 100.0)
    )

    final_non_crit_index = non_crit_index * resistance_multiplier * defense_multiplier
    final_crit_index = crit_index * resistance_multiplier * defense_multiplier
    final_expected_index = expected_index * resistance_multiplier * defense_multiplier

    return {
        "final_stat": round(final_stat, 1),
        "non_crit_index": round(non_crit_index, 1),
        "crit_index": round(crit_index, 1),
        "expected_index": round(expected_index, 1),

        "resistance_multiplier": round(resistance_multiplier, 4),
        "defense_multiplier": round(defense_multiplier, 4),

        "final_non_crit_index": round(final_non_crit_index, 1),
        "final_crit_index": round(final_crit_index, 1),
        "final_expected_index": round(final_expected_index, 1),

        "crit": crit_result
    }

def run_custom_build_preview(
    character_name,
    build_name,
    selected_mainstats,
    score_mode,
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000,
    current_gear=None,
    strongbox_enabled=False,
    strongbox_target_set="セット1",
    overflow_mode="to_cd",
    overflow_ratio=1.0
):
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    custom_build = {
        "mainstats": selected_mainstats,
        "elixir_fixed_substats": build_data["elixir_fixed_substats"],
        "score_weights": build_data["score_weight_options"][score_mode]
    }

    initial_selected = build_selected_from_current_gear(current_gear)

    count, best_total, best_selected = simulate_until_total_score_for_custom_build(
        build=custom_build,
        target_score=target_score,
        elixir_interval=elixir_interval,
        reroll_interval=reroll_interval,
        reroll_times=reroll_times,
        max_attempts=max_attempts,
        initial_selected=initial_selected,
        strongbox_enabled=strongbox_enabled,
        strongbox_target_set=strongbox_target_set
    )

    if count is None or not best_selected:
        return None

    preview_result = calc_damage_preview_from_selected(
        character_name=character_name,
        build_name=build_name,
        selected_artifacts=best_selected,
        overflow_mode=overflow_mode,
        overflow_ratio=overflow_ratio
    )

    return {
        "character": character_name,
        "label": build_name,
        "target_score": target_score,
        "attempts": count,
        "best_total": best_total,
        "selected_artifacts": best_selected,
        "preview_result": preview_result
    }

def run_fixed_period_build_preview(
    character_name,
    build_name,
    selected_mainstats,
    score_mode,
    days,
    resin_per_day,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    current_gear=None,
    strongbox_enabled=False,
    strongbox_target_set="セット1",
    overflow_mode="to_cd",
    overflow_ratio=1.0
):
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    custom_build = {
        "mainstats": selected_mainstats,
        "elixir_fixed_substats": build_data["elixir_fixed_substats"],
        "score_weights": build_data["score_weight_options"][score_mode]
    }

    initial_selected = build_selected_from_current_gear(current_gear)
    total_attempts = int(days * resin_per_day / 20)

    best_total, best_selected = simulate_score_after_fixed_attempts_for_custom_build(
        build=custom_build,
        total_attempts=total_attempts,
        elixir_interval=elixir_interval,
        reroll_interval=reroll_interval,
        reroll_times=reroll_times,
        initial_selected=initial_selected,
        strongbox_enabled=strongbox_enabled,
        strongbox_target_set=strongbox_target_set
    )

    if not best_selected:
        return None

    preview_result = calc_damage_preview_from_selected(
        character_name=character_name,
        build_name=build_name,
        selected_artifacts=best_selected,
        overflow_mode=overflow_mode,
        overflow_ratio=overflow_ratio
    )

    return {
        "character": character_name,
        "label": build_name,
        "days": days,
        "total_attempts": total_attempts,
        "best_total": best_total,
        "selected_artifacts": best_selected,
        "preview_result": preview_result
    }

# =========================
# 統計まとめ
# =========================
def summarize_results(results):
    if not results:
        return {
            "average": None,
            "median": None,
            "best10": None,
            "worst10": None,
            "results": []
        }

    results = sorted(results)
    n = len(results)

    avg = sum(results) / n
    median = results[n // 2] if n % 2 else (results[n // 2 - 1] + results[n // 2]) / 2
    best10 = results[int(n * 0.1)]
    worst10 = results[int(n * 0.9)]

    return {
        "average": round(avg, 1),
        "median": median,
        "best10": best10,
        "worst10": worst10,
        "results": results
    }
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
        "初期OP数": 4,
        "スコア": 0
    }
# =========================
# 振り直し（アップグレードだけ再抽選）
# =========================
def build_selected_from_current_gear(current_gear):
    selected = {
        p: {
            "セット1": None,
            "セット2": None
        }
        for p in parts
    }

    if current_gear is None:
        return selected

    for part, artifact in current_gear.items():
        if artifact is None:
            continue

        artifact_set = artifact.get("セット")
        if part not in selected:
            continue
        if artifact_set not in selected[part]:
            continue

        selected[part][artifact_set] = {
            "部位": artifact["部位"],
            "セット": artifact["セット"],
            "メイン": artifact["メイン"],
            "スコア": artifact["スコア"],
            "初期サブ": artifact.get("初期サブ"),
            "サブ": artifact.get("サブ"),
            "初期OP数": artifact.get("初期OP数")
        }

    return selected
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
        "初期OP数": artifact.get("初期OP数", len(artifact.get("初期サブ", artifact["サブ"]))),
        "スコア": artifact.get("スコア", 0)
    }

    base_sub = dict(artifact.get("初期サブ", artifact["サブ"]))
    initial_op_count = artifact.get("初期OP数", len(base_sub))
    reroll_upgrades = 4 if initial_op_count == 3 else 5

    for _ in range(reroll_times):
        new_sub = dict(base_sub)

        for _ in range(reroll_upgrades):
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
            "初期OP数": initial_op_count,
            "スコア": candidate_score
        }

        if candidate["スコア"] > best.get("スコア", 0):
            best = candidate

    return best


def try_apply_strongbox(selected, build, strongbox_count, strongbox_target_set="セット1"):
    mainstats = build["mainstats"]
    score_weights = build["score_weights"]

    while strongbox_count >= 3:
        strongbox_count -= 3

        part = random.choice(parts)
        artifact = generate_artifact(
            part,
            score_weights=score_weights,
            forced_set=strongbox_target_set
        )

        if artifact["メイン"] == mainstats[part]:
            artifact["スコア"] = round(
                calc_weighted_score(artifact["サブ"], score_weights), 1
            )

            current = selected[part][strongbox_target_set]
            if current is None or artifact["スコア"] > current["スコア"]:
                selected[part][strongbox_target_set] = artifact

    return selected, strongbox_count
# =========================
# カスタムビルド用シミュ
# =========================
def simulate_until_total_score_for_custom_build(
    build,
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000,
    initial_selected=None,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
):
    if initial_selected is None:
        selected = {
            p: {
                "セット1": None,
                "セット2": None
            }
            for p in parts
        }
    else:
        selected = {
            p: {
                "セット1": initial_selected.get(p, {}).get("セット1"),
                "セット2": initial_selected.get(p, {}).get("セット2")
            }
            for p in parts
        }

    reinforce_count = 0
    strongbox_count = 0

    mainstats = build["mainstats"]
    fixed_substats = build["elixir_fixed_substats"]
    score_weights = build["score_weights"]

    while reinforce_count < max_attempts:
        part = random.choice(parts)
        artifact = generate_artifact(part)
        reinforce_count += 1

        # メイン一致チェック
        used_artifact = False
        used_artifact = False
        if artifact["メイン"] == mainstats[part]:
            artifact["スコア"] = round(
                calc_weighted_score(artifact["サブ"], score_weights), 1
            )

            artifact_set = artifact["セット"]
            current = selected[part][artifact_set]

            if current is None or artifact["スコア"] > current["スコア"]:
                selected[part][artifact_set] = artifact
                used_artifact = True

        if strongbox_enabled and not used_artifact:
            strongbox_count += 1
            selected, strongbox_count = try_apply_strongbox(
                selected,
                build,
                strongbox_count,
                strongbox_target_set=strongbox_target_set
            )

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

        best_total, best_combo = find_best_valid_combo(selected)

        if best_total is not None and best_total >= target_score:
            best_selected = {artifact["部位"]: artifact for artifact in best_combo}
            return reinforce_count, best_total, best_selected

    return None, None, selected

def simulate_score_after_fixed_attempts_for_custom_build(
    build,
    total_attempts,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    initial_selected=None,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
):
    if initial_selected is None:
        selected = {
            p: {
                "セット1": None,
                "セット2": None
            }
            for p in parts
        }
    else:
        selected = {
            p: {
                "セット1": initial_selected.get(p, {}).get("セット1"),
                "セット2": initial_selected.get(p, {}).get("セット2")
            }
            for p in parts
        }

    reinforce_count = 0
    strongbox_count = 0

    mainstats = build["mainstats"]
    fixed_substats = build["elixir_fixed_substats"]
    score_weights = build["score_weights"]

    while reinforce_count < total_attempts:
        part = random.choice(parts)
        artifact = generate_artifact(part)
        reinforce_count += 1

        used_artifact = False
        if artifact["メイン"] == mainstats[part]:
            artifact["スコア"] = round(
                calc_weighted_score(artifact["サブ"], score_weights), 1
            )

            artifact_set = artifact["セット"]
            current = selected[part][artifact_set]

            if current is None or artifact["スコア"] > current["スコア"]:
                selected[part][artifact_set] = artifact
                used_artifact = True

        if strongbox_enabled and not used_artifact:
            strongbox_count += 1
            selected, strongbox_count = try_apply_strongbox(
                selected,
                build,
                strongbox_count,
                strongbox_target_set=strongbox_target_set
            )

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

                elixir["セット"] = weakest_set
                elixir["スコア"] = round(
                    calc_weighted_score(elixir["サブ"], score_weights), 1
                )

                current = selected[weakest_part][weakest_set]
                if current is None or elixir["スコア"] > current["スコア"]:
                    selected[weakest_part][weakest_set] = elixir

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

    best_total, best_combo = find_best_valid_combo(selected)

    if best_total is None:
        return 0, selected

    best_selected = {artifact["部位"]: artifact for artifact in best_combo}
    return best_total, best_selected

# =========================
# 単体シミュ用の簡易デフォルトビルド
# =========================
def simulate_until_total_score(
    target_score=180,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    max_attempts=100000,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
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
        max_attempts=max_attempts,
        strongbox_enabled=strongbox_enabled,
        strongbox_target_set=strongbox_target_set
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
    max_attempts=100000,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
):
    results = []
    success_count = 0

    for _ in range(trials):
        count, _, _ = simulate_until_total_score(
            target_score=target_score,
            elixir_interval=elixir_interval,
            reroll_interval=reroll_interval,
            reroll_times=reroll_times,
            max_attempts=max_attempts,
            strongbox_enabled=strongbox_enabled,
            strongbox_target_set=strongbox_target_set
        )

        if count is not None:
            results.append(count)
            success_count += 1

    summary = summarize_results(results)

    return {
        "success_count": success_count,
        "success_rate": success_count / trials if trials > 0 else 0,
        "average": summary["average"],
        "median": summary["median"],
        "best10": summary["best10"],
        "worst10": summary["worst10"],
        "results": summary["results"]
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
    max_attempts=100000,
    current_gear=None,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
):
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    custom_build = {
        "mainstats": selected_mainstats,
        "elixir_fixed_substats": build_data["elixir_fixed_substats"],
        "score_weights": build_data["score_weight_options"][score_mode]
    }

    initial_selected = build_selected_from_current_gear(current_gear)

    results = []
    success_count = 0

    for _ in range(trials):
        count, _, _ = simulate_until_total_score_for_custom_build(
            build=custom_build,
            target_score=target_score,
            elixir_interval=elixir_interval,
            reroll_interval=reroll_interval,
            reroll_times=reroll_times,
            max_attempts=max_attempts,
            initial_selected=initial_selected,
            strongbox_enabled=strongbox_enabled,
            strongbox_target_set=strongbox_target_set
        )

        if count is not None:
            results.append(count)
            success_count += 1

    summary = summarize_results(results)

    return {
        "character": character_name,
        "label": build_name,
        "target_score": target_score,
        "mainstats": selected_mainstats,
        "average": summary["average"],
        "median": summary["median"],
        "best10": summary["best10"],
        "worst10": summary["worst10"],
        "results": summary["results"],
        "success_rate": success_count / trials if trials > 0 else 0
    }

def run_fixed_period_build_simulation(
    character_name,
    build_name,
    selected_mainstats,
    score_mode,
    days,
    resin_per_day,
    trials=100,
    elixir_interval=250,
    reroll_interval=1000,
    reroll_times=10,
    current_gear=None,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
):
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    custom_build = {
        "mainstats": selected_mainstats,
        "elixir_fixed_substats": build_data["elixir_fixed_substats"],
        "score_weights": build_data["score_weight_options"][score_mode]
    }

    initial_selected = build_selected_from_current_gear(current_gear)

    total_attempts = int(days * resin_per_day / 20)
    results = []

    for _ in range(trials):
        total_score, _ = simulate_score_after_fixed_attempts_for_custom_build(
            build=custom_build,
            total_attempts=total_attempts,
            elixir_interval=elixir_interval,
            reroll_interval=reroll_interval,
            reroll_times=reroll_times,
            initial_selected=initial_selected,
            strongbox_enabled=strongbox_enabled,
            strongbox_target_set=strongbox_target_set
        )
        results.append(total_score)

    summary = summarize_results(results)

    return {
        "character": character_name,
        "label": build_name,
        "days": days,
        "resin_per_day": resin_per_day,
        "total_attempts": total_attempts,
        "mainstats": selected_mainstats,
        "average": summary["average"],
        "median": summary["median"],
        "best10": summary["best10"],
        "worst10": summary["worst10"],
        "results": summary["results"]
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

def build_damage_preview_base(character_name, build_name):
    character_data = character_builds[character_name]
    build_data = character_data["builds"][build_name]

    preview = build_data.get("damage_preview")
    if preview is None:
        raise ValueError(f"{character_name} / {build_name} に damage_preview がありません")

    stat_type = preview.get("stat_type", "攻撃")

    base_hp = preview.get("base_hp", 0.0)
    base_atk = preview.get("base_atk", 0.0)
    base_def = preview.get("base_def", 0.0)

    weapon_base_stat = preview.get("weapon_base_stat", 0.0)
    weapon_sub_stat = dict(preview.get("weapon_sub_stat", {}))

    ascension_stat = dict(preview.get("ascension_stat", {}))
    extra_stats = dict(preview.get("extra_stats", {}))

    base_crit_rate = preview.get("base_crit_rate", 5.0)
    base_crit_damage = preview.get("base_crit_damage", 50.0)
    talent_multiplier = preview.get("talent_multiplier", 100.0)
    crit_rate_cap = preview.get("crit_rate_cap", 100.0)

    elemental_bonus_type = preview.get("elemental_bonus_type")
    default_enemy = dict(preview.get("default_enemy", {}))

    if stat_type == "攻撃":
        base_stat = base_atk + weapon_base_stat
    elif stat_type == "HP":
        base_stat = base_hp
    elif stat_type == "防御":
        base_stat = base_def
    else:
        raise ValueError(f"未対応の stat_type: {stat_type}")

    base_stats = {}

    for stat, value in weapon_sub_stat.items():
        base_stats[stat] = base_stats.get(stat, 0.0) + value

    asc_type = ascension_stat.get("type")
    asc_value = ascension_stat.get("value", 0.0)
    if asc_type:
        base_stats[asc_type] = base_stats.get(asc_type, 0.0) + asc_value

    for stat, value in extra_stats.items():
        base_stats[stat] = base_stats.get(stat, 0.0) + value

    total_base_crit_rate = base_crit_rate + base_stats.get("会心率", 0.0)
    total_base_crit_damage = base_crit_damage + base_stats.get("会心ダメージ", 0.0)

    elemental_bonus = 0.0
    if elemental_bonus_type:
        elemental_bonus = base_stats.get(elemental_bonus_type, 0.0)

    return {
        "character": character_name,
        "build_name": build_name,
        "stat_type": stat_type,
        "base_stat": round(base_stat, 2),
        "base_hp": round(base_hp, 2),
        "base_atk": round(base_atk, 2),
        "base_def": round(base_def, 2),
        "weapon_base_stat": round(weapon_base_stat, 2),
        "base_stats": base_stats,
        "base_crit_rate": round(total_base_crit_rate, 2),
        "base_crit_damage": round(total_base_crit_damage, 2),
        "talent_multiplier": talent_multiplier,
        "crit_rate_cap": round(crit_rate_cap, 2),
        "elemental_bonus_type": elemental_bonus_type,
        "elemental_bonus": round(elemental_bonus, 2),
        "default_enemy": default_enemy
    }


def merge_total_stats_for_damage_preview(base_stats, artifact_stats):
    total = dict(base_stats)

    for stat, value in artifact_stats.items():
        total[stat] = total.get(stat, 0.0) + value

    return total


def calc_damage_preview_from_selected(
    character_name,
    build_name,
    selected_artifacts,
    overflow_mode="to_cd",
    overflow_ratio=1.0
):
    preview_base = build_damage_preview_base(character_name, build_name)
    artifact_stats = sum_selected_stats(selected_artifacts, include_mainstats=True)
    total_stats = merge_total_stats_for_damage_preview(
        preview_base["base_stats"],
        artifact_stats
    )

    dmg_bonus = preview_base["elemental_bonus"]
    elemental_bonus_type = preview_base.get("elemental_bonus_type")
    if elemental_bonus_type:
        dmg_bonus = total_stats.get(elemental_bonus_type, 0.0) if elemental_bonus_type else 0.0

    enemy = preview_base.get("default_enemy", {})
    enemy_level = enemy.get("level", 100)
    enemy_resistance = enemy.get("resistance", 10.0)
    talent_multiplier = preview_base.get("talent_multiplier", 100.0)
    base_crit_rate=preview_base["base_crit_rate"] - total_stats.get("会心率", 0.0),
    base_crit_damage=preview_base["base_crit_damage"] - total_stats.get("会心ダメージ", 0.0),
    damage_result = calc_damage_index(
        substats=total_stats,
        base_stat=preview_base["base_stat"],
        stat_type=preview_base["stat_type"],

        dmg_bonus=dmg_bonus,
        crit_rate_cap=preview_base["crit_rate_cap"],
        overflow_mode=overflow_mode,
        overflow_ratio=overflow_ratio,
        character_level=90,
        enemy_level=enemy_level,
        enemy_resistance=enemy_resistance,
        talent_multiplier=talent_multiplier
    )

    return {
        "preview_base": preview_base,
        "artifact_stats": artifact_stats,
        "total_stats": total_stats,
        "damage_result": damage_result
    }