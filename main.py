import streamlit as st
import pandas as pd
import numpy as np
import random
from typing import List, Tuple, Dict, Any
from output_formatter import OutputFormatter

# ページ設定
st.set_page_config(
    page_title="けいさんドリル作成ツール",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

class MathProblemGenerator:
    def __init__(self):
        self.initialize_default_settings()
    
    def validate_slider_values(self):
        """スライダーの値の整合性をチェック"""
        settings = st.session_state.settings
        
        # 足し算の範囲チェック
        if settings['add_min1'] > settings['add_max1']:
            settings['add_max1'] = settings['add_min1']
        if settings['add_min2'] > settings['add_max2']:
            settings['add_max2'] = settings['add_min2']
        
        # 引き算の範囲チェック
        if settings['sub_min1'] > settings['sub_max1']:
            settings['sub_max1'] = settings['sub_min1']
        if settings['sub_min2'] > settings['sub_max2']:
            settings['sub_max2'] = settings['sub_min2']
        
        # かけ算の範囲チェック
        if settings['mul_min1'] > settings['mul_max1']:
            settings['mul_max1'] = settings['mul_min1']
        if settings['mul_min2'] > settings['mul_max2']:
            settings['mul_max2'] = settings['mul_min2']
        
        # わり算の範囲チェック
        if settings['div_min1'] > settings['div_max1']:
            settings['div_max1'] = settings['div_min1']
        if settings['div_min2'] > settings['div_max2']:
            settings['div_max2'] = settings['div_min2']
        
        # 値制限のチェック
        if settings['value_min'] > settings['value_max']:
            settings['value_max'] = settings['value_min']
    
    def initialize_default_settings(self):
        """デフォルト設定の初期化"""
        if 'settings' not in st.session_state:
            st.session_state.settings = {
                # 基本設定
                'problem_type': 1,  # 1:足し算, 2:引き算, 3:足し引き混合, 4:かけ算, 5:わり算, 6:四則混合
                'randomize_order': True,
                'question_count': 30,
                'term_count': 2,
                'generation_mode': 1,  # 1:通常モード, 2:網羅モード
                
                # 網羅設定
                'add_coverage': 1,  # 1:通常, 2:全組合せ
                'sub_coverage': 1,
                'mul_coverage': 1,
                'div_coverage': 1,
                
                # 数値範囲設定
                'add_min1': 1, 'add_max1': 10,
                'add_min2': 0, 'add_max2': 10,
                'sub_min1': 1, 'sub_max1': 10,
                'sub_min2': 1, 'sub_max2': 10,
                'mul_min1': 1, 'mul_max1': 9,
                'mul_min2': 1, 'mul_max2': 9,
                'div_min1': 1, 'div_max1': 81,
                'div_min2': 1, 'div_max2': 9,
                
                # 制約設定
                'add_limit': 1,  # 1:10以下, 2:11-20, 3:制限なし
                'sub_limit': 1,  # 1:正の整数, 2:負の値もOK
                'mul_limit': 1,  # 1:100以下, 2:制限なし
                'div_limit': 1,  # 1:余りなし, 2:余りあり
                'value_limit_enabled': 1,  # 1:無効, 2:有効
                'value_min': 0, 'value_max': 50,
                
                # 表示設定
                'answer_display': 1,  # 1:あり, 2:なし, 3:別シート
                'show_answer_column': True,  # 答え欄の表示
                'font_size': 14,  # フォントサイズを14ptに固定
                'header_text': "計算プリント",
                
                # 印刷設定
                'print_margin': 20,  # 印刷時の余白（mm）
                'print_columns': 2,  # 印刷時の列数
                'print_show_border': True,  # 枠線の表示
                'print_border_width': 1,  # 枠線の幅（px）
                'print_show_grid': False,  # グリッド線の表示
                'print_preview_mode': False,  # プレビューモード
            }
    
    def get_random_number(self, min_val: int, max_val: int) -> int:
        """指定された範囲の乱数生成"""
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        return random.randint(min_val, max_val)
    
    def generate_operands(self, operator: str) -> List[int]:
        """各演算子のオペランド生成"""
        nums = []
        for i in range(self.settings['term_count']):
            if operator == "+":
                if i == 0:
                    nums.append(self.get_random_number(self.settings['add_min1'], self.settings['add_max1']))
                else:
                    nums.append(self.get_random_number(self.settings['add_min2'], self.settings['add_max2']))
            elif operator == "-":
                if i == 0:
                    nums.append(self.get_random_number(self.settings['sub_min1'], self.settings['sub_max1']))
                else:
                    nums.append(self.get_random_number(self.settings['sub_min2'], self.settings['sub_max2']))
            elif operator == "*":
                if i == 0:
                    nums.append(self.get_random_number(self.settings['mul_min1'], self.settings['mul_max1']))
                else:
                    nums.append(self.get_random_number(self.settings['mul_min2'], self.settings['mul_max2']))
            elif operator == "/":
                if i == 0:
                    nums.append(self.get_random_number(self.settings['div_min1'], self.settings['div_max1']))
                else:
                    num = self.get_random_number(self.settings['div_min2'], self.settings['div_max2'])
                    nums.append(num if num != 0 else 1)
        return nums
    
    def adjust_div_operands(self, nums: List[int], operator: str) -> List[int]:
        """わり算の場合の被除数調整"""
        if operator != "/" or self.settings['div_limit'] != 1:
            return nums
        
        # 余りなしの場合、除数部分の積で被除数を調整
        product = 1
        for i in range(1, len(nums)):
            product *= nums[i]
        
        multiplier = self.get_random_number(
            max(1, self.settings['value_min'] // product),
            self.settings['value_max'] // product
        )
        nums[0] = product * multiplier
        if nums[0] == 0:
            nums[0] = product
        
        return nums
    
    def calculate_answer(self, nums: List[int], operator: str) -> Any:
        """計算結果の取得"""
        answer = nums[0]
        
        for i in range(1, len(nums)):
            if operator == "+":
                answer += nums[i]
            elif operator == "-":
                answer -= nums[i]
            elif operator == "*":
                answer *= nums[i]
            elif operator == "/":
                if nums[i] == 0:
                    return "ERROR"
                elif self.settings['div_limit'] == 1:
                    answer = answer / nums[i]
                else:
                    quotient = answer // nums[i]
                    remainder = answer % nums[i]
                    if remainder == 0:
                        answer = quotient
                    else:
                        answer = f"{quotient} 余り {remainder}"
        
        return answer
    
    def is_valid_question(self, answer: Any, operator: str) -> bool:
        """問題の妥当性チェック"""
        if answer == "ERROR":
            return False
        
        # 足し算の制約
        if operator == "+":
            if self.settings['add_limit'] == 1 and answer > 10:
                return False
            elif self.settings['add_limit'] == 2 and (answer <= 10 or answer > 20):
                return False
        
        # 引き算の制約
        elif operator == "-":
            if self.settings['sub_limit'] == 1 and answer <= 0:
                return False
        
        # かけ算の制約
        elif operator == "*":
            if self.settings['mul_limit'] == 1 and answer > 100:
                return False
        
        # 解の値制限
        if self.settings['value_limit_enabled'] == 2:
            try:
                numeric_value = float(answer)
                if numeric_value < self.settings['value_min'] or numeric_value > self.settings['value_max']:
                    return False
            except (ValueError, TypeError):
                return False
        
        return True
    
    def build_question_string(self, nums: List[int], operator: str) -> str:
        """問題文（文字列）の生成"""
        result = str(nums[0])
        for i in range(1, len(nums)):
            if operator == "+":
                result += f" + {nums[i]}"
            elif operator == "-":
                result += f" - {nums[i]}"
            elif operator == "*":
                result += f" × {nums[i]}"
            elif operator == "/":
                result += f" ÷ {nums[i]}"
        return result
    
    def format_vertical_equation(self, nums: List[int], operator: str) -> str:
        """問題文生成（横書き形式）"""
        return self.build_question_string(nums, operator)
    
    def generate_problems(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """問題生成メイン"""
        random.seed()
        
        problems = []
        answers = []
        used_questions = set()
        
        # 演算子リストの決定
        operator_map = {
            1: ["+"],
            2: ["-"],
            3: ["+", "-"],
            4: ["*"],
            5: ["/"],
            6: ["+", "-", "*", "/"]
        }
        operators = operator_map.get(self.settings['problem_type'], ["+"])
        
        # 網羅モードの処理
        for operator in operators:
            coverage_map = {
                "+": self.settings['add_coverage'],
                "-": self.settings['sub_coverage'],
                "*": self.settings['mul_coverage'],
                "/": self.settings['div_coverage']
            }
            
            if coverage_map.get(operator, 1) == 2:
                # 網羅的な全組み合わせ生成
                min_val = self.get_min_value(operator)
                max_val = self.get_max_value(operator)
                combinations = self.generate_combinations(min_val, max_val)
                
                for combo in combinations:
                    nums = combo.copy()
                    nums = self.adjust_div_operands(nums, operator)
                    answer = self.calculate_answer(nums, operator)
                    
                    if self.is_valid_question(answer, operator):
                        question = self.build_question_string(nums, operator)
                        if question not in used_questions:
                            used_questions.add(question)
                            problems.append({
                                'ばんごう': len(problems) + 1,
                                'もんだい': self.format_vertical_equation(nums, operator),
                                'こたえ': '',  # 生徒が記入する答え欄
                                'せいかい': answer
                            })
                            answers.append({
                                'もんだいばんごう': len(answers) + 1,
                                'せいかい': answer
                            })
        
        # 通常生成モード
        max_tries = 20000
        try_count = 0
        
        while len(problems) < self.settings['question_count'] and try_count < max_tries:
            try_count += 1
            
            # 演算子の選択
            if self.settings['problem_type'] == 3:
                operator = random.choice(["+", "-"])
            elif self.settings['problem_type'] == 6:
                operator = random.choice(["+", "-", "*", "/"])
            else:
                operator = operators[0]
            
            nums = self.generate_operands(operator)
            nums = self.adjust_div_operands(nums, operator)
            answer = self.calculate_answer(nums, operator)
            
            if not self.is_valid_question(answer, operator):
                continue
            
            question = self.build_question_string(nums, operator)
            if question not in used_questions:
                used_questions.add(question)
                problems.append({
                    'ばんごう': len(problems) + 1,
                    'もんだい': self.format_vertical_equation(nums, operator),
                    'こたえ': '',  # 生徒が記入する答え欄
                    'せいかい': answer
                })
                answers.append({
                    'もんだいばんごう': len(answers) + 1,
                    'せいかい': answer
                })
        
        # 順序設定の適用
        if self.settings['randomize_order']:
            # ランダム順序
            random.shuffle(problems)
            random.shuffle(answers)
        else:
            # 昇順（数値順）
            def extract_numbers(problem):
                import re
                numbers = re.findall(r'\d+', problem['もんだい'])
                return [int(n) for n in numbers]
            
            problems.sort(key=lambda x: extract_numbers(x))
            answers.sort(key=lambda x: extract_numbers(problems[x['もんだいばんごう']-1]))
        
        # 番号の再割り当て
        for i, problem in enumerate(problems):
            problem['ばんごう'] = i + 1
        for i, answer in enumerate(answers):
            answer['もんだいばんごう'] = i + 1
        
        return pd.DataFrame(problems), pd.DataFrame(answers)
    
    def get_min_value(self, operator: str) -> int:
        """最小値取得"""
        min_map = {
            "+": self.settings['add_min1'],
            "-": self.settings['sub_min1'],
            "*": self.settings['mul_min1'],
            "/": self.settings['div_min1']
        }
        return min_map.get(operator, 1)
    
    def get_max_value(self, operator: str) -> int:
        """最大値取得"""
        max_map = {
            "+": self.settings['add_max1'],
            "-": self.settings['sub_max1'],
            "*": self.settings['mul_max1'],
            "/": self.settings['div_max1']
        }
        return max_map.get(operator, 10)
    
    def generate_combinations(self, min_val: int, max_val: int) -> List[List[int]]:
        """組み合わせ生成"""
        combinations = []
        for i in range(min_val, max_val + 1):
            for j in range(min_val, max_val + 1):
                combinations.append([i, j])
        return combinations
    
    @property
    def settings(self) -> Dict[str, Any]:
        return st.session_state.settings



def main():
    st.title("🧮 けいさんドリル作成ツール")
    st.markdown("---")
    
    # ジェネレーターとフォーマッターの初期化
    generator = MathProblemGenerator()
    formatter = OutputFormatter()
    
    # バリデーション実行
    generator.validate_slider_values()
    
    # サイドバーに基本設定を配置
    with st.sidebar:
        st.header("⚙️ 基本設定")
        
        # 問題形式
        problem_type = st.selectbox(
            "問題形式",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: {
                1: "足し算", 2: "引き算", 3: "足し引き混合",
                4: "かけ算", 5: "わり算", 6: "四則混合"
            }[x],
            index=generator.settings['problem_type'] - 1
        )
        generator.settings['problem_type'] = problem_type
        st.caption("生成する問題の種類")
        
        # 項数（ドロップボックス）
        term_count = st.selectbox(
            "項数",
            options=[2, 3, 4, 5],
            index=generator.settings['term_count'] - 2,
            format_func=lambda x: f"{x}項"
        )
        generator.settings['term_count'] = term_count
        st.caption(f"1問あたりの項数")
        
        # 生成モード選択
        generation_mode = st.radio(
            "生成方法",
            options=[1, 2],
            format_func=lambda x: "通常モード" if x == 1 else "網羅モード",
            index=generator.settings.get('generation_mode', 1) - 1,
            key="generation_mode_sidebar_radio"
        )
        generator.settings['generation_mode'] = generation_mode
        
        if generation_mode == 1:
            # 通常の問題数設定
            question_count = st.slider(
                "問題数",
                min_value=10,
                max_value=100,
                value=generator.settings['question_count'],
                step=10,
                key="question_count_sidebar_slider"
            )
            generator.settings['question_count'] = question_count
            st.caption(f"{generator.settings['question_count']}問生成")
        else:
            st.caption("全組み合わせ生成")
        
        # 順序設定
        order_mode = st.radio(
            "問題の順序",
            options=[1, 2],
            format_func=lambda x: "昇順" if x == 1 else "ランダム",
            index=0 if not generator.settings.get('randomize_order', True) else 1,
            key="order_mode_sidebar_radio"
        )
        generator.settings['randomize_order'] = (order_mode == 2)
        
        if order_mode == 1:
            st.caption("数値の小さい順")
        else:
            st.caption("ランダムな順序")
        

        
        # 詳細設定ページへのリンク
        st.markdown("---")
        # st.subheader("🔗 ページリンク")
        
        if st.button("⚙️ 詳細設定ページ", use_container_width=True, key="go_to_detailed_settings"):
            st.session_state.show_detailed_settings = True
            st.rerun()
        # if st.button("🖨️ 表示設定ページ", use_container_width=True, key="go_to_display_settings"):
        #     st.session_state.show_display_settings = True
            # st.rerun()
        if st.button("📖 使い方ページ", use_container_width=True, key="go_to_usage_guide"):
            st.session_state.show_usage_guide = True
            st.rerun()
    
    # 詳細設定ページの表示制御
    if st.session_state.get('show_detailed_settings', False):
        # 詳細設定ページを表示
        st.header("⚙️ 詳細設定")
        # st.markdown("---")
        
        # 詳細設定を表示
        from detailed_settings import show_detailed_settings
        show_detailed_settings(generator)
        
        # 操作ボタン
        # st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 メインページに戻る", use_container_width=True, key="back_to_main"):
                st.session_state.show_detailed_settings = False
                st.rerun()
        
        with col2:
            if st.button("📊 設定をリセット", use_container_width=True, key="reset_settings_detail"):
                generator.initialize_default_settings()
                st.rerun()
    
    # 表示設定ページの表示制御
    elif st.session_state.get('show_display_settings', False):
        # 表示設定ページを表示
        st.header("🖨️ 表示設定")
        # st.markdown("---")
        
        # 表示設定を表示
        from display_settings import show_display_settings
        show_display_settings(generator)
        
        # 操作ボタン
        # st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 メインページに戻る", use_container_width=True, key="back_to_main_display"):
                st.session_state.show_display_settings = False
                st.rerun()
        
        with col2:
            if st.button("📊 設定をリセット", use_container_width=True, key="reset_settings_display"):
                generator.initialize_default_settings()
                st.rerun()
    
    # 使い方ページの表示制御
    elif st.session_state.get('show_usage_guide', False):
        # 使い方ページを表示
        from usage_guide import show_usage_guide
        show_usage_guide()
        
        # 操作ボタン
        # st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 メインページに戻る", use_container_width=True, key="back_to_main_usage"):
                st.session_state.show_usage_guide = False
                st.rerun()
        
        with col2:
            if st.button("📊 設定をリセット", use_container_width=True, key="reset_settings_usage"):
                generator.initialize_default_settings()
                st.rerun()
    
    else:
        # メインページ
        st.subheader("🎯 問題生成")
        
        # 操作ボタン
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 問題生成", type="primary", use_container_width=True, key="generate_problems_main"):
                with st.spinner("問題を生成中..."):
                    # 組み合わせ網羅モードの場合は問題数を十分大きく設定
                    if generator.settings['generation_mode'] == 2:
                        original_count = generator.settings['question_count']
                        generator.settings['question_count'] = 10000  # 十分大きな数
                    
                    problems_df, answers_df = generator.generate_problems()
                    
                    # 組み合わせ網羅モードの場合は実際の生成数を設定に反映
                    if generator.settings['generation_mode'] == 2:
                        generator.settings['question_count'] = len(problems_df)
                    
                    st.session_state.problems_df = problems_df
                    st.session_state.answers_df = answers_df
                    st.success(f"{len(problems_df)}問の問題が生成されました！")
                    
                    # PDFも同時に生成・ダウンロード
                    with st.spinner("PDFを生成中..."):
                        pdf_buffer = formatter.create_pdf(problems_df, answers_df, generator.settings)
                        
                        # PDFを自動ダウンロード
                        file_name = f"{generator.settings['header_text']}_{len(problems_df)}問.pdf"
                        href, b64_pdf = formatter.create_download_link(pdf_buffer, file_name)
                        
                        st.markdown(href, unsafe_allow_html=True)
                        
                        # 自動ダウンロードのJavaScript
                        script = formatter.create_auto_download_script(b64_pdf, file_name)
                        st.markdown(script, unsafe_allow_html=True)
        
        with col2:
            if st.button("📊 設定をリセット", use_container_width=True, key="reset_settings_main"):
                generator.initialize_default_settings()
                st.rerun()
        
        # st.markdown("---")
        
        # 問題の表示
        if 'problems_df' in st.session_state:
            formatter.display_problems(st.session_state.problems_df, st.session_state.answers_df, generator.settings)
        else:
            # st.info("👆 上記の「問題生成」ボタンをクリックして問題を生成してください。")
            
            # 現在の設定の表示
            st.subheader("📋 現在の設定")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("問題形式", {
                    1: "足し算", 2: "引き算", 3: "足し引き混合",
                    4: "かけ算", 5: "わり算", 6: "四則混合"
                }[generator.settings['problem_type']])
                st.metric("項数", f"{generator.settings['term_count']}項")
            
            with col2:
                st.metric("生成方法", "通常モード" if generator.settings['generation_mode'] == 1 else "網羅モード")
                st.metric("問題数", f"{generator.settings['question_count']}問")
            
            with col3:
                st.metric("順序", "昇順" if not generator.settings['randomize_order'] else "ランダム")
                st.metric("答え欄", "表示" if generator.settings.get('show_answer_column', True) else "非表示")
            
            # 列幅情報の表示
            if 'output_styles' in st.session_state:
                col_widths = st.session_state.output_styles['column_widths']
                total_width = sum(col_widths.values())
                # st.info(f"📏 **列幅設定**: 番号({col_widths['problem_number']}pt) + 問題({col_widths['problem']}pt) + 答え欄({col_widths['answer_column']}pt) + 解答({col_widths['answer']}pt) = {total_width}pt")
                
                if total_width > 550:
                    st.warning("⚠️ 列幅の合計が推奨値を超えています。表示設定ページで調整してください。")
                
                # 行の高さ情報
                row_height = st.session_state.output_styles['row_height']
                header_height = st.session_state.output_styles['header_row_height']
                # st.info(f"📏 **行の高さ設定**: 通常行({row_height}pt) + ヘッダー行({header_height}pt)")

    # 印刷用CSSスタイル
    st.markdown("""
    <style>
    @media print {
        .stApp {
            margin: 0;
            padding: 0;
        }
        .stDataFrame {
            page-break-inside: avoid;
        }
        .print-container {
            margin: 20mm;
            border: 1px solid black;
            padding: 10px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
