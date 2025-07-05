import streamlit as st
from typing import Dict, Any
from display_settings import show_display_settings

def show_detailed_settings(generator):
    """詳細設定ページを表示"""

    # # 項数に応じた数値範囲の説明
    # st.info(f"💡 **現在の項数: {generator.settings['term_count']}項** - 数値範囲は項数に応じて調整されます。")
    
    # タブで設定を分離
    tab1, tab2, tab3 = st.tabs(["数値範囲", "制約設定", "表示設定"])
    
    with tab1:
        st.subheader("数値範囲設定")
        
        # 項数に応じた数値範囲の設定
        if generator.settings['term_count'] == 2:
            st.write("💡 **2項の場合**: 各演算で2つの数の範囲を設定します。")
        elif generator.settings['term_count'] == 3:
            st.write("💡 **3項の場合**: 各演算で3つの数の範囲を設定します。3番目の数は追加の数値範囲で設定されます。")
        elif generator.settings['term_count'] == 4:
            st.write("💡 **4項の場合**: 各演算で4つの数の範囲を設定します。3番目、4番目の数は追加の数値範囲で設定されます。")
        elif generator.settings['term_count'] == 5:
            st.write("💡 **5項の場合**: 各演算で5つの数の範囲を設定します。3番目、4番目、5番目の数は追加の数値範囲で設定されます。")
        
        # 足し算の範囲設定
        with st.expander("➕ 足し算の範囲設定", expanded=False):
            st.write("💡 **足し算の範囲設定について**\n\n"
                   "• **加数1**: 足し算の最初の数の範囲\n"
                   "• **加数2**: 足し算の2番目の数の範囲\n"
                   "• 例：3+5の場合、加数1は「3」、加数2は「5」")
            
            col1, col2 = st.columns(2)
            with col1:
                add_range1 = st.slider(
                    "加数1 範囲",
                    min_value=1,
                    max_value=20,
                    value=(generator.settings['add_min1'], generator.settings['add_max1']),
                    key="add_range1_slider"
                )
                generator.settings['add_min1'] = add_range1[0]
                generator.settings['add_max1'] = add_range1[1]
                st.caption(f"範囲: {generator.settings['add_min1']} ～ {generator.settings['add_max1']}")
                st.write("💡 **加数1**: 足し算の最初の数の範囲を設定します。例：3+5の「3」の部分。")
                
            with col2:
                add_range2 = st.slider(
                    "加数2 範囲",
                    min_value=1,
                    max_value=20,
                    value=(generator.settings['add_min2'], generator.settings['add_max2']),
                    key="add_range2_slider"
                )
                generator.settings['add_min2'] = add_range2[0]
                generator.settings['add_max2'] = add_range2[1]
                st.caption(f"範囲: {generator.settings['add_min2']} ～ {generator.settings['add_max2']}")
                st.write("💡 **加数2**: 足し算の2番目の数の範囲を設定します。例：3+5の「5」の部分。")
            
            # 3項以上の追加設定
            if generator.settings['term_count'] >= 3:
                st.markdown("---")
                st.write("**追加の数値範囲設定**")
                
                for i in range(3, generator.settings['term_count'] + 1):
                    add_range_extra = st.slider(
                        f"加数{i} 範囲",
                        min_value=1,
                        max_value=20,
                        value=(1, 10),
                        key=f"add_range{i}_slider"
                    )
                    # 追加の数値範囲を設定に保存（必要に応じて実装）
                    st.caption(f"範囲: {add_range_extra[0]} ～ {add_range_extra[1]}")
        
        # 引き算の範囲設定
        with st.expander("➖ 引き算の範囲設定", expanded=False):
            st.write("💡 **引き算の範囲設定について**\n\n"
                   "• **被減数**: 引き算で引かれる数の範囲\n"
                   "• **減数**: 引き算で引く数の範囲\n"
                   "• 例：7-3の場合、被減数は「7」、減数は「3」")
            
            col1, col2 = st.columns(2)
            with col1:
                sub_range1 = st.slider(
                    "被減数 範囲",
                    min_value=1,
                    max_value=20,
                    value=(generator.settings['sub_min1'], generator.settings['sub_max1']),
                    key="sub_range1_slider"
                )
                generator.settings['sub_min1'] = sub_range1[0]
                generator.settings['sub_max1'] = sub_range1[1]
                st.caption(f"範囲: {generator.settings['sub_min1']} ～ {generator.settings['sub_max1']}")
                st.write("💡 **被減数**: 引き算で引かれる数の範囲を設定します。例：7-3の「7」の部分。")
            with col2:
                sub_range2 = st.slider(
                    "減数 範囲",
                    min_value=1,
                    max_value=20,
                    value=(generator.settings['sub_min2'], generator.settings['sub_max2']),
                    key="sub_range2_slider"
                )
                generator.settings['sub_min2'] = sub_range2[0]
                generator.settings['sub_max2'] = sub_range2[1]
                st.caption(f"範囲: {generator.settings['sub_min2']} ～ {generator.settings['sub_max2']}")
                st.write("💡 **減数**: 引き算で引く数の範囲を設定します。例：7-3の「3」の部分。")
            
            # 3項以上の追加設定
            if generator.settings['term_count'] >= 3:
                st.markdown("---")
                st.write("**追加の数値範囲設定**")
                
                for i in range(3, generator.settings['term_count'] + 1):
                    sub_range_extra = st.slider(
                        f"減数{i} 範囲",
                        min_value=1,
                        max_value=20,
                        value=(1, 10),
                        key=f"sub_range{i}_slider"
                    )
                    st.caption(f"範囲: {sub_range_extra[0]} ～ {sub_range_extra[1]}")
        
        # かけ算の範囲設定
        with st.expander("✖️ かけ算の範囲設定", expanded=False):
            st.write("💡 **かけ算の範囲設定について**\n\n"
                   "• **乗数1**: かけ算の最初の数の範囲\n"
                   "• **乗数2**: かけ算の2番目の数の範囲\n"
                   "• 例：4×6の場合、乗数1は「4」、乗数2は「6」")
            
            col1, col2 = st.columns(2)
            with col1:
                mul_range1 = st.slider(
                    "乗数1 範囲",
                    min_value=1,
                    max_value=12,
                    value=(generator.settings['mul_min1'], generator.settings['mul_max1']),
                    key="mul_range1_slider"
                )
                generator.settings['mul_min1'] = mul_range1[0]
                generator.settings['mul_max1'] = mul_range1[1]
                st.caption(f"範囲: {generator.settings['mul_min1']} ～ {generator.settings['mul_max1']}")
                st.write("💡 **乗数1**: かけ算の最初の数の範囲を設定します。例：4×6の「4」の部分。")
            with col2:
                mul_range2 = st.slider(
                    "乗数2 範囲",
                    min_value=1,
                    max_value=12,
                    value=(generator.settings['mul_min2'], generator.settings['mul_max2']),
                    key="mul_range2_slider"
                )
                generator.settings['mul_min2'] = mul_range2[0]
                generator.settings['mul_max2'] = mul_range2[1]
                st.caption(f"範囲: {generator.settings['mul_min2']} ～ {generator.settings['mul_max2']}")
                st.write("💡 **乗数2**: かけ算の2番目の数の範囲を設定します。例：4×6の「6」の部分。")
            
            # 3項以上の追加設定
            if generator.settings['term_count'] >= 3:
                st.markdown("---")
                st.write("**追加の数値範囲設定**")
                
                for i in range(3, generator.settings['term_count'] + 1):
                    mul_range_extra = st.slider(
                        f"乗数{i} 範囲",
                        min_value=1,
                        max_value=12,
                        value=(1, 9),
                        key=f"mul_range{i}_slider"
                    )
                    st.caption(f"範囲: {mul_range_extra[0]} ～ {mul_range_extra[1]}")
        
        # わり算の範囲設定
        with st.expander("➗ わり算の範囲設定", expanded=False):
            st.write("💡 **わり算の範囲設定について**\n\n"
                   "• **被除数**: わり算で割られる数の範囲\n"
                   "• **除数**: わり算で割る数の範囲\n"
                   "• 例：12÷3の場合、被除数は「12」、除数は「3」")
            
            col1, col2 = st.columns(2)
            with col1:
                div_range1 = st.slider(
                    "被除数 範囲",
                    min_value=1,
                    max_value=50,
                    value=(generator.settings['div_min1'], generator.settings['div_max1']),
                    key="div_range1_slider"
                )
                generator.settings['div_min1'] = div_range1[0]
                generator.settings['div_max1'] = div_range1[1]
                st.caption(f"範囲: {generator.settings['div_min1']} ～ {generator.settings['div_max1']}")
                st.write("💡 **被除数**: わり算で割られる数の範囲を設定します。例：12÷3の「12」の部分。")
            with col2:
                div_range2 = st.slider(
                    "除数 範囲",
                    min_value=1,
                    max_value=12,
                    value=(generator.settings['div_min2'], generator.settings['div_max2']),
                    key="div_range2_slider"
                )
                generator.settings['div_min2'] = div_range2[0]
                generator.settings['div_max2'] = div_range2[1]
                st.caption(f"範囲: {generator.settings['div_min2']} ～ {generator.settings['div_max2']}")
                st.write("💡 **除数**: わり算で割る数の範囲を設定します。例：12÷3の「3」の部分。")
            
            # 3項以上の追加設定
            if generator.settings['term_count'] >= 3:
                st.markdown("---")
                st.write("**追加の数値範囲設定**")
                
                for i in range(3, generator.settings['term_count'] + 1):
                    div_range_extra = st.slider(
                        f"除数{i} 範囲",
                        min_value=1,
                        max_value=12,
                        value=(1, 9),
                        key=f"div_range{i}_slider"
                    )
                    st.caption(f"範囲: {div_range_extra[0]} ～ {div_range_extra[1]}")
    
    with tab2:
        st.subheader("🔒 制約設定")
        st.write("💡 **制約設定について**\n\n"
               "• **足し算の制限**: 答えの合計を制限して難易度を調整\n"
               "• **引き算の制限**: 答えが正の数になるかどうかを設定\n"
               "• **かけ算の制限**: 答えの積を制限して難易度を調整\n"
               "• **わり算の制限**: 余りがある問題を含めるかどうかを設定")
        
        add_limit = st.selectbox(
            "足し算の合計制限",
            options=[1, 2, 3],
            format_func=lambda x: {1: "10以下", 2: "11-20", 3: "制限なし"}[x],
            index=generator.settings['add_limit'] - 1
        )
        generator.settings['add_limit'] = add_limit
        st.write("💡 **足し算制限**: 足し算の答えの合計を制限します。10以下は簡単、11-20は中級、制限なしは上級レベルです。")
        
        sub_limit = st.selectbox(
            "引き算の解の制限",
            options=[1, 2],
            format_func=lambda x: {1: "正の整数", 2: "負の値もOK"}[x],
            index=generator.settings['sub_limit'] - 1
        )
        generator.settings['sub_limit'] = sub_limit
        st.write("💡 **引き算制限**: 引き算の答えが正の数になるかどうかを設定します。負の値もOKにすると、より難しい問題が生成されます。")
        
        mul_limit = st.selectbox(
            "かけ算の積の制限",
            options=[1, 2],
            format_func=lambda x: {1: "100以下", 2: "制限なし"}[x],
            index=generator.settings['mul_limit'] - 1
        )
        generator.settings['mul_limit'] = mul_limit
        st.write("💡 **かけ算制限**: かけ算の答えの積を制限します。100以下は九九レベル、制限なしは大きな数のかけ算になります。")
        
        div_limit = st.selectbox(
            "わり算の制限",
            options=[1, 2],
            format_func=lambda x: {1: "余りなし", 2: "余りあり"}[x],
            index=generator.settings['div_limit'] - 1
        )
        generator.settings['div_limit'] = div_limit
        st.write("💡 **わり算制限**: わり算で余りがある問題を含めるかどうかを設定します。余りなしは簡単、余りありは難しい問題になります。")
        
        # 値制限設定
        value_limit_enabled = st.selectbox(
            "解の値制限",
            options=[1, 2],
            format_func=lambda x: {1: "無効", 2: "有効"}[x],
            index=generator.settings['value_limit_enabled'] - 1
        )
        generator.settings['value_limit_enabled'] = value_limit_enabled
        st.write("💡 **値制限**: すべての演算の答えを指定した範囲に制限します。有効にすると、最小値と最大値を設定できます。")
        
        if generator.settings['value_limit_enabled'] == 2:
            value_range = st.slider(
                "解の値範囲",
                min_value=-50,
                max_value=100,
                value=(generator.settings['value_min'], generator.settings['value_max']),
                key="value_range_slider"
            )
            generator.settings['value_min'] = value_range[0]
            generator.settings['value_max'] = value_range[1]
            st.caption(f"範囲: {generator.settings['value_min']} ～ {generator.settings['value_max']}")
    
    with tab3:
        show_display_settings(generator) 