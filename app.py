import streamlit as st
import matplotlib.pyplot as plt
from simulator import (
    generate_artifact,
    run_multiple_simulations,
    run_character_simulation,
    build_selected_mainstats,
    run_custom_build_simulation,
    character_builds,
    parts,
    run_fixed_period_build_simulation
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

mode = st.radio(
    "モードを選択",
    ["運試し", "かんたん診断", "期間シミュ", "シミュ"],
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
        "max_attempts": st.session_state.get("preset_max_attempts", 100000)
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
            key="period_score_mode"
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
        st.caption("詳細設定でエリクシル・振り直しを変更できます。")
        st.caption("目安：180=実用 / 200=強い / 220+=ガチ")

    with right_col:
        st.markdown("### 結果")

        if run_light:
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
                    max_attempts=max_attempts
                )

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
                    reroll_times=reroll_times
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
            metric_col3.metric("良い側10%", f"{result['worst10']}")
            metric_col4.metric("沼側10%", f"{result['best10']}")

            with st.expander("使用条件とスコア式を見る"):
                st.write(f"**評価タイプ**: {score_mode}")
                st.write(f"**厳選日数**: {days}")
                st.write(f"**1日の樹脂消費量**: {resin_per_day}")
                st.write(f"**シミュ回数**: {trials}")
                st.write(f"**エリクシル使用間隔**: {elixir_interval}")
                st.write(f"**振り直し使用間隔**: {reroll_interval}")
                st.write(f"**振り直し1回の試行数**: {reroll_times}")
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

        else:
            st.info("左で条件を設定してシミュを開始してください。")

# =========================
# シミュモード
# =========================
elif mode == "シミュ":
    st.subheader("シミュモード")
    st.info("目標スコアに到達するまでに必要な試行回数をシミュレートします。")

    left_col, right_col = st.columns([1, 1.5])

    with left_col:
        st.markdown("### 設定")

        trials = st.number_input(
            "シミュ回数",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )

        elixir_interval = st.number_input(
            "エリクシル使用間隔（0で使用しない）",
            min_value=0,
            max_value=5000,
            value=250,
            step=50
        )

        reroll_interval = st.number_input(
            "振り直し使用間隔（0で使用しない）",
            min_value=0,
            max_value=10000,
            value=1000,
            step=100
        )

        reroll_times = st.number_input(
            "振り直し1回の試行数",
            min_value=1,
            max_value=100,
            value=10,
            step=1
        )

        max_attempts = st.number_input(
            "最大試行回数",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=1000
        )

        sim_mode = st.radio(
            "シミュの種類",
            ["単体シミュ", "比較シミュ（180 / 200 / 240）"]
        )

        if sim_mode == "単体シミュ":
            target_score = st.number_input(
                "目標合計スコア",
                min_value=50,
                max_value=2000,
                value=180,
                step=10
            )
            run_single = st.button("単体シミュ開始", use_container_width=True, type="primary")
            run_compare = False
        else:
            target_score = None
            run_compare = st.button("比較シミュ開始", use_container_width=True, type="primary")
            run_single = False

        st.caption("0にすると、そのアイテムは使わない設定になります。")

    with right_col:
        st.markdown("### 結果")

        if run_single:
            with st.spinner("計算中..."):
                result = run_multiple_simulations(
                    trials=trials,
                    target_score=target_score,
                    elixir_interval=elixir_interval,
                    reroll_interval=reroll_interval,
                    reroll_times=reroll_times,
                    max_attempts=max_attempts
                )

            success_col1, success_col2 = st.columns(2)
            success_col1.metric("成功回数", f"{result['success_count']} / {trials}")
            success_col2.metric("成功率", f"{result['success_rate'] * 100:.1f}%")

            if result["average"] is None:
                st.warning("この条件では最大試行回数内に到達しませんでした。")
            else:
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                metric_col1.metric("平均", result["average"])
                metric_col2.metric("中央値", result["median"])
                metric_col3.metric("良い方10%", result["best10"])
                metric_col4.metric("沼な10%", result["worst10"])

                fig, ax = plt.subplots()
                ax.hist(result["results"], bins=20)
                ax.axvline(result["average"], linestyle="--", label="平均")
                ax.axvline(result["median"], linestyle=":", label="中央値")
                ax.set_title("試行回数の分布")
                ax.set_xlabel("強化回数")
                ax.set_ylabel("件数")
                ax.legend()
                st.pyplot(fig)

                st.caption("右に長いほど、沼りやすい条件です。")

                with st.expander("試行回数一覧を見る"):
                    st.write(result["results"])

            st.caption("※シミュ結果は簡易モデルです。実際のゲーム内体感と完全一致するものではありません。")

        elif run_compare:
            compare_targets = [180, 200, 240]
            compare_results = []

            with st.spinner("計算中..."):
                for score in compare_targets:
                    result = run_multiple_simulations(
                        trials=trials,
                        target_score=score,
                        elixir_interval=elixir_interval,
                        reroll_interval=reroll_interval,
                        reroll_times=reroll_times,
                        max_attempts=max_attempts
                    )
                    compare_results.append((score, result))

            st.markdown("#### 比較結果")

            for score, result in compare_results:
                st.markdown(f"##### 目標スコア {score}")

                success_col1, success_col2 = st.columns(2)
                success_col1.metric("成功回数", f"{result['success_count']} / {trials}")
                success_col2.metric("成功率", f"{result['success_rate'] * 100:.1f}%")

                if result["average"] is None:
                    st.warning("この条件では最大試行回数内に到達しませんでした。")
                else:
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    metric_col1.metric("平均", result["average"])
                    metric_col2.metric("中央値", result["median"])
                    metric_col3.metric("良い方10%", result["best10"])
                    metric_col4.metric("沼な10%", result["worst10"])