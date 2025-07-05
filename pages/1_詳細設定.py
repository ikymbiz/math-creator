import streamlit as st
import sys
import os

# 親ディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import MathProblemGenerator
from detailed_settings import show_detailed_settings

# ページ設定
st.set_page_config(
    page_title="詳細設定 - 算数ドリル作成ツール",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # st.title("⚙️ 詳細設定")
    # st.markdown("---")
    
    # ジェネレーターの初期化
    generator = MathProblemGenerator()
    
    # バリデーション実行
    generator.validate_slider_values()
    
    # 詳細設定を表示
    show_detailed_settings(generator)
    
    # 操作ボタン
    # st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 メインページに戻る", use_container_width=True, key="back_to_main"):
            st.switch_page("main.py")
    
    with col2:
        if st.button("📊 設定をリセット", use_container_width=True, key="reset_settings_detail"):
            generator.initialize_default_settings()
            st.rerun()

if __name__ == "__main__":
    main() 