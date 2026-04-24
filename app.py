import streamlit as st
import matplotlib.pyplot as plt
import urllib.parse
from simulator import (
    generate_artifact,
    run_multiple_simulations,
    run_character_simulation,
    build_selected_mainstats,
    run_custom_build_simulation,
    character_builds,
    parts,
    run_fixed_period_build_simulation,
    run_custom_build_preview,
    run_fixed_period_build_preview
)

st.set_page_config(
    page_title="原神 聖遺物厳選シミュレーター｜目標スコア到達回数を計算",
    layout="wide"
)

    
st.title("原神 聖遺物厳選シミュレーター")
st.markdown("""
原神の聖遺物厳選で、目標スコアに到達するまでの試行回数をシミュレーションできるツールです。
花・羽・時計・杯・冠の条件を指定して、厳選回数や平均日数の目安を確認できます。
""")
st.markdown("""
バグや不具合などやキャラが一部しかいないなどまだまだ完璧ではありませんがよろしくお願いします
""")
mode = st.radio(
    "モードを選択",
    ["運試し", "かんたん診断", "期間シミュ"],
    horizontal=True
)

def build_light_query_params():
    data = build_light_preset_data()
    return {
        "mode": "かんたん診断",
        "element_filter": data["element_filter"],
        "character_name": data["character_name"],
        "build_name": data["build_name"],
        "clock_choice": data["clock_choice"],
        "goblet_choice": data["goblet_choice"],
        "circlet_choice": data["circlet_choice"],
        "score_mode": data["score_mode"],
        "target_score": str(data["target_score"]),
        "resin_per_day": str(data["resin_per_day"]),
        "trials": str(data["trials"]),
        "elixir_interval": str(data["elixir_interval"]),
        "reroll_interval": str(data["reroll_interval"]),
        "reroll_times": str(data["reroll_times"]),
        "max_attempts": str(data["max_attempts"]),
        "strongbox_enabled": "1" if data["strongbox_enabled"] else "0",
        "strongbox_target_set": data["strongbox_target_set"],
    }


def apply_light_query_params():
    params = st.query_params

    if params.get("mode") != "かんたん診断":
        return

    st.session_state["preset_element_filter"] = params.get("element_filter", "すべて")
    st.session_state["preset_character_name"] = params.get("character_name", "")
    st.session_state["preset_build_name"] = params.get("build_name", "")
    st.session_state["preset_clock_choice"] = params.get("clock_choice", "")
    st.session_state["preset_goblet_choice"] = params.get("goblet_choice", "")
    st.session_state["preset_circlet_choice"] = params.get("circlet_choice", "")
    st.session_state["preset_score_mode"] = params.get("score_mode", "")
    st.session_state["preset_target_score"] = int(params.get("target_score", 180))
    st.session_state["preset_resin_per_day"] = int(params.get("resin_per_day", 180))
    st.session_state["preset_trials"] = int(params.get("trials", 50))
    st.session_state["preset_elixir_interval"] = int(params.get("elixir_interval", 0))
    st.session_state["preset_reroll_interval"] = int(params.get("reroll_interval", 0))
    st.session_state["preset_reroll_times"] = int(params.get("reroll_times", 1))
    st.session_state["preset_max_attempts"] = int(params.get("max_attempts", 100000))
    st.session_state["preset_strongbox_enabled"] = params.get("strongbox_enabled", "0") == "1"
    st.session_state["preset_strongbox_target_set"] = params.get("strongbox_target_set", "セット1")

def build_light_preset_data():
    return {
        "element_filter": st.session_state.get("preset_element_filter", "すべて"),
        "character_name": st.session_state.get("preset_character_name", ""),
        "build_name": st.session_state.get("preset_build_name", ""),
        "clock_choice": st.session_state.get("preset_clock_choice", ""),
        "goblet_choice": st.session_state.get("preset_goblet_choice", ""),
        "circlet_choice": st.session_state.get("preset_circlet_choice", ""),
        "score_mode": st.session_state.get("preset_score_mode", ""),
        "target_score": st.session_state.get("preset_target_score", 180),
        "resin_per_day": st.session_state.get("preset_resin_per_day", 180),
        "trials": st.session_state.get("preset_trials", 50),
        "elixir_interval": st.session_state.get("preset_elixir_interval", 0),
        "reroll_interval": st.session_state.get("preset_reroll_interval", 0),
        "reroll_times": st.session_state.get("preset_reroll_times", 1),
        "max_attempts": st.session_state.get("preset_max_attempts", 100000),
        "strongbox_enabled": st.session_state.get("preset_strongbox_enabled", False),
        "strongbox_target_set": st.session_state.get("preset_strongbox_target_set", "セット1")
    }


