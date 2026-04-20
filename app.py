import streamlit as st
import matplotlib.pyplot as plt
from simulator import (
    generate_artifact,
    run_multiple_simulations,
    run_character_simulation,
    character_builds,
    parts
)

st.set_page_config(
    page_title="聖遺物シミュレーター",
    layout="wide"
)

st.title("原神 聖遺物シミュレーター")
st.caption("1から厳選を始めた場合の、ざっくりした試行回数をシミュレートするツールです。")
st.caption("運試しモードと、厳選シミュモードを切り替えて使えます。")

mode = st.radio(
    "モードを選択",
    ["運試し", "かんたん診断", "シミュ"],
    horizontal=True
)

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

# =========================
# かんたん診断モード
# =========================
elif mode == "かんたん診断":
    st.subheader("かんたん診断")
    st.info("キャラを選ぶだけで、標準設定での厳選の目安をざっくり確認できます。")

    left_col, right_col = st.columns([1, 1.5])

    with left_col:
        st.markdown("### 設定")

        character_name = st.selectbox(
            "キャラを選択",
            list(character_builds.keys())
        )

        resin_per_day = st.number_input(
            "1日の樹脂消費量",
            min_value=20,
            max_value=400,
            value=160,
            step=20
        )

        trials = st.number_input(
            "シミュ回数",
            min_value=10,
            max_value=300,
            value=50,
            step=10,
            key="light_trials"
        )

        run_light = st.button("かんたん診断開始", use_container_width=True, type="primary")

        st.caption("1周あたり樹脂20で換算します。")
        st.caption("標準設定として、エリクシル・振り直しは既定値を使います。")

    with right_col:
        st.markdown("### 結果")

        if run_light:
            with st.spinner("計算中..."):
                result = run_character_simulation(
                    character_name=character_name,
                    trials=trials,
                    elixir_interval=250,
                    reroll_interval=1000,
                    reroll_times=10,
                    max_attempts=100000
                )

            st.markdown(f"#### {result['character']}｜{result['label']}（目標スコア {result['target_score']}）")

            st.write("**おすすめ構成**")
            st.write(result["mainstats"])

            if result["average"] is None:
                st.warning("この条件では最大試行回数内に到達しませんでした。")
            else:
                runs_per_day = resin_per_day / 20

                avg_days = result["average"] / runs_per_day
                top10_days = result["top10"] / runs_per_day
                bottom10_days = result["bottom10"] / runs_per_day

                metric_col1, metric_col2, metric_col3 = st.columns(3)
                metric_col1.metric("平均", f"{result['average']} 回")
                metric_col2.metric("上位10%", f"{result['top10']} 回")
                metric_col3.metric("下位10%", f"{result['bottom10']} 回")

                day_col1, day_col2, day_col3 = st.columns(3)
                day_col1.metric("平均日数", f"{avg_days:.1f} 日")
                day_col2.metric("上位10%日数", f"{top10_days:.1f} 日")
                day_col3.metric("下位10%日数", f"{bottom10_days:.1f} 日")

                if avg_days <= 14:
                    st.success("比較的現実的です")
                elif avg_days <= 30:
                    st.warning("少し重めです")
                else:
                    st.error("かなり重いです")

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

        # -------------------------
        # 単体シミュ
        # -------------------------
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
                metric_col3.metric("上位10%", result["top10"])
                metric_col4.metric("下位10%", result["bottom10"])

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

    # -------------------------
    # 比較シミュ
    # -------------------------
        elif mode == "かんたん診断":
            st.subheader("かんたん診断")

            st.info("キャラを選ぶだけで、標準設定での厳選の目安をざっくり確認できます。")

            left_col, right_col = st.columns([1, 1.5])

    # =====================
    # 左：設定
    # =====================
    with left_col:
        st.markdown("### 設定")

        character_name = st.selectbox(
            "キャラを選択",
            list(character_builds.keys())
        )

        build_names = list(character_builds[character_name]["builds"].keys())

        build_name = st.selectbox(
            "ビルドを選択",
            build_names
        )

        resin_per_day = st.number_input(
            "1日の樹脂消費量",
            min_value=0,
            max_value=300,
            value=180,
            step=20
        )

        trials = st.number_input(
            "シミュ回数",
            min_value=10,
            max_value=5000,
            value=50,
            step=10
        )

        run_light = st.button("目安を見る", use_container_width=True)

        st.caption("1周あたり樹脂20で換算します。")
        st.caption("エリクシル・振り直しは標準設定です。")
    # =====================
    # 右：結果
    # =====================
    with right_col:
        st.markdown("### 結果")

        if run_light:
            with st.spinner("計算中..."):
                result = run_character_simulation(
                    character_name=character_name,
                    build_name=build_name,
                    trials=trials,
                    elixir_interval=250,
                    reroll_interval=1000,
                    reroll_times=10,
                    max_attempts=100000
                )

            build = character_builds[character_name]

            # ===== キャラ情報 =====
            info_col1, info_col2, info_col3, info_col4 = st.columns(4)
            info_col1.metric("キャラ", result["character"])
            info_col2.metric("ビルド", result["build_name"])
            info_col3.metric("元素", result["element"])
            info_col4.metric("武器種", result["weapon"])
                st.markdown("---")

            # ===== おすすめ構成 =====
            with st.expander("おすすめ構成を見る"):
                st.write(result["mainstats"])

            if result["average"] is None:
                st.warning("この条件では最大試行回数内に到達しませんでした。")
            else:
                runs_per_day = resin_per_day / 20

                avg_days = result["average"] / runs_per_day
                top10_days = result["top10"] / runs_per_day
                bottom10_days = result["bottom10"] / runs_per_day

                # ===== 結論 =====
                st.markdown("#### 結論")

                day_col1, day_col2, day_col3 = st.columns(3)
                day_col1.metric("平均日数", f"{avg_days:.1f} 日")
                day_col2.metric("上位10%", f"{top10_days:.1f} 日")
                day_col3.metric("下位10%", f"{bottom10_days:.1f} 日")

                st.caption("樹脂20で1周換算")

                # ===== 一言評価 =====
                if avg_days <= 14:
                    st.success("比較的現実的です")
                elif avg_days <= 30:
                    st.warning("少し重めです")
                else:
                    st.error("かなり重いです")

                # ===== 詳細 =====
                with st.expander("詳細データを見る"):
                    detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                    detail_col1.metric("平均回数", f"{result['average']} 回")
                    detail_col2.metric("中央値", result["median"])
                    detail_col3.metric("上位10%回数", result["top10"])
                    detail_col4.metric("下位10%回数", result["bottom10"])

                # ===== グラフ =====
                st.markdown("#### 分布")
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
            st.info("左でキャラを選ぶと、平均日数の目安を表示します。")