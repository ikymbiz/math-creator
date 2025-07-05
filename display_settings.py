import streamlit as st
from reportlab.lib.pagesizes import A4

def show_display_settings(generator):
    st.subheader("📄 表示設定")
    st.write("💡 **表示設定について**\n\n"
             "• **解答欄表示**: 解答を同じ画面に表示するか別にするか\n"
             "• **フォントサイズ**: 問題の文字サイズ\n"
             "• **ヘッダー文字**: 印刷時のページ上部に表示される文字")
    
    answer_display = st.selectbox(
        "解答欄表示",
        options=[1, 2, 3],
        format_func=lambda x: {1: "あり", 2: "なし", 3: "別シート"}[x],
        index=generator.settings['answer_display'] - 1
    )
    generator.settings['answer_display'] = answer_display
    st.write("💡 **解答欄表示**: 解答の表示方法を選択します。あり：同じ画面に表示、なし：解答を隠す、別シート：解答を別画面に表示。")
    
    show_answer_column = st.checkbox(
        "答え欄の表示",
        value=generator.settings.get('show_answer_column', True)
    )
    generator.settings['show_answer_column'] = show_answer_column
    st.write("💡 **答え欄の表示**: 生徒が答えを記入できる欄を表示します。チェックを外すと答え欄が非表示になります。")
    

    
    header_text = st.text_input(
        "ヘッダー文字",
        value=generator.settings['header_text'],
        key="header_text_detail_input"
    )
    generator.settings['header_text'] = header_text
    st.write("💡 **ヘッダー文字**: 印刷時のページ上部に表示されるタイトルを設定します。例：「計算プリント」「算数ドリル」など。")
    
    # A4印刷用の列幅設定
    st.markdown("---")
    st.subheader("📏 A4印刷用レイアウト設定")
    st.write("💡 **列幅設定**: A4印刷時の各列の幅を調整します。1行66ピクセルを想定しています。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        problem_number_width = st.slider(
            "番号列の幅 (ポイント)",
            min_value=20,
            max_value=80,
            value=st.session_state.output_styles['column_widths']['problem_number'],
            key="problem_number_width_slider"
        )
        st.session_state.output_styles['column_widths']['problem_number'] = problem_number_width
        
        problem_width = st.slider(
            "問題列の幅 (ポイント)",
            min_value=150,
            max_value=400,
            value=st.session_state.output_styles['column_widths']['problem'],
            key="problem_width_slider"
        )
        st.session_state.output_styles['column_widths']['problem'] = problem_width
    
    with col2:
        answer_column_width = st.slider(
            "答え欄の幅 (ポイント)",
            min_value=60,
            max_value=150,
            value=st.session_state.output_styles['column_widths']['answer_column'],
            key="answer_column_width_slider"
        )
        st.session_state.output_styles['column_widths']['answer_column'] = answer_column_width
        
        answer_width = st.slider(
            "解答列の幅 (ポイント)",
            min_value=60,
            max_value=150,
            value=st.session_state.output_styles['column_widths']['answer'],
            key="answer_width_slider"
        )
        st.session_state.output_styles['column_widths']['answer'] = answer_width
    
    # 合計幅の表示
    total_width = (problem_number_width + problem_width + answer_column_width + answer_width)
    st.info(f"📊 **合計幅**: {total_width}ポイント (推奨: 550ポイント以下)")
    
    if total_width > 550:
        st.warning("⚠️ 合計幅が推奨値を超えています。A4印刷時に列がはみ出る可能性があります。")
    
    # 行の高さ設定
    st.markdown("---")
    st.subheader("📏 行の高さ設定")
    st.write("💡 **行の高さ**: 印刷時の行の高さを調整します。大きくすると見やすくなりますが、1ページに表示できる問題数が減ります。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        row_height = st.slider(
            "通常行の高さ (ポイント)",
            min_value=20,
            max_value=50,
            value=st.session_state.output_styles['row_height'],
            key="row_height_slider"
        )
        st.session_state.output_styles['row_height'] = row_height
        st.caption(f"通常行の高さ: {row_height}ポイント")
    
    with col2:
        header_row_height = st.slider(
            "ヘッダー行の高さ (ポイント)",
            min_value=25,
            max_value=60,
            value=st.session_state.output_styles['header_row_height'],
            key="header_row_height_slider"
        )
        st.session_state.output_styles['header_row_height'] = header_row_height
        st.caption(f"ヘッダー行の高さ: {header_row_height}ポイント")
    
 