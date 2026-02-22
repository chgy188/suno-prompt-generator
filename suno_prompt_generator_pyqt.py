"""
Suno AI Prompt Generator - PyQt6版本
基于SUNO提示词清单PDF生成AI音乐提示词
使用PyQt6实现现代化UI
"""

import sys
import json
import os

# 隐藏控制台窗口（仅Windows）
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QScrollArea, QLabel, QLineEdit, QComboBox,
    QPushButton, QTextEdit, QCheckBox, QFrame, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette


# 现代深色主题配色
COLORS = {
    'bg': '#2B2B2B',
    'bg_light': '#3B3B3B',
    'bg_input': '#4B4B4B',
    'text': '#E0E0E0',
    'text_muted': '#A0A0A0',
    'accent': '#4CAF50',
    'accent_hover': '#45A049',
    'border': '#555555',
    'highlight': '#6B6B6B',
}

# 字体配置（使用较大字体）
FONTS = {
    'default': QFont('Microsoft YaHei UI', 12),
    'label': QFont('Microsoft YaHei UI', 12),
    'checkbox': QFont('Microsoft YaHei UI', 11),
    'button': QFont('Microsoft YaHei UI', 12),
    'title': QFont('Microsoft YaHei UI', 14, QFont.Weight.Bold),
    'input': QFont('Microsoft YaHei UI', 12),
    'card_title': QFont('Microsoft YaHei UI', 11, QFont.Weight.Bold),
    'card_desc': QFont('Microsoft YaHei UI', 10),
}


