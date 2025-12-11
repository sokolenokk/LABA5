import sys
import subprocess
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QProgressBar,
    QFileDialog, QMessageBox, QSlider, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class ProgressBarTab(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        title = QLabel("Демонстрация прогрессбара")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1559EA;
                border-radius: 8px;
                text-align: center;
                height: 30px;
                font-size: 14px;
                background-color: rgba(0, 0, 0, 0.1);
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #1559EA;
                border-radius: 6px;
            }    
        """)
        layout.addWidget(self.progress_bar)

        slider_container = QVBoxLayout()
        slider_container.setSpacing(8)

        slider_title = QLabel("Ручное управление:")
        slider_title.setAlignment(Qt.AlignCenter)
        slider_title.setStyleSheet("color: rgba(0, 0, 0, 0.6);")
        slider_container.addWidget(slider_title)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.slider_changed)
        self.slider.setFixedHeight(30)
        self.slider.setStyleSheet("""
            QSlider {
                background: transparent;
            }
            QSlider::groove:horizontal {
                border: 1px solid #1559EA;
                height: 8px;
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background-color: #1559EA;
                border: 2px solid #1559EA;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background-color: #3479E9;
                border: 2px solid #3479E9;
            }
            QSlider::sub-page:horizontal {
                background-color: #1559EA;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 4px;
            }
        """)
        slider_container.addWidget(self.slider)

        self.slider_label = QLabel("0%")
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.slider_label.setStyleSheet("color: #1559EA; font-weight: bold; font-size: 14px;")
        slider_container.addWidget(self.slider_label)

        layout.addLayout(slider_container)

        buttons_layout = QHBoxLayout()

        self.start_btn = QPushButton("Старт")
        self.start_btn.clicked.connect(self.start_progress)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #1559EA;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;                
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Пауза")
        self.stop_btn.clicked.connect(self.stop_progress)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #61A6FA;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(self.stop_btn)

        self.reset_btn = QPushButton("Сброс")
        self.reset_btn.clicked.connect(self.reset_progress)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2);
                color: rgba(0, 0, 0, 0.7);
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.3);
            }
        """)
        buttons_layout.addWidget(self.reset_btn)

        layout.addLayout(buttons_layout)

        self.status_label = QLabel("Статус: Ожидание")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: rgba(0, 0, 0, 0.5);")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

    def start_progress(self):
        self.timer.start(50)
        self.status_label.setText("Статус: Выполняется...")
        self.status_label.setStyleSheet("color: #1559EA; font-weight: bold;")

    def stop_progress(self):
        self.timer.stop()
        self.status_label.setText("Статус: Пауза")
        self.status_label.setStyleSheet("color: #61A6FA; font-weight: bold;")

    def reset_progress(self):
        self.timer.stop()
        self.progress_bar.setValue(0)
        self.slider.setValue(0)
        self.status_label.setText("Статус: Сброшено")
        self.status_label.setStyleSheet("color: rgba(0, 0, 0, 0.5);")

    def update_progress(self):
        current = self.progress_bar.value()
        if current >= 100:
            self.timer.stop()
            self.status_label.setText("Статус: Завершено!")
            self.status_label.setStyleSheet("color: #1559EA; font-weight: bold;")
        else:
            self.progress_bar.setValue(current + 1)
            self.slider.blockSignals(True)
            self.slider.setValue(current + 1)
            self.slider.blockSignals(False)
            self.slider_label.setText(f"{current + 1}%")

    def slider_changed(self, value):
        self.progress_bar.setValue(value)
        self.slider_label.setText(f"{value}%")


class FileDialogTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Диалоги выбора файлов")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        buttons_layout = QGridLayout(buttons_frame)
        buttons_layout.setSpacing(10)

        open_btn = QPushButton("Открыть файл")
        open_btn.clicked.connect(self.open_file)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #1559EA;
                color: white;
                border: none;
                padding: 15px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(open_btn, 0, 0)

        open_multiple_btn = QPushButton("Открыть несколько")
        open_multiple_btn.clicked.connect(self.open_multiple_files)
        open_multiple_btn.setStyleSheet("""
            QPushButton {
                background-color: #1559EA;
                color: white;
                border: none;
                padding: 15px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(open_multiple_btn, 0, 1)

        save_btn = QPushButton("Сохранить как...")
        save_btn.clicked.connect(self.save_file)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #61A6FA;
                color: white;
                border: none;
                padding: 15px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(save_btn, 1, 0)

        dir_btn = QPushButton("Выбрать папку")
        dir_btn.clicked.connect(self.select_directory)
        dir_btn.setStyleSheet("""
            QPushButton {
                background-color: #61A6FA;
                color: white;
                border: none;
                padding: 15px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(dir_btn, 1, 1)

        layout.addWidget(buttons_frame)

        info_label = QLabel("Информация о файле:")
        info_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(info_label)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.05);
                color: rgba(0, 0, 0, 0.8);
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.info_text.setPlaceholderText("Здесь появится информация о выбранном файле...")
        layout.addWidget(self.info_text)

        self.setLayout(layout)

    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Все файлы (*);;Текстовые файлы (*.txt);;Python файлы (*.py);;Изображения (*.png *.jpg *.jpeg)"
        )
        if filepath:
            self.show_file_info(filepath)

    def open_multiple_files(self):
        filepaths, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите файлы",
            "",
            "Все файлы (*);;Текстовые файлы (*.txt)"
        )
        if filepaths:
            info = f"Выбрано файлов: {len(filepaths)}\n\n"
            for i, fp in enumerate(filepaths, 1):
                info += f"{i}. {os.path.basename(fp)}\n"
                info += f"   Путь: {fp}\n\n"
            self.info_text.setText(info)

    def save_file(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            "new_file.txt",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if filepath:
            self.info_text.setText(f"Файл будет сохранён как:\n{filepath}")

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку",
            ""
        )
        if directory:
            files = os.listdir(directory)
            info = f"Выбрана папка:\n{directory}\n\n"
            info += f"Содержимое ({len(files)} элементов):\n"
            for item in files[:20]:
                full_path = os.path.join(directory, item)
                item_type = "[Папка]" if os.path.isdir(full_path) else "[Файл]"
                info += f"  {item_type} {item}\n"
            if len(files) > 20:
                info += f"\n  ... и ещё {len(files) - 20} элементов"
            self.info_text.setText(info)

    def show_file_info(self, filepath):
        try:
            stat = os.stat(filepath)
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

            if size < 1024:
                size_str = f"{size} байт"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} КБ"
            else:
                size_str = f"{size / (1024 * 1024):.2f} МБ"

            info = f"Имя файла: {os.path.basename(filepath)}\n"
            info += f"Полный путь: {filepath}\n"
            info += f"Размер: {size_str}\n"
            info += f"Изменён: {modified}\n"
            info += f"Расширение: {os.path.splitext(filepath)[1] or 'нет'}\n"

            if filepath.endswith(('.txt', '.py', '.md', '.json', '.html', '.css')):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read(500)
                    info += f"\n--- Превью содержимого ---\n{content}"
                    if len(content) == 500:
                        info += "\n..."
                except:
                    pass

            self.info_text.setText(info)
        except Exception as e:
            self.info_text.setText(f"Ошибка чтения файла:\n{str(e)}")


class TextOutputTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Обработка текста")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        input_label = QLabel("Введите текст:")
        input_label.setStyleSheet("color: rgba(0, 0, 0, 0.6);")
        layout.addWidget(input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите что-нибудь и нажмите кнопку...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                color: #000000;
                padding: 12px;
                font-size: 14px;
                border: 2px solid rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                background-color: rgba(0, 0, 0, 0.05);
            }
            QLineEdit:focus {
                border-color: #1559EA;
            }
        """)
        self.input_field.returnPressed.connect(self.process_text)
        layout.addWidget(self.input_field)

        buttons_layout = QHBoxLayout()

        process_btn = QPushButton("Вывести текст")
        process_btn.clicked.connect(self.process_text)
        process_btn.setStyleSheet("""
            QPushButton {
                background-color: #1559EA;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(process_btn)

        upper_btn = QPushButton("В верхний регистр")
        upper_btn.clicked.connect(self.to_upper)
        upper_btn.setStyleSheet("""
            QPushButton {
                background-color: #1559EA;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(upper_btn)

        reverse_btn = QPushButton("Перевернуть")
        reverse_btn.clicked.connect(self.reverse_text)
        reverse_btn.setStyleSheet("""
            QPushButton {
                background-color: #61A6FA;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        buttons_layout.addWidget(reverse_btn)

        clear_btn = QPushButton("Очистить")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2);
                color: rgba(0, 0, 0, 0.7);
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.3);
            }
        """)
        buttons_layout.addWidget(clear_btn)

        layout.addLayout(buttons_layout)

        output_label = QLabel("Результат:")
        output_label.setStyleSheet("color: rgba(0, 0, 0, 0.6);")
        layout.addWidget(output_label)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.05);
                color: rgba(0, 0, 0, 0.8);
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        layout.addWidget(self.output_area)

        self.stats_label = QLabel("Статистика: 0 символов, 0 слов")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("color: rgba(0, 0, 0, 0.5);")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def process_text(self):
        text = self.input_field.text()
        if text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.output_area.append(f"[{timestamp}] {text}")
            self.update_stats(text)
        else:
            QMessageBox.warning(self, "Внимание", "Введите текст!")

    def to_upper(self):
        text = self.input_field.text()
        if text:
            result = text.upper()
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.output_area.append(f"[{timestamp}] UPPER: {result}")
            self.update_stats(text)

    def reverse_text(self):
        text = self.input_field.text()
        if text:
            result = text[::-1]
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.output_area.append(f"[{timestamp}] REVERSE: {result}")
            self.update_stats(text)

    def clear_all(self):
        self.input_field.clear()
        self.output_area.clear()
        self.stats_label.setText("Статистика: 0 символов, 0 слов")

    def update_stats(self, text):
        chars = len(text)
        words = len(text.split())
        self.stats_label.setText(f"Статистика: {chars} символов, {words} слов")


class LocalChatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_user = "User1"
        self.user_colors = {
            "User1": "#1559EA",
            "User2": "#61A6FA",
            "Bot": "#3479E9"
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("Локальный чат")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        controls_layout = QHBoxLayout()

        user_label = QLabel("Пользователь:")
        user_label.setStyleSheet("color: rgba(0, 0, 0, 0.6);")
        controls_layout.addWidget(user_label)

        self.user1_btn = QPushButton("User 1")
        self.user1_btn.setCheckable(True)
        self.user1_btn.setChecked(True)
        self.user1_btn.clicked.connect(lambda: self.set_user("User1"))
        self.user1_btn.setStyleSheet(self.get_user_btn_style("#1559EA", True))
        controls_layout.addWidget(self.user1_btn)

        self.user2_btn = QPushButton("User 2")
        self.user2_btn.setCheckable(True)
        self.user2_btn.clicked.connect(lambda: self.set_user("User2"))
        self.user2_btn.setStyleSheet(self.get_user_btn_style("#61A6FA", False))
        controls_layout.addWidget(self.user2_btn)

        controls_layout.addStretch()

        bot_btn = QPushButton("Сообщение от бота")
        bot_btn.clicked.connect(self.bot_message)
        bot_btn.setStyleSheet("""
            QPushButton {
                background-color: #61A6FA;
                color: white;
                border: none;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        controls_layout.addWidget(bot_btn)

        clear_btn = QPushButton("Очистить чат")
        clear_btn.clicked.connect(self.clear_chat)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2);
                color: rgba(0, 0, 0, 0.7);
                border: none;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.3);
            }
        """)
        controls_layout.addWidget(clear_btn)

        layout.addLayout(controls_layout)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.05);
                color: rgba(0, 0, 0, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.chat_area)

        input_layout = QHBoxLayout()

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Введите сообщение...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 0.05);
                color: rgba(0, 0, 0, 0.8);
                padding: 12px;
                font-size: 14px;
                border: 2px solid rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            }
            QLineEdit:focus {
                border-color: #1559EA;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)

        send_btn = QPushButton("Отправить")
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #1559EA;
                color: white;
                border: none;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3479E9;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)

        layout.addLayout(input_layout)

        self.setLayout(layout)

        self.add_system_message("Добро пожаловать в локальный чат!")

    def get_user_btn_style(self, color, active):
        if active:
            return f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 8px;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: rgba(0, 0, 0, 0.05);
                    color: {color};
                    border: 2px solid {color};
                    padding: 8px 15px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 0, 0, 0.1);
                }}
            """

    def set_user(self, user):
        self.current_user = user
        self.user1_btn.setChecked(user == "User1")
        self.user2_btn.setChecked(user == "User2")
        self.user1_btn.setStyleSheet(self.get_user_btn_style("#1559EA", user == "User1"))
        self.user2_btn.setStyleSheet(self.get_user_btn_style("#61A6FA", user == "User2"))

    def send_message(self):
        text = self.message_input.text().strip()
        if text:
            self.add_message(self.current_user, text)
            self.message_input.clear()

    def add_message(self, user, text):
        timestamp = datetime.now().strftime("%H:%M")
        color = self.user_colors.get(user, "#333")
        html = f"""
        <div style="margin: 5px 0;">
            <span style="color: {color}; font-weight: bold;">{user}</span>
            <span style="color: rgba(0,0,0,0.4); font-size: 11px;"> [{timestamp}]</span>
            <br/>
            <span style="color: rgba(0,0,0,0.8);">{text}</span>
        </div>
        """
        self.chat_area.append(html)

    def add_system_message(self, text):
        html = f"""
        <div style="margin: 10px 0; text-align: center;">
            <span style="color: rgba(0,0,0,0.4);">— {text} —</span>
        </div>
        """
        self.chat_area.append(html)

    def clear_chat(self):
        self.chat_area.clear()
        self.add_system_message("Чат очищен")

    def bot_message(self):
        import random
        messages = [
            "Привет! Я бот-помощник",
            "Как дела?",
            "Интересная беседа!",
            "PyQt5 — отличный фреймворк!",
            "Tkinter тоже хорош для простых задач",
            "Не забудьте сохранить важные сообщения",
        ]
        self.add_message("Bot", random.choice(messages))



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №5")
        self.setGeometry(50, 50, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                background-color: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: rgba(0, 0, 0, 0.05);
                padding: 10px 15px;
                margin-right: 4px;
                margin-bottom: 8px;
                border-radius: 8px;
                color: rgba(0, 0, 0, 0.6);
                min-width: 140px;
            }
            QTabBar::tab:selected {
                background-color: #1559EA;
                color: white;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Лабораторная работа №5")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: rgba(0, 0, 0, 0.8); margin-bottom: 10px;")
        main_layout.addWidget(header)

        subtitle = QLabel("Визуальное программирование на Python (Tkinter & PyQt5)")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: rgba(0, 0, 0, 0.5); margin-bottom: 20px;")
        main_layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.addTab(ProgressBarTab(), "1. Прогрессбар")
        tabs.addTab(FileDialogTab(), "2. Выбор файла")
        tabs.addTab(TextOutputTab(), "3. Текст + кнопка")
        tabs.addTab(LocalChatTab(), "5. Локальный чатик")


        main_layout.addWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
