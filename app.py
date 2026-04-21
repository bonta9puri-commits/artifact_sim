import streamlit as st
import matplotlib.pyplot as plt
from preset_utils import upsert_preset, get_preset, list_presets
from simulator import (
    generate_artifact,
    run_multiple_simulations,
    run_character_simulation,
    build_selected_mainstats,
    run_custom_build_simulation,
    character_builds,
    parts
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
    ["運試し", "かんたん診断", "シミュ"],
    horizontal=True
)


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
        score_mode = st.selectbox(
            "評価タイプ",
            score_mode_names,
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

            max_attempts = st.number_input(
                "最大試行回数",
                min_value=1000,
                max_value=10000000,
                value=100000,
                step=1000,
                key="preset_max_attempts"
            )

        st.markdown("### プリセット")

        light_presets = list_presets(mode="かんたん診断")
        light_preset_names = [""] + list(light_presets.keys())

        preset_name_input = st.text_input(
            "保存するプリセット名",
            key="light_preset_name_input"
        )

        preset_note_input = st.text_input(
            "メモ（任意）",
            key="light_preset_note_input"
        )

        selected_preset_name = st.selectbox(
            "保存済みプリセット",
            light_preset_names,
            key="selected_light_preset_name"
        )

        preset_save_col, preset_load_col = st.columns(2)

        with preset_save_col:
            if st.button("条件を保存", use_container_width=True):
                preset_name = preset_name_input.strip()
                if preset_name:
                    upsert_preset(
                        name=preset_name,
                        mode="かんたん診断",
                        data=build_light_preset_data(),
                        note=preset_note_input.strip()
                    )
                    st.success(f"プリセット「{preset_name}」を保存しました")
                else:
                    st.warning("プリセット名を入力してください")

        with preset_load_col:
            if st.button("読み込む", use_container_width=True):
                if selected_preset_name:
                    preset = get_preset(selected_preset_name)
                    if preset and preset.get("mode") == "かんたん診断":
                        apply_light_preset_data(preset.get("data", {}))
                        st.rerun()
                    else:
                        st.warning("読み込めるプリセットが見つかりませんでした")
                else:
                    st.warning("読み込むプリセットを選んでください")

        run_light = st.button("目安を見る", use_container_width=True, type="primary")

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

            st.caption("※比較シミュではグラフは省略しています。必要なら追加できます。")