def apply_light_preset_data(data):
    st.session_state["preset_element_filter"] = data.get("element_filter", "すべて")
    st.session_state["preset_character_name"] = data.get("character_name", "")
    st.session_state["preset_build_name"] = data.get("build_name", "")
    st.session_state["preset_clock_choice"] = data.get("clock_choice", "")
    st.session_state["preset_goblet_choice"] = data.get("goblet_choice", "")
    st.session_state["preset_circlet_choice"] = data.get("circlet_choice", "")
    st.session_state["preset_score_mode"] = data.get("score_mode", "")
    st.session_state["preset_target_score"] = data.get("target_score", 180)
    st.session_state["preset_resin_per_day"] = data.get("resin_per_day", 180)
    st.session_state["preset_trials"] = data.get("trials", 50)
    st.session_state["preset_elixir_interval"] = data.get("elixir_interval", 0)
    st.session_state["preset_reroll_interval"] = data.get("reroll_interval", 0)
    st.session_state["preset_reroll_times"] = data.get("reroll_times", 1)
    st.session_state["preset_max_attempts"] = data.get("max_attempts", 100000)
    st.session_state["preset_strongbox_enabled"] = data.get("strongbox_enabled", False)
    st.session_state["preset_strongbox_target_set"] = data.get("strongbox_target_set", "セット1")

def build_current_gear_from_inputs(gear_inputs):
    current_gear = {}

    for part, data in gear_inputs.items():
        score = data["score"]
        artifact_set = data["set"]
        mainstat = data["main"]

        if score is None or score <= 0:
            continue

        current_gear[part] = {
            "部位": part,
            "セット": artifact_set,
            "メイン": mainstat,
            "スコア": score
        }

    return current_gear

def build_x_intent_url(text: str) -> str:
    return "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(text)


def build_light_result_post_text(
    character_name,
    build_name,
    score_mode,
    target_score,
    resin_per_day,
    result,
    elixir_interval=0,
    reroll_interval=0,
    reroll_times=1,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
):
    lines = [
        "聖遺物厳選シミュ結果",
        f"{character_name} / {build_name}",
        f"評価: {score_mode}",
        f"目標スコア: {target_score}",
    ]

    if result["average"] is None:
        lines.append("結果: 最大試行回数内に到達できませんでした")
    else:
        lines.extend([
            f"平均: {result['average']}回",
            f"中央値: {result['median']}回",
            f"良い側10%: {result['best10']}回",
            f"沼側10%: {result['worst10']}回",
            f"成功率: {result['success_rate'] * 100:.1f}%",
        ])

        if resin_per_day > 0:
            runs_per_day = resin_per_day / 20
            avg_days = result["average"] / runs_per_day
            lines.append(f"平均日数: {avg_days:.1f}日")

    option_text = []
    if elixir_interval > 0:
        option_text.append(f"エリクシル{elixir_interval}回ごと")
    if reroll_interval > 0:
        option_text.append(f"振り直し{reroll_interval}回ごと×{reroll_times}")
    if strongbox_enabled:
        option_text.append(f"廻聖あり({strongbox_target_set})")

    if option_text:
        lines.append("条件: " + " / ".join(option_text))

    lines.extend([
        "#原神",
        "#聖遺物",
    ])
    return "\n".join(lines)


def build_period_result_post_text(
    character_name,
    build_name,
    score_mode,
    days,
    resin_per_day,
    result,
    elixir_interval=0,
    reroll_interval=0,
    reroll_times=1,
    strongbox_enabled=False,
    strongbox_target_set="セット1"
):
    lines = [
        "聖遺物厳選シミュ結果",
        f"{character_name} / {build_name}",
        f"評価: {score_mode}",
        f"期間: {days}日",
        f"樹脂: 1日{resin_per_day}",
        f"総試行回数: {result['total_attempts']}回",
        f"平均スコア: {result['average']}",
        f"中央値: {result['median']}",
        f"良い側10%: {result['best10']}",
        f"沼側10%: {result['worst10']}",
    ]

    option_text = []
    if elixir_interval > 0:
        option_text.append(f"エリクシル{elixir_interval}回ごと")
    if reroll_interval > 0:
        option_text.append(f"振り直し{reroll_interval}回ごと×{reroll_times}")
    if strongbox_enabled:
        option_text.append(f"廻聖あり({strongbox_target_set})")

    if option_text:
        lines.append("条件: " + " / ".join(option_text))

    lines.extend([
        "#原神",
        "#聖遺物",
    ])
    return "\n".join(lines)



