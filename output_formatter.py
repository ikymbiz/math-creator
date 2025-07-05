import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import io
import base64
import os

class OutputFormatter:
    """問題の出力フォーマットとデザインを管理するクラス"""
    
    def __init__(self):
        self.initialize_default_styles()
        self.setup_japanese_fonts()
    
    def setup_japanese_fonts(self):
        """日本語フォントの設定"""
        import os
        import platform
        
        # 利用可能な日本語フォントのリスト
        japanese_fonts = [
            'HeiseiMin-W3',      # ReportLab標準
            'HeiseiKakuGo-W5',   # ReportLab標準（ゴシック体）
            'MS-Mincho',         # Windows標準
            'MS-Gothic',         # Windows標準（ゴシック体）
            'Yu-Mincho',         # Windows Vista以降
            'Yu-Gothic',         # Windows Vista以降（ゴシック体）
            'Hiragino-Mincho',   # macOS標準
            'Hiragino-Gothic',   # macOS標準（ゴシック体）
        ]
        
        # フォントを順番に試す
        for font_name in japanese_fonts:
            try:
                pdfmetrics.registerFont(UnicodeCIDFont(font_name))
                self.japanese_font = font_name
                self.japanese_bold_font = font_name
                st.success(f"✅ 日本語フォント（{font_name}）を使用します")
                return
            except Exception as e:
                continue
        
        # すべての日本語フォントが失敗した場合
        try:
            # 最後の手段として、ReportLabのデフォルト日本語フォントを試す
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
            self.japanese_font = 'HeiseiMin-W3'
            self.japanese_bold_font = 'HeiseiMin-W3'
            # st.info("ℹ️ デフォルトの日本語フォントを使用します")
        except Exception as e:
            # 最終フォールバック: 英語フォントを使用
            self.japanese_font = 'Helvetica'
            self.japanese_bold_font = 'Helvetica-Bold'
            st.warning(f"⚠️ 日本語フォントの設定に失敗しました。英語フォントを使用します。\nエラー詳細: {e}")
    
    def initialize_default_styles(self):
        """デフォルトのスタイル設定を初期化"""
        if 'output_styles' not in st.session_state:
            st.session_state.output_styles = {
                # PDF設定
                'pdf_title_font_size': 16,
                'pdf_table_font_size': 18,  # テーブルフォントサイズを14ptに固定
                'pdf_header_font_size': 14,  # ヘッダーフォントサイズを14ptに固定
                'pdf_margin': 20,
                'pdf_line_spacing': 1.2,
                
                # テーブル設定
                'table_header_bg_color': colors.grey,
                'table_header_text_color': colors.whitesmoke,
                'table_body_bg_color': colors.white,  # 背景色を白に変更
                'table_border_color': colors.black,
                'table_border_width': 1,
                
                # 表示設定
                'show_problem_numbers': True,
                'show_answers': True,
                'separate_answer_sheet': False,
                
                # フォント設定
                'font_family': 'HeiseiMin-W3',  # 日本語フォント（ReportLab標準）
                'bold_font_family': 'HeiseiMin-W3',  # 日本語太字フォント
                
                # A4印刷用レイアウト設定（1行66ピクセル想定）
                # A4幅: 210mm = 595.28ポイント
                # 余白を考慮して利用可能幅: 約550ポイント
                # 1行66ピクセル = 約50ポイント
                'column_widths': {
                    'problem_number': 80,    # 番号列
                    'problem': 210,          # 問題列
                    'answer_column': 120,    # 答え欄
                    'answer': 100            # 解答列
                },
                
                # 行の高さ設定
                'row_height':47,            # 行の高さ（ポイント）
                'header_row_height': 25,     # ヘッダー行の高さ（ポイント）
            }
    
    def create_pdf(self, problems_df, answers_df, settings):
        """PDFファイルを生成する関数"""
        buffer = io.BytesIO()
        # A4の上部と下部マージンを小さくする（デフォルトは72ポイント）
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30, bottomMargin=30, leftMargin=72, rightMargin=72)
        elements = []
        
        # スタイル設定
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=st.session_state.output_styles['pdf_title_font_size'],
            spaceAfter=10,  # タイトルの後の余白を小さく
            spaceBefore=0,  # タイトルの前の余白を0に
            alignment=0,  # 左揃え
            fontName=self.japanese_font  # 日本語フォントを使用
        )
        
        # 日付と時間のスタイル
        datetime_style = ParagraphStyle(
            'DateTime',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            spaceBefore=0,
            alignment=2,  # 右揃え
            fontName=self.japanese_font
        )
        
        # 現在の日付と時間を取得
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        
        # タイトルと日付を2列で表示
        title_table_data = [
            [Paragraph(settings['header_text'], title_style), 
             Paragraph(current_datetime, datetime_style)]
        ]
        
        # タイトルテーブルの列幅設定（左側にタイトル、右側に日付）
        title_col_widths = [400, 150]  # タイトル用に400ポイント、日付用に150ポイント
        
        title_table = Table(title_table_data, colWidths=title_col_widths)
        title_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # タイトルは左揃え
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # 日付は右揃え
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),  # 背景を白に
            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # グリッドを透明に
        ]))
        
        elements.append(title_table)
        elements.append(Spacer(1, 5))  # タイトルとテーブルの間隔を小さく
        
        # 問題テーブルの作成
        if settings['answer_display'] == 2:
            # 解答なしの場合
            if settings.get('show_answer_column', True):
                table_data = [['ばんごう', 'もんだい', 'こたえ']]
                for _, row in problems_df.iterrows():
                    # カラム名の存在確認
                    if 'ばんごう' in row and 'もんだい' in row and 'こたえ' in row:
                        table_data.append([str(row['ばんごう']), str(row['もんだい']), str(row['こたえ'])])
                    else:
                        st.error(f"カラム名が一致しません。期待: ['ばんごう', 'もんだい', 'こたえ'], 実際: {list(row.index)}")
                        return None
                # 列幅設定: 番号、問題、答え欄
                col_widths = [
                    st.session_state.output_styles['column_widths']['problem_number'],
                    st.session_state.output_styles['column_widths']['problem'],
                    st.session_state.output_styles['column_widths']['answer_column']
                ]
            else:
                table_data = [['ばんごう', 'もんだい']]
                for _, row in problems_df.iterrows():
                    # カラム名の存在確認
                    if 'ばんごう' in row and 'もんだい' in row:
                        table_data.append([str(row['ばんごう']), str(row['もんだい'])])
                    else:
                        st.error(f"カラム名が一致しません。期待: ['ばんごう', 'もんだい'], 実際: {list(row.index)}")
                        return None
                # 列幅設定: 番号、問題
                col_widths = [
                    st.session_state.output_styles['column_widths']['problem_number'],
                    st.session_state.output_styles['column_widths']['problem'] + st.session_state.output_styles['column_widths']['answer_column']
                ]
        else:
            # 解答ありの場合
            if settings.get('show_answer_column', True):
                table_data = [['ばんごう', 'もんだい', 'こたえ', 'せいかい']]
                for _, row in problems_df.iterrows():
                    # カラム名の存在確認
                    if 'ばんごう' in row and 'もんだい' in row and 'こたえ' in row and 'せいかい' in row:
                        table_data.append([str(row['ばんごう']), str(row['もんだい']), str(row['こたえ']), str(row['せいかい'])])
                    else:
                        st.error(f"カラム名が一致しません。期待: ['ばんごう', 'もんだい', 'こたえ', 'せいかい'], 実際: {list(row.index)}")
                        return None
                # 列幅設定: 番号、問題、答え欄、解答
                col_widths = [
                    st.session_state.output_styles['column_widths']['problem_number'],
                    st.session_state.output_styles['column_widths']['problem'],
                    st.session_state.output_styles['column_widths']['answer_column'],
                    st.session_state.output_styles['column_widths']['answer']
                ]
            else:
                table_data = [['ばんごう', 'もんだい', 'せいかい']]
                for _, row in problems_df.iterrows():
                    # カラム名の存在確認
                    if 'ばんごう' in row and 'もんだい' in row and 'せいかい' in row:
                        table_data.append([str(row['ばんごう']), str(row['もんだい']), str(row['せいかい'])])
                    else:
                        st.error(f"カラム名が一致しません。期待: ['ばんごう', 'もんだい', 'せいかい'], 実際: {list(row.index)}")
                        return None
                # 列幅設定: 番号、問題、解答
                col_widths = [
                    st.session_state.output_styles['column_widths']['problem_number'],
                    st.session_state.output_styles['column_widths']['problem'] + st.session_state.output_styles['column_widths']['answer_column'],
                    st.session_state.output_styles['column_widths']['answer']
                ]
        
        # テーブル作成（列幅を指定）
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), st.session_state.output_styles['table_header_bg_color']),
            ('TEXTCOLOR', (0, 0), (-1, 0), st.session_state.output_styles['table_header_text_color']),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.japanese_font),  # 日本語フォントを使用
            ('FONTSIZE', (0, 0), (-1, 0), st.session_state.output_styles['pdf_header_font_size']),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), st.session_state.output_styles['table_body_bg_color']),
            ('GRID', (0, 0), (-1, -1), st.session_state.output_styles['table_border_width'], st.session_state.output_styles['table_border_color']),
            ('FONTSIZE', (0, 1), (-1, -1), st.session_state.output_styles['pdf_table_font_size']),
            ('FONTNAME', (0, 1), (-1, -1), self.japanese_font),  # 日本語フォントを使用
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # 行の高さ設定
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, 0), st.session_state.output_styles['header_row_height'] // 2 - 6),  # ヘッダー行の高さ
            ('BOTTOMPADDING', (0, 0), (-1, 0), st.session_state.output_styles['header_row_height'] // 2 - 6),
            ('TOPPADDING', (0, 1), (-1, -1), st.session_state.output_styles['row_height'] // 2 - 6),  # 通常行の高さ
            ('BOTTOMPADDING', (0, 1), (-1, -1), st.session_state.output_styles['row_height'] // 2 - 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 10))  # テーブル下の余白を小さく
        
        # 解答が別シートの場合
        if settings['answer_display'] == 3 and answers_df is not None:
            # 改ページ
            elements.append(Spacer(1, 15))  # 改ページ前の余白を小さく
            
            # 解答タイトル
            answer_title = Paragraph("解答", title_style)
            elements.append(answer_title)
            elements.append(Spacer(1, 10))
            
            # 解答テーブル
            answer_data = [['もんだいばんごう', 'せいかい']]
            for _, row in answers_df.iterrows():
                # カラム名の存在確認
                if 'もんだいばんごう' in row and 'せいかい' in row:
                    answer_data.append([str(row['もんだいばんごう']), str(row['せいかい'])])
                else:
                    st.error(f"解答テーブルのカラム名が一致しません。期待: ['もんだいばんごう', 'せいかい'], 実際: {list(row.index)}")
                    return None
            
            # 解答テーブルの列幅設定
            answer_col_widths = [
                st.session_state.output_styles['column_widths']['problem_number'],
                st.session_state.output_styles['column_widths']['answer']
            ]
            
            answer_table = Table(answer_data, colWidths=answer_col_widths)
            answer_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), st.session_state.output_styles['table_header_bg_color']),
                ('TEXTCOLOR', (0, 0), (-1, 0), st.session_state.output_styles['table_header_text_color']),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), self.japanese_font),  # 日本語フォントを使用
                ('FONTSIZE', (0, 0), (-1, 0), st.session_state.output_styles['pdf_header_font_size']),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), st.session_state.output_styles['table_body_bg_color']),
                ('GRID', (0, 0), (-1, -1), st.session_state.output_styles['table_border_width'], st.session_state.output_styles['table_border_color']),
                ('FONTSIZE', (0, 1), (-1, -1), st.session_state.output_styles['pdf_table_font_size']),
                ('FONTNAME', (0, 1), (-1, -1), self.japanese_font),  # 日本語フォントを使用
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                # 行の高さ設定
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, 0), st.session_state.output_styles['header_row_height'] // 2 - 6),  # ヘッダー行の高さ
                ('BOTTOMPADDING', (0, 0), (-1, 0), st.session_state.output_styles['header_row_height'] // 2 - 6),
                ('TOPPADDING', (0, 1), (-1, -1), st.session_state.output_styles['row_height'] // 2 - 6),  # 通常行の高さ
                ('BOTTOMPADDING', (0, 1), (-1, -1), st.session_state.output_styles['row_height'] // 2 - 6),
            ]))
            
            elements.append(answer_table)
        
        # PDF生成
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def display_problems(self, problems_df, answers_df, settings):
        """問題を画面に表示する関数"""
        # st.markdown("---")
        st.header("📝 生成された問題")
        
        # 問題の表示
        if settings['answer_display'] == 1:
            # 解答あり
            if settings.get('show_answer_column', True):
                st.dataframe(
                    problems_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                display_df = problems_df.drop('こたえ', axis=1)
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
        elif settings['answer_display'] == 2:
            # 解答なし
            if settings.get('show_answer_column', True):
                display_df = problems_df.drop('せいかい', axis=1)
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                display_df = problems_df.drop(['せいかい', 'こたえ'], axis=1)
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
        else:
            # 別シート
            if settings.get('show_answer_column', True):
                display_df = problems_df.drop('せいかい', axis=1)
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                display_df = problems_df.drop(['せいかい', 'こたえ'], axis=1)
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            
            st.markdown("---")
            st.header("📋 解答")
            st.dataframe(
                answers_df,
                use_container_width=True,
                hide_index=True
            )
    
    def create_download_link(self, pdf_buffer, file_name):
        """ダウンロードリンクを作成する関数"""
        pdf_data = pdf_buffer.getvalue()
        b64_pdf = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{file_name}" target="_blank">💾 PDFをダウンロード</a>'
        return href, b64_pdf
    
    def create_auto_download_script(self, b64_pdf, file_name):
        """自動ダウンロードスクリプトを作成する関数"""
        script = f"""
        <script>
        setTimeout(function() {{
            var link = document.createElement('a');
            link.href = 'data:application/pdf;base64,{b64_pdf}';
            link.download = '{file_name}';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}, 1000);
        </script>
        """
        return script
    
    @property
    def styles(self):
        return st.session_state.output_styles 