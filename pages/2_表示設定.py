import streamlit as st
import sys
import os

# 親ディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import MathProblemGenerator
from display_settings import show_display_settings

st.set_page_config(
    page_title="表示設定 - けいさんドリル作成ツール",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🖨️ 表示設定")
    st.markdown("---")
    generator = MathProblemGenerator()
    generator.validate_slider_values()
    show_display_settings(generator)
    st.markdown("---")
    if st.button("🏠 メインページに戻る", use_container_width=True, key="back_to_main_display"):
        st.switch_page("main.py")

if __name__ == "__main__":
    main() 