if "query_applied" not in st.session_state:
    apply_light_query_params()
    st.session_state["query_applied"] = True

# =========================
# 運試しモード
# =========================
if mode == "運試し":
    st.subheader("運試しモード")

    left_col, right_col = st.columns([1, 1.2])

    with left_col:
        st.markdown("### 設定")
        selected_part = st.selectbox("部位を選択", parts)
        generate_button = st.button("1個生成", use_container_width=True, type="primary")

    with right_col:
        st.markdown("### 結果")

        if generate_button:
            artifact = generate_artifact(selected_part)

            score = artifact["スコア"]
            if score >= 40:
                evaluation = "🔥 神引き"
                eval_type = "success"
            elif score >= 30:
                evaluation = "✨ 強い"
                eval_type = "info"
            elif score >= 20:
                evaluation = "🙂 まあまあ"
                eval_type = "warning"
            else:
                evaluation = "💀 厳しい"
                eval_type = "error"

            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("部位", artifact["部位"])
            metric_col2.metric("メイン", artifact["メイン"])
            metric_col3.metric("スコア", artifact["スコア"])

            if eval_type == "success":
                st.success(evaluation)
            elif eval_type == "info":
                st.info(evaluation)
            elif eval_type == "warning":
                st.warning(evaluation)
            else:
                st.error(evaluation)

            st.markdown("#### 初期サブ")
            st.write(artifact["初期サブ"])

            st.markdown("#### 最終サブ")
            st.write(artifact["サブ"])
        else:
            st.info("左で部位を選んで「1個生成」を押してください。")

    st.caption("簡易スコア: 会心率×2 + 会心ダメージ×1 + 攻撃%×1")



