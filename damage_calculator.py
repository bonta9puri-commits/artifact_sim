"""Basic damage calculation skeleton for future extension.

このモジュールは、係数や補正を後から差し替えやすいように
関数を小さく分割した最小構成のダメージ計算ロジックです。
"""

from dataclasses import dataclass


@dataclass
class DamageInput:
    """入力パラメータをまとめるデータ構造。"""

    base_atk: float
    flat_atk: float
    atk_percent: float
    talent_multiplier: float
    dmg_bonus: float
    crit_rate: float
    crit_dmg: float
    enemy_def_multiplier: float
    enemy_res_multiplier: float
    reaction_multiplier: float


def clamp_crit_rate(crit_rate: float) -> float:
    """会心率を 0.0〜1.0 に丸める。"""
    return max(0.0, min(crit_rate, 1.0))


def calc_total_atk(base_atk: float, atk_percent: float, flat_atk: float) -> float:
    """総攻撃力を計算する。"""
    return base_atk * (1 + atk_percent) + flat_atk


def calc_base_damage(total_atk: float, talent_multiplier: float) -> float:
    """総攻撃力に天賦倍率を掛けた基礎ダメージを計算する。"""
    return total_atk * talent_multiplier


def apply_damage_bonus(base_damage: float, dmg_bonus: float) -> float:
    """ダメージバフを適用する。"""
    return base_damage * (1 + dmg_bonus)


def apply_enemy_and_reaction_multipliers(
    bonus_damage: float,
    enemy_def_multiplier: float,
    enemy_res_multiplier: float,
    reaction_multiplier: float,
) -> float:
    """敵防御・耐性・反応倍率を乗算する。

    将来的に防御無視、耐性低下、別枠乗算バフなどを
    分離して追加しやすいようにしている。
    """
    return (
        bonus_damage
        * enemy_def_multiplier
        * enemy_res_multiplier
        * reaction_multiplier
    )


def calc_noncrit_damage(
    total_atk: float,
    talent_multiplier: float,
    dmg_bonus: float,
    enemy_def_multiplier: float,
    enemy_res_multiplier: float,
    reaction_multiplier: float,
) -> float:
    """非会心ダメージを計算する。"""
    base_damage = calc_base_damage(total_atk, talent_multiplier)
    bonus_damage = apply_damage_bonus(base_damage, dmg_bonus)
    return apply_enemy_and_reaction_multipliers(
        bonus_damage,
        enemy_def_multiplier,
        enemy_res_multiplier,
        reaction_multiplier,
    )


def calc_crit_damage(final_noncrit: float, crit_dmg: float) -> float:
    """会心時ダメージを計算する。"""
    return final_noncrit * (1 + crit_dmg)


def calc_expected_damage(
    final_noncrit: float,
    crit_rate: float,
    crit_dmg: float,
) -> float:
    """期待値ダメージを計算する。"""
    safe_crit_rate = clamp_crit_rate(crit_rate)
    return final_noncrit * (1 + safe_crit_rate * crit_dmg)


def calc_damage_breakdown(params: DamageInput) -> dict[str, float]:
    """入力から非会心・会心・期待値を一括計算して返す。"""
    total_atk = calc_total_atk(
        params.base_atk,
        params.atk_percent,
        params.flat_atk,
    )

    final_noncrit = calc_noncrit_damage(
        total_atk=total_atk,
        talent_multiplier=params.talent_multiplier,
        dmg_bonus=params.dmg_bonus,
        enemy_def_multiplier=params.enemy_def_multiplier,
        enemy_res_multiplier=params.enemy_res_multiplier,
        reaction_multiplier=params.reaction_multiplier,
    )

    final_crit = calc_crit_damage(final_noncrit, params.crit_dmg)
    expected_damage = calc_expected_damage(
        final_noncrit,
        params.crit_rate,
        params.crit_dmg,
    )

    return {
        "total_atk": total_atk,
        "final_noncrit": final_noncrit,
        "final_crit": final_crit,
        "expected_damage": expected_damage,
        "clamped_crit_rate": clamp_crit_rate(params.crit_rate),
    }