def load_suno_data():
    """从suno_data.json加载数据"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, 'suno_data.json')
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data['data']
    except FileNotFoundError:
        QMessageBox.critical(None, "错误", "找不到suno_data.json文件")
        sys.exit(1)
    except json.JSONDecodeError as e:
        QMessageBox.critical(None, "错误", f"JSON文件格式错误: {e}")
        sys.exit(1)
    except Exception as e:
        QMessageBox.critical(None, "错误", f"加载数据失败: {e}")
        sys.exit(1)


# 加载数据
SUNO_DATA = load_suno_data()

# 提取各类数据
GENRE_TAGS = SUNO_DATA['genres']
TEMPO_TAGS = SUNO_DATA['tempos']
STYLE_TAGS = SUNO_DATA['styles']
INSTRUMENT_TAGS = SUNO_DATA['instruments']
LYRICS_PROMPTS = SUNO_DATA['lyrics_prompts']
STRUCTURE_PROMPTS = SUNO_DATA['structure_prompts']
DANCE_PROMPTS = SUNO_DATA['dance_prompts']

# 获取分类
LYRICS_CATEGORIES = sorted(list(set(item["category"] for item in LYRICS_PROMPTS)))
STRUCTURE_CATEGORIES = sorted(list(set(item["category"] for item in STRUCTURE_PROMPTS)))


def set_dark_theme(app):
    """设置深色主题"""
    app.setStyle("Fusion")
    
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS['bg']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS['bg_input']))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS['bg_light']))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(COLORS['bg']))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS['bg_light']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Link, QColor(COLORS['accent']))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS['accent']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor('#FFFFFF'))
    
    app.setPalette(palette)


class TabContentWidget(QWidget):
    """标签页内容基类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # 控制区域
        self.control_frame = QFrame()
        self.control_layout = QHBoxLayout(self.control_frame)
        self.layout.addWidget(self.control_frame)
        
        # 显示区域（带滚动条）
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)
    
    def clear_content(self):
        """清空内容"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class GenreTab(TabContentWidget):
    """风格选择标签页"""
    
    def __init__(self, parent=None, selection_changed_callback=None):
        super().__init__(parent)
        self.selection_changed_callback = selection_changed_callback
        self.selected_genres = set()
        
        # 添加控制元素
        label = QLabel("选择字母:")
        label.setFont(FONTS['label'])
        self.control_layout.addWidget(label)
        
        self.combo = QComboBox()
        self.combo.setFont(FONTS['input'])
        self.combo.addItems(list(GENRE_TAGS.keys()))
        self.combo.setCurrentText("A")
        self.combo.setMinimumWidth(100)
        self.combo.currentTextChanged.connect(self.on_letter_changed)
        self.control_layout.addWidget(self.combo)
        
        self.control_layout.addSpacing(20)
        
        search_label = QLabel("搜索:")
        search_label.setFont(FONTS['label'])
        self.control_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setFont(FONTS['input'])
        self.search_input.setPlaceholderText("搜索风格...")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.on_search)
        self.control_layout.addWidget(self.search_input)
        
        # 显示所有风格
        self.show_genre_tags("A")
    
    def on_letter_changed(self, letter):
        """字母改变时更新显示"""
        self.search_input.clear()
        self.show_genre_tags(letter)
    
    def on_search(self, text):
        """搜索风格"""
        self.clear_content()
        
        search_text = text.lower()
        if not search_text:
            self.show_genre_tags(self.combo.currentText())
            return
        
        found_tags = []
        for letter, tags in GENRE_TAGS.items():
            for en, zh in tags:
                if search_text in en.lower() or search_text in zh.lower():
                    found_tags.append((en, zh))
        
        for en, zh in found_tags:
            self.add_genre_checkbox(en, zh)
        
        if not found_tags:
            no_result_label = QLabel("未找到匹配的标签")
            no_result_label.setFont(FONTS['label'])
            self.content_layout.addWidget(no_result_label)
    
    def show_genre_tags(self, letter):
        """显示指定字母的风格"""
        self.clear_content()
        
        if letter in GENRE_TAGS:
            for en, zh in GENRE_TAGS[letter]:
                self.add_genre_checkbox(en, zh)
    
    def add_genre_checkbox(self, en, zh):
        """添加风格复选框"""
        checkbox = QCheckBox(f"{en} - {zh}")
        checkbox.setFont(FONTS['checkbox'])
        checkbox.setChecked(en in self.selected_genres)
        checkbox.stateChanged.connect(
            lambda state, e=en: self.toggle_genre(e, state)
        )
        self.content_layout.addWidget(checkbox)
    
    def toggle_genre(self, genre, state):
        """切换风格选择"""
        if state == 2:
            self.selected_genres.add(genre)
        else:
            self.selected_genres.discard(genre)
        
        if self.selection_changed_callback:
            self.selection_changed_callback()


class TempoTab(TabContentWidget):
    """节奏选择标签页"""
    
    def __init__(self, parent=None, selection_changed_callback=None):
        super().__init__(parent)
        self.selection_changed_callback = selection_changed_callback
        self.selected_tempos = set()
        
        # 添加控制元素
        label = QLabel("选择速度:")
        label.setFont(FONTS['label'])
        self.control_layout.addWidget(label)
        
        self.combo = QComboBox()
        self.combo.setFont(FONTS['input'])
        self.combo.addItems(list(TEMPO_TAGS.keys()))
        self.combo.setMinimumWidth(150)
        self.combo.currentTextChanged.connect(self.on_category_changed)
        self.control_layout.addWidget(self.combo)
        
        # 显示所有节奏
        self.show_tempo_tags(list(TEMPO_TAGS.keys())[0])
    
    def on_category_changed(self, category):
        """分类改变时更新显示"""
        self.show_tempo_tags(category)
    
    def show_tempo_tags(self, category):
        """显示指定分类的节奏"""
        self.clear_content()
        
        if category in TEMPO_TAGS:
            for en, zh in TEMPO_TAGS[category]:
                self.add_tempo_checkbox(en, zh)
    
    def add_tempo_checkbox(self, en, zh):
        """添加节奏复选框"""
        checkbox = QCheckBox(f"{en} - {zh}")
        checkbox.setFont(FONTS['checkbox'])
        checkbox.setChecked(en in self.selected_tempos)
        checkbox.stateChanged.connect(
            lambda state, e=en: self.toggle_tempo(e, state)
        )
        self.content_layout.addWidget(checkbox)
    
    def toggle_tempo(self, tempo, state):
        """切换节奏选择"""
        if state == 2:
            self.selected_tempos.add(tempo)
        else:
            self.selected_tempos.discard(tempo)
        
        if self.selection_changed_callback:
            self.selection_changed_callback()


class StyleTab(TabContentWidget):
    """描述选择标签页"""
    
    def __init__(self, parent=None, selection_changed_callback=None):
        super().__init__(parent)
        self.selection_changed_callback = selection_changed_callback
        self.selected_styles = set()
        
        # 添加控制元素
        label = QLabel("选择类别:")
        label.setFont(FONTS['label'])
        self.control_layout.addWidget(label)
        
        self.combo = QComboBox()
        self.combo.setFont(FONTS['input'])
        self.combo.addItems(list(STYLE_TAGS.keys()))
        self.combo.setMinimumWidth(180)
        self.combo.currentTextChanged.connect(self.on_category_changed)
        self.control_layout.addWidget(self.combo)
        
        # 显示所有描述
        self.show_style_tags(list(STYLE_TAGS.keys())[0])
    
    def on_category_changed(self, category):
        """分类改变时更新显示"""
        self.show_style_tags(category)
    
    def show_style_tags(self, category):
        """显示指定分类的描述"""
        self.clear_content()
        
        if category in STYLE_TAGS:
            for en, zh in STYLE_TAGS[category]:
                self.add_style_checkbox(en, zh)
    
    def add_style_checkbox(self, en, zh):
        """添加描述复选框"""
        checkbox = QCheckBox(f"{en} - {zh}")
        checkbox.setFont(FONTS['checkbox'])
        checkbox.setChecked(en in self.selected_styles)
        checkbox.stateChanged.connect(
            lambda state, e=en: self.toggle_style(e, state)
        )
        self.content_layout.addWidget(checkbox)
    
    def toggle_style(self, style, state):
        """切换描述选择"""
        if state == 2:
            self.selected_styles.add(style)
        else:
            self.selected_styles.discard(style)
        
        if self.selection_changed_callback:
            self.selection_changed_callback()


class InstrumentTab(TabContentWidget):
    """乐器选择标签页"""
    
    def __init__(self, parent=None, selection_changed_callback=None):
        super().__init__(parent)
        self.selection_changed_callback = selection_changed_callback
        self.selected_instruments = set()
        
        # 移除控制框架（乐器不需要筛选）
        self.control_frame.deleteLater()
        
        # 显示所有乐器
        self.show_instruments()
    
    def show_instruments(self):
        """显示所有乐器"""
        for en, zh in INSTRUMENT_TAGS:
            self.add_instrument_checkbox(en, zh)
    
    def add_instrument_checkbox(self, en, zh):
        """添加乐器复选框"""
        checkbox = QCheckBox(f"{en} - {zh}")
        checkbox.setFont(FONTS['checkbox'])
        checkbox.setChecked(en in self.selected_instruments)
        checkbox.stateChanged.connect(
            lambda state, e=en: self.toggle_instrument(e, state)
        )
        self.content_layout.addWidget(checkbox)
    
    def toggle_instrument(self, instrument, state):
        """切换乐器选择"""
        if state == 2:
            self.selected_instruments.add(instrument)
        else:
            self.selected_instruments.discard(instrument)
        
        if self.selection_changed_callback:
            self.selection_changed_callback()


class BonusTab(TabContentWidget):
    """附加提示词标签页"""
    
    def __init__(self, parent=None, selection_changed_callback=None):
        super().__init__(parent)
        self.selection_changed_callback = selection_changed_callback
        self.selected_lyrics = set()
        self.current_page = 1
        self.items_per_page = 10
        self.current_data = []
        self.current_category = "All"
        
        # 添加控制元素
        search_label = QLabel("搜索:")
        search_label.setFont(FONTS['label'])
        self.control_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setFont(FONTS['input'])
        self.search_input.setPlaceholderText("搜索提示词...")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.on_search)
        self.control_layout.addWidget(self.search_input)
        
        self.control_layout.addSpacing(20)
        
        category_label = QLabel("分类:")
        category_label.setFont(FONTS['label'])
        self.control_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.setFont(FONTS['input'])
        categories = ["All"] + LYRICS_CATEGORIES
        self.category_combo.addItems(categories)
        self.category_combo.setMinimumWidth(150)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        self.control_layout.addWidget(self.category_combo)
        
        # 分页控制
        self.page_frame = QFrame()
        self.page_layout = QHBoxLayout(self.page_frame)
        self.layout.addWidget(self.page_frame)
        
        self.prev_btn = QPushButton("< 上一页")
        self.prev_btn.setFont(FONTS['button'])
        self.prev_btn.clicked.connect(self.prev_page)
        self.page_layout.addWidget(self.prev_btn)
        
        self.page_label = QLabel("1/1")
        self.page_label.setFont(FONTS['label'])
        self.page_layout.addWidget(self.page_label)
        
        self.next_btn = QPushButton("下一页 >")
        self.next_btn.setFont(FONTS['button'])
        self.next_btn.clicked.connect(self.next_page)
        self.page_layout.addWidget(self.next_btn)
        
        # 显示数据
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        self.current_data = LYRICS_PROMPTS
        self.display_page()
    
    def on_search(self, text):
        """搜索"""
        search_text = text.lower()
        if not search_text:
            self.current_data = LYRICS_PROMPTS
        else:
            self.current_data = [
                p for p in LYRICS_PROMPTS
                if (search_text in p["en_name"].lower() or 
                    search_text in p["zh_name"] or
                    search_text in p["category"].lower())
            ]
        self.current_page = 1
        self.display_page()
    
    def on_category_changed(self, category):
        """分类改变"""
        self.current_category = category
        if category == "All":
            self.current_data = LYRICS_PROMPTS
        else:
            self.current_data = [
                p for p in LYRICS_PROMPTS
                if p["category"] == category
            ]
        self.current_page = 1
        self.display_page()
    
    def display_page(self):
        """显示当前页"""
        self.clear_content()
        
        if not self.current_data:
            no_result_label = QLabel("未找到匹配的提示词")
            no_result_label.setFont(FONTS['label'])
            self.content_layout.addWidget(no_result_label)
            return
        
        # 计算分页
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.current_data[start_idx:end_idx]
        
        # 显示提示词
        for prompt in page_data:
            self.add_prompt_card(prompt)
        
        # 更新分页信息
        total_pages = (len(self.current_data) + self.items_per_page - 1) // self.items_per_page
        self.page_label.setText(f"{self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
    
    def add_prompt_card(self, prompt):
        """添加提示词卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_input']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        # 复选框和标题
        header_layout = QHBoxLayout()
        
        checkbox = QCheckBox(f"{prompt['en_name']} - {prompt['zh_name']}")
        checkbox.setFont(FONTS['checkbox'])
        checkbox.setChecked(prompt['en_name'] in self.selected_lyrics)
        checkbox.stateChanged.connect(
            lambda state, e=prompt['en_name']: self.toggle_lyrics(e, state)
        )
        header_layout.addWidget(checkbox)
        
        card_layout.addLayout(header_layout)
        
        # 分类标签
        category_label = QLabel(f"分类: {prompt['category']}")
        category_label.setFont(FONTS['card_desc'])
        category_label.setStyleSheet(f"color: {COLORS['text_muted']};")
        card_layout.addWidget(category_label)
        
        self.content_layout.addWidget(card)
    
    def toggle_lyrics(self, lyrics, state):
        """切换附加提示词选择"""
        if state == 2:
            self.selected_lyrics.add(lyrics)
        else:
            self.selected_lyrics.discard(lyrics)
        
        if self.selection_changed_callback:
            self.selection_changed_callback()
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_page()
    
    def next_page(self):
        """下一页"""
        total_pages = (len(self.current_data) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_page()


class StructureTab(TabContentWidget):
    """结构提示词标签页"""
    
    def __init__(self, parent=None, selection_changed_callback=None):
        super().__init__(parent)
        self.selection_changed_callback = selection_changed_callback
        self.selected_structure = set()
        self.current_page = 1
        self.items_per_page = 10
        self.current_data = []
        self.current_category = "All"
        
        # 添加控制元素
        search_label = QLabel("搜索:")
        search_label.setFont(FONTS['label'])
        self.control_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setFont(FONTS['input'])
        self.search_input.setPlaceholderText("搜索提示词...")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.on_search)
        self.control_layout.addWidget(self.search_input)
        
        self.control_layout.addSpacing(20)
        
        category_label = QLabel("分类:")
        category_label.setFont(FONTS['label'])
        self.control_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.setFont(FONTS['input'])
        categories = ["All"] + STRUCTURE_CATEGORIES
        self.category_combo.addItems(categories)
        self.category_combo.setMinimumWidth(150)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        self.control_layout.addWidget(self.category_combo)
        
        # 分页控制
        self.page_frame = QFrame()
        self.page_layout = QHBoxLayout(self.page_frame)
        self.layout.addWidget(self.page_frame)
        
        self.prev_btn = QPushButton("< 上一页")
        self.prev_btn.setFont(FONTS['button'])
        self.prev_btn.clicked.connect(self.prev_page)
        self.page_layout.addWidget(self.prev_btn)
        
        self.page_label = QLabel("1/1")
        self.page_label.setFont(FONTS['label'])
        self.page_layout.addWidget(self.page_label)
        
        self.next_btn = QPushButton("下一页 >")
        self.next_btn.setFont(FONTS['button'])
        self.next_btn.clicked.connect(self.next_page)
        self.page_layout.addWidget(self.next_btn)
        
        # 显示数据
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        self.current_data = STRUCTURE_PROMPTS
        self.display_page()
    
    def on_search(self, text):
        """搜索"""
        search_text = text.lower()
        if not search_text:
            self.current_data = STRUCTURE_PROMPTS
        else:
            self.current_data = [
                p for p in STRUCTURE_PROMPTS
                if (search_text in p["en_name"].lower() or 
                    search_text in p["zh_name"] or
                    search_text in p["category"].lower())
            ]
        self.current_page = 1
        self.display_page()
    
    def on_category_changed(self, category):
        """分类改变"""
        self.current_category = category
        if category == "All":
            self.current_data = STRUCTURE_PROMPTS
        else:
            self.current_data = [
                p for p in STRUCTURE_PROMPTS
                if p["category"] == category
            ]
        self.current_page = 1
        self.display_page()
    
    def display_page(self):
        """显示当前页"""
        self.clear_content()
        
        if not self.current_data:
            no_result_label = QLabel("未找到匹配的提示词")
            no_result_label.setFont(FONTS['label'])
            self.content_layout.addWidget(no_result_label)
            return
        
        # 计算分页
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.current_data[start_idx:end_idx]
        
        # 显示提示词
        for prompt in page_data:
            self.add_prompt_card(prompt)
        
        # 更新分页信息
        total_pages = (len(self.current_data) + self.items_per_page - 1) // self.items_per_page
        self.page_label.setText(f"{self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
    
    def add_prompt_card(self, prompt):
        """添加提示词卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_input']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        # 复选框和标题
        header_layout = QHBoxLayout()
        
        checkbox = QCheckBox(f"{prompt['en_name']} - {prompt['zh_name']}")
        checkbox.setFont(FONTS['checkbox'])
        checkbox.setChecked(prompt['en_name'] in self.selected_structure)
        checkbox.stateChanged.connect(
            lambda state, e=prompt['en_name']: self.toggle_structure(e, state)
        )
        header_layout.addWidget(checkbox)
        
        card_layout.addLayout(header_layout)
        
        # 分类标签
        category_label = QLabel(f"分类: {prompt['category']}")
        category_label.setFont(FONTS['card_desc'])
        category_label.setStyleSheet(f"color: {COLORS['text_muted']};")
        card_layout.addWidget(category_label)
        
        self.content_layout.addWidget(card)
    
    def toggle_structure(self, structure, state):
        """切换结构提示词选择"""
        if state == 2:
            self.selected_structure.add(structure)
        else:
            self.selected_structure.discard(structure)
        
        if self.selection_changed_callback:
            self.selection_changed_callback()
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_page()
    
    def next_page(self):
        """下一页"""
        total_pages = (len(self.current_data) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_page()


class DanceTab(TabContentWidget):
    """舞曲提示词标签页"""
    
    def __init__(self, parent=None, selection_changed_callback=None):
        super().__init__(parent)
        self.selection_changed_callback = selection_changed_callback
        self.selected_dance = set()
        self.current_page = 1
        self.items_per_page = 10
        self.current_data = []
        self.current_category = "All"
        
        # 获取所有分类
        all_categories = set()
        for prompt in DANCE_PROMPTS:
            all_categories.update(prompt.get('categories', []))
        categories = ["All"] + sorted(list(all_categories))
        
        # 添加控制元素
        search_label = QLabel("搜索:")
        search_label.setFont(FONTS['label'])
        self.control_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setFont(FONTS['input'])
        self.search_input.setPlaceholderText("搜索提示词...")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.on_search)
        self.control_layout.addWidget(self.search_input)
        
        self.control_layout.addSpacing(20)
        
        category_label = QLabel("分类:")
        category_label.setFont(FONTS['label'])
        self.control_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.setFont(FONTS['input'])
        self.category_combo.addItems(categories)
        self.category_combo.setMinimumWidth(150)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        self.control_layout.addWidget(self.category_combo)
        
        # 分页控制
        self.page_frame = QFrame()
        self.page_layout = QHBoxLayout(self.page_frame)
        self.layout.addWidget(self.page_frame)
        
        self.prev_btn = QPushButton("< 上一页")
        self.prev_btn.setFont(FONTS['button'])
        self.prev_btn.clicked.connect(self.prev_page)
        self.page_layout.addWidget(self.prev_btn)
        
        self.page_label = QLabel("1/1")
        self.page_label.setFont(FONTS['label'])
        self.page_layout.addWidget(self.page_label)
        
        self.next_btn = QPushButton("下一页 >")
        self.next_btn.setFont(FONTS['button'])
        self.next_btn.clicked.connect(self.next_page)
        self.page_layout.addWidget(self.next_btn)
        
        # 显示数据
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        self.current_data = DANCE_PROMPTS
        self.display_page()
    
    def on_search(self, text):
        """搜索"""
        search_text = text.lower()
        if not search_text:
            self.current_data = DANCE_PROMPTS
        else:
            self.current_data = [
                p for p in DANCE_PROMPTS
                if (search_text in p["en_name"].lower() or 
                    search_text in p["zh_name"] or
                    search_text in p["zh_desc"] or
                    any(search_text in cat.lower() for cat in p.get('categories', [])))
            ]
        self.current_page = 1
        self.display_page()
    
    def on_category_changed(self, category):
        """分类改变"""
        self.current_category = category
        if category == "All":
            self.current_data = DANCE_PROMPTS
        else:
            self.current_data = [
                p for p in DANCE_PROMPTS
                if category in p.get('categories', [])
            ]
        self.current_page = 1
        self.display_page()
    
    def display_page(self):
        """显示当前页"""
        self.clear_content()
        
        if not self.current_data:
            no_result_label = QLabel("未找到匹配的提示词")
            no_result_label.setFont(FONTS['label'])
            self.content_layout.addWidget(no_result_label)
            return
        
        # 计算分页
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.current_data[start_idx:end_idx]
        
        # 显示提示词
        for prompt in page_data:
            self.add_prompt_card(prompt)
        
        # 更新分页信息
        total_pages = (len(self.current_data) + self.items_per_page - 1) // self.items_per_page
        self.page_label.setText(f"{self.current_page}/{total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
    
    def add_prompt_card(self, prompt):
        """添加提示词卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_input']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        # 复选框和标题
        header_layout = QHBoxLayout()
        
        checkbox = QCheckBox(f"{prompt['en_name']} - {prompt['zh_name']}")
        checkbox.setFont(FONTS['checkbox'])
        checkbox.setChecked(prompt['en_name'] in self.selected_dance)
        checkbox.stateChanged.connect(
            lambda state, e=prompt['en_name']: self.toggle_dance(e, state)
        )
        header_layout.addWidget(checkbox)
        
        card_layout.addLayout(header_layout)
        
        # 分类标签
        categories_str = ", ".join(prompt.get('categories', []))
        category_label = QLabel(f"分类: {categories_str}")
        category_label.setFont(FONTS['card_desc'])
        category_label.setStyleSheet(f"color: {COLORS['text_muted']};")
        card_layout.addWidget(category_label)
        
        # 描述
        desc_label = QLabel(prompt['zh_desc'])
        desc_label.setFont(FONTS['card_desc'])
        desc_label.setStyleSheet(f"color: {COLORS['text_muted']};")
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        self.content_layout.addWidget(card)
    
    def toggle_dance(self, dance, state):
        """切换舞曲提示词选择"""
        if state == 2:
            self.selected_dance.add(dance)
        else:
            self.selected_dance.discard(dance)
        
        if self.selection_changed_callback:
            self.selection_changed_callback()
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_page()
    
    def next_page(self):
        """下一页"""
        total_pages = (len(self.current_data) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_page()


class SunoPromptGenerator(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Suno AI Prompt Generator")
        self.resize(1400, 850)
        
        # 创建中央控件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 主布局
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)
        
        # 创建分割器
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.splitter)
        
        # 创建标签页
        self.create_tab_widget()
        
        # 创建输出面板
        self.create_output_panel()
        
        # 设置分割器比例
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
    
    def create_tab_widget(self):
        """创建标签页控件"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setMinimumWidth(500)
        
        # 创建各个标签页
        self.genre_tab = GenreTab(selection_changed_callback=self.update_selection_display)
        self.tempo_tab = TempoTab(selection_changed_callback=self.update_selection_display)
        self.style_tab = StyleTab(selection_changed_callback=self.update_selection_display)
        self.instrument_tab = InstrumentTab(selection_changed_callback=self.update_selection_display)
        self.bonus_tab = BonusTab(selection_changed_callback=self.update_selection_display)
        self.structure_tab = StructureTab(selection_changed_callback=self.update_selection_display)
        self.dance_tab = DanceTab(selection_changed_callback=self.update_selection_display)
        
        # 添加标签页
        self.tab_widget.addTab(self.genre_tab, "Genre 风格")
        self.tab_widget.addTab(self.tempo_tab, "Tempo 节奏")
        self.tab_widget.addTab(self.style_tab, "Style 描述")
        self.tab_widget.addTab(self.instrument_tab, "Instruments 乐器")
        self.tab_widget.addTab(self.bonus_tab, "Bonus 附加")
        self.tab_widget.addTab(self.structure_tab, "Structure 结构")
        self.tab_widget.addTab(self.dance_tab, "Dance 舞曲")
        
        self.splitter.addWidget(self.tab_widget)
    
    def create_output_panel(self):
        """创建输出面板"""
        output_panel = QFrame()
        output_layout = QVBoxLayout(output_panel)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("Current Selection 当前选择")
        title_label.setFont(FONTS['title'])
        title_label.setStyleSheet(f"font-weight: bold; color: {COLORS['text']};")
        output_layout.addWidget(title_label)
        
        # 当前选择显示
        self.selection_display = QTextEdit()
        self.selection_display.setReadOnly(True)
        self.selection_display.setFont(FONTS['input'])
        self.selection_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        output_layout.addWidget(self.selection_display)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("Generate 生成")
        self.generate_btn.setFont(FONTS['button'])
        self.generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_hover']};
            }}
        """)
        self.generate_btn.clicked.connect(self.generate_prompt)
        button_layout.addWidget(self.generate_btn)
        
        self.copy_btn = QPushButton("Copy 复制")
        self.copy_btn.setFont(FONTS['button'])
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['highlight']};
            }}
        """)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_btn)
        
        self.clear_btn = QPushButton("Clear 清空")
        self.clear_btn.setFont(FONTS['button'])
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['highlight']};
            }}
        """)
        self.clear_btn.clicked.connect(self.clear_selection)
        button_layout.addWidget(self.clear_btn)
        
        output_layout.addLayout(button_layout)
        
        # 输出区域
        output_label = QLabel("Generated Prompt 生成的提示词")
        output_label.setFont(FONTS['title'])
        output_label.setStyleSheet(f"font-weight: bold; color: {COLORS['text']};")
        output_layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setFont(FONTS['input'])
        self.output_text.setPlaceholderText("生成的提示词将显示在这里...")
        self.output_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        output_layout.addWidget(self.output_text)
        
        self.splitter.addWidget(output_panel)
    
    def update_selection_display(self):
        """更新选择显示"""
        selections = []
        
        if self.genre_tab.selected_genres:
            selections.extend([f"Genre: {', '.join(sorted(self.genre_tab.selected_genres))}"])
        
        if self.tempo_tab.selected_tempos:
            selections.extend([f"Tempo: {', '.join(sorted(self.tempo_tab.selected_tempos))}"])
        
        if self.style_tab.selected_styles:
            selections.extend([f"Style: {', '.join(sorted(self.style_tab.selected_styles))}"])
        
        if self.instrument_tab.selected_instruments:
            selections.extend([f"Instruments: {', '.join(sorted(self.instrument_tab.selected_instruments))}"])
        
        if self.bonus_tab.selected_lyrics:
            selections.extend([f"Bonus: {', '.join(sorted(self.bonus_tab.selected_lyrics))}"])
        
        if self.structure_tab.selected_structure:
            selections.extend([f"Structure: {', '.join(sorted(self.structure_tab.selected_structure))}"])
        
        if self.dance_tab.selected_dance:
            selections.extend([f"Dance: {', '.join(sorted(self.dance_tab.selected_dance))}"])
        
        if selections:
            self.selection_display.setText('\n'.join(selections))
        else:
            self.selection_display.setText("No selections yet / 暂无选择")
    
    def generate_prompt(self):
        """生成提示词"""
        prompt_parts = []
        
        # 添加Genre
        if self.genre_tab.selected_genres:
            prompt_parts.extend(sorted(self.genre_tab.selected_genres))
        
        # 添加Tempo
        if self.tempo_tab.selected_tempos:
            prompt_parts.extend(sorted(self.tempo_tab.selected_tempos))
        
        # 添加Style
        if self.style_tab.selected_styles:
            prompt_parts.extend(sorted(self.style_tab.selected_styles))
        
        # 添加Instruments
        if self.instrument_tab.selected_instruments:
            prompt_parts.extend(sorted(self.instrument_tab.selected_instruments))
        
        # 添加Bonus Prompts
        if self.bonus_tab.selected_lyrics:
            prompt_parts.extend(sorted(self.bonus_tab.selected_lyrics))
        
        # 添加Structure Prompts
        if self.structure_tab.selected_structure:
            prompt_parts.extend(sorted(self.structure_tab.selected_structure))
        
        # 添加Dance Prompts
        if self.dance_tab.selected_dance:
            for prompt_name in self.dance_tab.selected_dance:
                prompt = next((p for p in DANCE_PROMPTS if p['en_name'] == prompt_name), None)
                if prompt:
                    prompt_parts.append(prompt['en_desc'])
        
        # 生成最终提示词
        if prompt_parts:
            final_prompt = ", ".join(prompt_parts)
            
            # 添加一些额外的描述性词汇使提示词更完整
            descriptive_parts = []
            
            if "Energetic" in self.style_tab.selected_styles:
                descriptive_parts.append("high energy")
            if "Melodic" in self.style_tab.selected_styles:
                descriptive_parts.append("melodic elements")
            if "Cinematic" in self.style_tab.selected_styles:
                descriptive_parts.append("cinematic quality")
            if "Dreamy" in self.style_tab.selected_styles or "Ethereal" in self.style_tab.selected_styles:
                descriptive_parts.append("atmospheric textures")
            if "Bass-heavy" in self.style_tab.selected_styles:
                descriptive_parts.append("heavy bass")
            if "Punchy" in self.style_tab.selected_styles:
                descriptive_parts.append("punchy drums")
            
            # 组合提示词
            if descriptive_parts:
                final_prompt = f"{final_prompt}, {', '.join(descriptive_parts)}"
            
            self.output_text.setText(final_prompt)
        else:
            QMessageBox.warning(self, "警告", "请至少选择一个标签！")
    
    def copy_to_clipboard(self):
        """复制到剪贴板"""
        text = self.output_text.toPlainText().strip()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "成功", "提示词已复制到剪贴板！")
        else:
            QMessageBox.warning(self, "警告", "没有可复制的内容！")
    
    def clear_selection(self):
        """清空所有选择"""
        self.genre_tab.selected_genres.clear()
        self.tempo_tab.selected_tempos.clear()
        self.style_tab.selected_styles.clear()
        self.instrument_tab.selected_instruments.clear()
        self.bonus_tab.selected_lyrics.clear()
        self.structure_tab.selected_structure.clear()
        self.dance_tab.selected_dance.clear()
        
        # 清空显示
        self.selection_display.clear()
        self.output_text.clear()
        
        # 刷新所有标签页显示
        self.genre_tab.show_genre_tags(self.genre_tab.combo.currentText())
        self.tempo_tab.show_tempo_tags(self.tempo_tab.combo.currentText())
        self.style_tab.show_style_tags(self.style_tab.combo.currentText())
        self.instrument_tab.show_instruments()
        self.bonus_tab.display_page()
        self.structure_tab.display_page()
        self.dance_tab.display_page()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置深色主题
    set_dark_theme(app)
    
    # 创建并显示主窗口
    window = SunoPromptGenerator()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()