# =========================
# かんたん診断モード
# =========================
elif mode == "かんたん診断":
    st.subheader("かんたん診断")
    st.info("キャラを選ぶだけで、標準設定での厳選の目安をざっくり確認できます。")

    left_col, right_col = st.columns([1, 1.5])

    with left_col:
        st.markdown("### 設定")

        element_filter = st.selectbox(
            "元素で絞り込み",
            ["すべて", "炎", "水", "雷", "氷", "風", "岩", "草"],
            key="preset_element_filter"
        )

        if element_filter == "すべて":
            filtered_character_names = sorted(character_builds.keys())
        else:
            filtered_character_names = sorted(
                name for name, data in character_builds.items()
                if data.get("element") == element_filter
            )

        if not filtered_character_names:
            st.warning("この元素のキャラはまだ登録されていません。")
            st.stop()

        character_name = st.selectbox(
            "キャラを選択",
            filtered_character_names,
            key="preset_character_name"
        )

        build_names = list(character_builds[character_name]["builds"].keys())
        build_name = st.selectbox(
            "ビルドを選択",
            build_names,
            key="preset_build_name"
        )

        build_data = character_builds[character_name]["builds"][build_name]

        clock_choice = st.selectbox(
            "時計",
            build_data["mainstat_options"]["時計"],
            key="preset_clock_choice"
        )

        goblet_choice = st.selectbox(
            "杯",
            build_data["mainstat_options"]["杯"],
            key="preset_goblet_choice"
        )

        circlet_choice = st.selectbox(
            "冠",
            build_data["mainstat_options"]["冠"],
            key="preset_circlet_choice"
        )

        score_mode_names = list(build_data["score_weight_options"].keys())
        default_score_mode = build_data.get("default_score_mode", score_mode_names[0])
        default_score_index = score_mode_names.index(default_score_mode) if default_score_mode in score_mode_names else 0
        score_mode = st.selectbox(
           "評価タイプ",
            score_mode_names,
            index=default_score_index,
            key="preset_score_mode"
        )
        target_score = st.slider(
            "目標スコア",
            min_value=120,
            max_value=260,
            value=build_data["default_target_score"],
            step=10,
            key="preset_target_score"
        )

        resin_per_day = st.number_input(
            "1日の樹脂消費量",
            min_value=0,
            max_value=300,
            value=180,
            step=20,
            key="preset_resin_per_day"
        )

        trials = st.number_input(
            "シミュ回数",
            min_value=10,
            max_value=5000,
            value=50,
            step=10,
            key="preset_trials"
        )

        with st.expander("詳細設定"):
            elixir_interval = st.number_input(
                "エリクシル使用間隔（0で使用しない）",
                min_value=0,
                max_value=5000,
                value=0,
                step=50,
                key="preset_elixir_interval"
            )

            reroll_interval = st.number_input(
                "振り直し使用間隔（0で使用しない）",
                min_value=0,
                max_value=10000,
                value=0,
                step=100,
                key="preset_reroll_interval"
            )

            reroll_times = st.number_input(
                "振り直し1回の試行数",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                key="preset_reroll_times"
            )

            strongbox_enabled = st.checkbox(
                "廻聖を使う",
                value=False,
                key="preset_strongbox_enabled"
            )

            strongbox_target_set = st.selectbox(
                "廻聖の対象セット",
                ["セット1", "セット2"],
                key="preset_strongbox_target_set"
            )

            max_attempts = st.number_input(
                "最大試行回数",
                min_value=1000,
                max_value=10000000,
                value=100000,
                step=1000,
                key="preset_max_attempts"
            )

       
        run_light = st.button("目安を見る", use_container_width=True, type="primary")

        if st.button("共有URLを更新", use_container_width=True):
            st.query_params.clear()
            st.query_params.update(build_light_query_params())
            st.success("URLを更新しました。今のURLをそのまま共有できます。")

        st.caption("1周あたり樹脂20で換算します。")
        st.caption("詳細設定でエリクシル・振り直し・廻聖を変更できます。")
        st.caption("目安：180=実用 / 200=強い / 220+=ガチ")

    with right_col:
        st.markdown("### 結果")

        if run_light:
            preview_result = None

            selected_mainstats = build_selected_mainstats(
                build_data,
                clock_choice,
                goblet_choice,
                circlet_choice
            )

            with st.spinner("計算中..."):
                result = run_custom_build_simulation(
                    character_name=character_name,
                    build_name=build_name,
                    selected_mainstats=selected_mainstats,
                    score_mode=score_mode,
                    trials=trials,
                    target_score=target_score,
                    elixir_interval=elixir_interval,
                    reroll_interval=reroll_interval,
                    reroll_times=reroll_times,
                    max_attempts=max_attempts,
                    strongbox_enabled=strongbox_enabled,
                    strongbox_target_set=strongbox_target_set
                )

            preview_bundle = None
            preview_result = None

            if "damage_preview" in build_data:
                preview_bundle = run_custom_build_preview(
                    character_name=character_name,
                    build_name=build_name,
                    selected_mainstats=selected_mainstats,
                    score_mode=score_mode,
                    target_score=target_score,
                    elixir_interval=elixir_interval,
                    reroll_interval=reroll_interval,
                    reroll_times=reroll_times,
                    max_attempts=max_attempts,
                    strongbox_enabled=strongbox_enabled,
                    strongbox_target_set=strongbox_target_set
                )

                preview_result = preview_bundle["preview_result"] if preview_bundle else None

            st.markdown(
                f"#### {result['character']}｜{result['label']}（目標スコア {result['target_score']}）"
            )

            st.write("**おすすめ構成**")
            st.write(result["mainstats"])
            st.info("「共有URLを更新」を押すと、現在の条件をURLに反映できます。ブックマークや共有に使えます。")

            with st.expander("使用条件とスコア式を見る"):
                st.write(f"**評価タイプ**: {score_mode}")
                st.write(f"**目標スコア**: {target_score}")
                st.write(f"**1日の樹脂消費量**: {resin_per_day}")
                st.write(f"**シミュ回数**: {trials}")
                st.write(f"**エリクシル使用間隔**: {elixir_interval}")
                st.write(f"**振り直し使用間隔**: {reroll_interval}")
                st.write(f"**振り直し1回の試行数**: {reroll_times}")
                st.write(f"**廻聖を使う**: {'あり' if strongbox_enabled else 'なし'}")
                if strongbox_enabled:
                    st.write(f"**廻聖の対象セット**: {strongbox_target_set}")
                st.write(f"**最大試行回数**: {max_attempts}")

                weights = build_data["score_weight_options"][score_mode]
                score_text = " + ".join(
                    f"{stat}×{weight}" for stat, weight in weights.items() if weight != 0
                )
                st.write("**スコア式**")
                st.caption(score_text)

            success_col1, success_col2 = st.columns(2)
            success_col1.metric("成功回数", f"{len(result['results'])} / {trials}")
            success_col2.metric("成功率", f"{result['success_rate'] * 100:.1f}%")

            if result["average"] is None:
                st.warning("この条件では最大試行回数内に到達しませんでした。")
            else:
                runs_per_day = resin_per_day / 20 if resin_per_day > 0 else 0

                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                metric_col1.metric("平均", f"{result['average']} 回")
                metric_col2.metric("中央値", f"{result['median']} 回")
                metric_col3.metric("良い側10%", f"{result['best10']} 回")
                metric_col4.metric("沼側10%", f"{result['worst10']} 回")

                if runs_per_day > 0:
                    avg_days = result["average"] / runs_per_day
                    best10_days = result["best10"] / runs_per_day
                    worst10_days = result["worst10"] / runs_per_day

                    with st.expander("日数換算を見る"):
                        day_col1, day_col2, day_col3 = st.columns(3)
                        day_col1.metric("平均日数", f"{avg_days:.1f} 日")
                        day_col2.metric("良い側10%日数", f"{best10_days:.1f} 日")
                        day_col3.metric("沼側10%日数", f"{worst10_days:.1f} 日")

                    if avg_days <= 14:
                        st.success("比較的現実的です")
                    elif avg_days <= 30:
                        st.warning("少し重めです")
                    else:
                        st.error("かなり重いです")
                else:
                    st.info("1日の樹脂消費量が0のため、日数換算は表示できません。")

                fig, ax = plt.subplots()
                ax.hist(result["results"], bins=20)
                ax.axvline(result["average"], linestyle="--", label="平均")
                ax.axvline(result["median"], linestyle=":", label="中央値")
                ax.set_title(f"{result['character']} の試行回数分布")
                ax.set_xlabel("強化回数")
                ax.set_ylabel("件数")
                ax.legend()
                st.pyplot(fig)

                st.caption("右に長いほど、沼りやすい条件です。")

                if "damage_preview" not in build_data:
                    st.info("このキャラはまだダメージ比較βに対応していません。")
                elif preview_result is not None:
                    preview = preview_result["preview_base"]
                    total_stats = preview_result["total_stats"]
                    artifact_stats = preview_result["artifact_stats"]
                    damage = preview_result["damage_result"]
                    crit = damage["crit"]

                    st.markdown("#### 聖遺物比較β（試験表示）")

                    talent_name = preview.get("talent_name", "攻撃")
                    reaction_name = preview.get("reaction", "なし")
                    enemy_name = preview["default_enemy"].get("name", "敵")
                    enemy_level = preview["default_enemy"].get("level", "-")
                    enemy_res = preview["default_enemy"].get("resistance", 0)

                    st.caption(
                       f"{talent_name} / {enemy_name} Lv{enemy_level} / 耐性{enemy_res}% / 反応{reaction_name}"
                     )


                    stat_type = preview["stat_type"]

                    top1, top2, top3, top4 = st.columns(4)
                    with top1:
                        if stat_type == "HP":
                            st.metric("最終HP", f"{damage['final_stat']:.0f}")
                        elif stat_type == "攻撃":
                            st.metric("最終攻撃力", f"{damage['final_stat']:.0f}")
                        elif stat_type == "防御":
                            st.metric("最終防御力", f"{damage['final_stat']:.0f}")
                        else:
                            st.metric("最終参照ステ", f"{damage['final_stat']:.0f}")
                    with top2:
                            st.metric("非会心ダメージ", f"{damage['final_non_crit_index']:.0f}")
                    with top3:
                            st.metric("会心ダメージ", f"{damage['final_crit_index']:.0f}")
                    with top4:
                            st.metric("期待値ダメージ", f"{damage['final_expected_index']:.0f}")

                    mid1, mid2, mid3 = st.columns(3)
                    with mid1:
                        st.metric("会心率", f"{crit['total_cr']:.1f}%")
                        st.metric("実効会心率", f"{crit['effective_cr']:.1f}%")
                    with mid2:
                        st.metric("会心ダメ", f"{crit['total_cd']:.1f}%")
                        st.metric("補正後会心ダメ", f"{crit['adjusted_cd']:.1f}%")
                    with mid3:
                        st.metric("あふれ会心率", f"{crit['overflow_cr']:.1f}%")
                        elemental_bonus_type = preview.get("elemental_bonus_type")
                        if elemental_bonus_type:
                            st.metric(elemental_bonus_type, f"{total_stats.get(elemental_bonus_type, 0):.1f}%")
                        else:
                            st.metric("元素ダメバフ", "0.0%")

                    extra1, extra2, extra3 = st.columns(3)
                    with extra1:
                        st.write(f"HP%: {total_stats.get('HP%', 0):.1f}")
                    with extra2:
                        st.write(f"攻撃%: {total_stats.get('攻撃%', 0):.1f}")
                    with extra3:
                        st.write(f"防御%: {total_stats.get('防御%', 0):.1f}")

                    with st.expander("合計ステータスを見る"):
                        st.write(total_stats)

                    with st.expander("聖遺物サブ合計を見る"):
                        st.write(artifact_stats)

            post_text = build_light_result_post_text(
                character_name=character_name,
                build_name=build_name,
                score_mode=score_mode,
                target_score=target_score,
                resin_per_day=resin_per_day,
                result=result,
                elixir_interval=elixir_interval,
                reroll_interval=reroll_interval,
                reroll_times=reroll_times,
                strongbox_enabled=strongbox_enabled,
                strongbox_target_set=strongbox_target_set
            )

            st.markdown("#### 共有")
            share_col1, share_col2 = st.columns(2)

            with share_col1:
                st.code(post_text, language=None)
                st.caption("必要なら少し書き換えてからポストできます。")

            with share_col2:
                st.link_button(
                    "Xにポスト",
                    build_x_intent_url(post_text),
                    use_container_width=True
                )
                st.text_area(
                    "コピペ用テキスト",
                    value=post_text,
                    height=220,
                    key=f"light_post_text_{character_name}_{build_name}_{target_score}"
                )

            st.caption("※シミュ結果は簡易モデルです。実際のゲーム内体感と完全一致するものではありません。")

        else:
            st.info("左でキャラを選んで診断を開始してください。")

elif mode == "期間シミュ":
    st.subheader("期間シミュ")
    st.info("一定期間厳選したとき、どれくらいのスコアに届きそうかをシミュレーションします。")

    left_col, right_col = st.columns([1, 1.5])

    with left_col:
        st.markdown("### 設定")

        element_filter = st.selectbox(
            "元素で絞り込み",
            ["すべて", "炎", "水", "雷", "氷", "風", "岩", "草"],
            key="period_element_filter"
        )

        if element_filter == "すべて":
            filtered_character_names = sorted(character_builds.keys())
        else:
            filtered_character_names = sorted(
                name for name, data in character_builds.items()
                if data.get("element") == element_filter
            )

        if not filtered_character_names:
            st.warning("この元素のキャラはまだ登録されていません。")
            st.stop()

        character_name = st.selectbox(
            "キャラを選択",
            filtered_character_names,
            key="period_character_name"
        )

        build_names = list(character_builds[character_name]["builds"].keys())
        build_name = st.selectbox(
            "ビルドを選択",
            build_names,
            key="period_build_name"
        )

        build_data = character_builds[character_name]["builds"][build_name]

        clock_choice = st.selectbox(
            "時計",
            build_data["mainstat_options"]["時計"],
            key="period_clock_choice"
        )

        goblet_choice = st.selectbox(
            "杯",
            build_data["mainstat_options"]["杯"],
            key="period_goblet_choice"
        )

        circlet_choice = st.selectbox(
            "冠",
            build_data["mainstat_options"]["冠"],
            key="period_circlet_choice"
        )
        score_mode_names = list(build_data["score_weight_options"].keys())
        default_score_mode = build_data.get("default_score_mode", score_mode_names[0])
        default_score_index = score_mode_names.index(default_score_mode) if default_score_mode in score_mode_names else 0

        score_mode = st.selectbox(
            "評価タイプ",
            score_mode_names,
            index=default_score_index,
            key="period_score_mode"
        )

        days = st.number_input(
            "厳選日数",
            min_value=1,
            max_value=3650,
            value=180,
            step=30,
            key="period_days"
        )

        resin_per_day = st.number_input(
            "1日の樹脂消費量",
            min_value=0,
            max_value=300,
            value=180,
            step=20,
            key="period_resin_per_day"
        )

        trial_option = st.selectbox(
            "シミュ精度",
            ["軽量（100回）", "標準（300回）", "高精度（1000回）"],
            index=1,
            key="period_trial_option"
        )

        trial_map = {
            "軽量（100回）": 100,
            "標準（300回）": 300,
            "高精度（1000回）": 1000
        }

        trials = trial_map[trial_option]
        with st.expander("詳細設定"):
            elixir_interval = st.number_input(
                "エリクシル使用間隔（0で使用しない）",
                min_value=0,
                max_value=5000,
                value=0,
                step=50,
                key="period_elixir_interval"
            )

            reroll_interval = st.number_input(
                "振り直し使用間隔（0で使用しない）",
                min_value=0,
                max_value=10000,
                value=0,
                step=100,
                key="period_reroll_interval"
            )

            reroll_times = st.number_input(
                "振り直し1回の試行数",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                key="period_reroll_times"
            )

            strongbox_enabled = st.checkbox(
                "廻聖を使う",
                value=False,
                key="period_strongbox_enabled"
            )

            strongbox_target_set = st.selectbox(
                "廻聖の対象セット",
                ["セット1", "セット2"],
                key="period_strongbox_target_set"
            )
        with st.expander("現在使っている聖遺物を入力（任意）"):
            st.caption("各部位の現在スコアを入力すると、その装備を初期状態としてシミュします。0なら未入力扱いです。")
            st.caption("セット揃えたいほうをセット１、自由枠をセット２としてください。")
            current_gear_inputs = {}

            for part in parts:
                st.markdown(f"**{part}**")
                gear_col1, gear_col2, gear_col3 = st.columns(3)

                with gear_col1:
                    artifact_set = st.selectbox(
                        f"{part}のセット",
                        ["セット1", "セット2"],
                        key=f"current_gear_set_{part}"
                    )

                with gear_col2:
                    if part in ["花", "羽"]:
                        if part == "花":
                            main_choice = "HP"
                        else:
                            main_choice = "攻撃力"
                        st.text_input(
                            f"{part}のメイン",
                            value=main_choice,
                            disabled=True,
                            key=f"current_gear_main_display_{part}"
                        )
                    else:
                        main_choice = st.selectbox(
                            f"{part}のメイン",
                            build_data["mainstat_options"][part],
                            key=f"current_gear_main_{part}"
                        )

                with gear_col3:
                    score_value = st.number_input(
                        f"{part}の現在スコア",
                        min_value=0.0,
                        max_value=100.0,
                        value=0.0,
                        step=0.1,
                        key=f"current_gear_score_{part}"
                    )

                current_gear_inputs[part] = {
                    "set": artifact_set,
                    "main": main_choice,
                    "score": score_value
                }
        run_period = st.button("期間シミュ開始", use_container_width=True, type="primary")

        st.caption("1周あたり樹脂20で換算します。")
        st.caption("例：180日 × 180樹脂/日 → 1620回分の試行")
        st.caption("平均・中央値・上振れ/下振れの目安を確認できます。")

    with right_col:
        st.markdown("### 結果")

        if run_period:
            selected_mainstats = build_selected_mainstats(
                build_data,
                clock_choice,
                goblet_choice,
                circlet_choice
            )

            current_gear = build_current_gear_from_inputs(current_gear_inputs)

            with st.spinner("計算中..."):
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
                    current_gear=current_gear,
                    strongbox_enabled=strongbox_enabled,
                    strongbox_target_set=strongbox_target_set
                )

            st.markdown(
                f"#### {result['character']}｜{result['label']}（{result['days']}日）"
            )

            st.write("**おすすめ構成**")
            st.write(result["mainstats"])

            summary_col1, summary_col2 = st.columns(2)
            summary_col1.metric("総試行回数", f"{result['total_attempts']} 回")
            summary_col2.metric("シミュ回数", f"{trials} 回")

            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            metric_col1.metric("平均", f"{result['average']}")
            metric_col2.metric("中央値", f"{result['median']}")
            metric_col3.metric("下位10%", f"{result['lower10']}")
            metric_col4.metric("上位10%", f"{result['upper10']}")

            def show_artifact_set(title, record):
                st.markdown(f"#### {title}：合計スコア {record['score']}")

                selected_artifacts = record.get("selected_artifacts")

                if not selected_artifacts:
                    st.info("表示できる聖遺物セットがありません。")
                    return

                for part in parts:
                    artifact = selected_artifacts.get(part)

                    if artifact is None:
                        st.write(f"**{part}**：なし")
                        continue

                    with st.expander(
                        f"{part}｜{artifact.get('セット', '-')}｜{artifact.get('メイン', '-')}｜スコア {artifact.get('スコア', 0)}"
                    ):
                        st.write("**初期サブ**")
                        st.write(artifact.get("初期サブ", {}))

                        st.write("**最終サブ**")
                        st.write(artifact.get("サブ", {}))

            with st.expander("代表的な聖遺物セットを見る"):
                sample_artifacts = result.get("sample_artifacts", {})

                if not sample_artifacts:
                    st.info("代表聖遺物セットがありません。")
                else:
                    tab_lower, tab_avg, tab_median, tab_upper = st.tabs(
                        ["下位10%", "平均付近", "中央値", "上位10%"]
                    )

                    with tab_lower:
                        show_artifact_set("下位10%", sample_artifacts["下位10%"])

                    with tab_avg:
                        show_artifact_set("平均付近", sample_artifacts["平均付近"])

                    with tab_median:
                        show_artifact_set("中央値", sample_artifacts["中央値"])

                    with tab_upper:
                        show_artifact_set("上位10%", sample_artifacts["上位10%"])

            with st.expander("使用条件とスコア式を見る"):
                st.write(f"**評価タイプ**: {score_mode}")
                st.write(f"**厳選日数**: {days}")
                st.write(f"**1日の樹脂消費量**: {resin_per_day}")
                st.write(f"**シミュ回数**: {trials}")
                st.write(f"**エリクシル使用間隔**: {elixir_interval}")
                st.write(f"**振り直し使用間隔**: {reroll_interval}")
                st.write(f"**振り直し1回の試行数**: {reroll_times}")
                st.write(f"**廻聖を使う**: {'あり' if strongbox_enabled else 'なし'}")

                if strongbox_enabled:
                    st.write(f"**廻聖の対象セット**: {strongbox_target_set}")

                st.write(f"**総試行回数**: {result['total_attempts']}")

                if current_gear:
                    st.write("**現在装備入力**: あり")
                    st.write(current_gear)
                else:
                    st.write("**現在装備入力**: なし（0からシミュ）")

                weights = build_data["score_weight_options"][score_mode]
                score_text = " + ".join(
                    f"{stat}×{weight}" for stat, weight in weights.items() if weight != 0
                )
                st.write("**スコア式**")
                st.caption(score_text)

            fig, ax = plt.subplots()
            ax.hist(result["results"], bins=20)
            ax.axvline(result["average"], linestyle="--", label="平均")
            ax.axvline(result["median"], linestyle=":", label="中央値")
            ax.set_title(f"{result['character']} の最終スコア分布")
            ax.set_xlabel("最終合計スコア")
            ax.set_ylabel("件数")
            ax.legend()
            st.pyplot(fig)

            st.caption("右に長いほど、かなり上振れた結果です。")

            post_text = build_period_result_post_text(
                character_name=character_name,
                build_name=build_name,
                score_mode=score_mode,
                days=days,
                resin_per_day=resin_per_day,
                result=result,
                elixir_interval=elixir_interval,
                reroll_interval=reroll_interval,
                reroll_times=reroll_times,
                strongbox_enabled=strongbox_enabled,
                strongbox_target_set=strongbox_target_set
            )

            st.markdown("#### 共有")
            share_col1, share_col2 = st.columns(2)

            with share_col1:
                st.code(post_text, language=None)
                st.caption("必要なら少し書き換えてからポストできます。")

            with share_col2:
                st.link_button(
                    "Xにポスト",
                    build_x_intent_url(post_text),
                    use_container_width=True
                )
                st.text_area(
                    "コピペ用テキスト",
                    value=post_text,
                    height=220,
                    key=f"period_post_text_{character_name}_{build_name}_{days}"
                )

        else:
            st.info("左で条件を設定してシミュを開始してください。")
with st.sidebar:
    st.markdown("---")
    st.subheader("📺 公式YouTube")
    st.link_button("チャンネル登録で応援する", "https://www.youtube.com/channel/UC_-uyn7NeDPhBqxFEQ8gLwQ" )
    
    st.markdown("---")
    st.subheader("💬 フィードバック")
    st.write("新キャラの追加依頼や不具合報告、応援メッセージはこちらから！")
    st.link_button("要望・不具合報告を送る", "https://forms.gle/GSHPqzZwYCJ6xq1s7" )