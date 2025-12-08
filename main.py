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
                border-radius: 8px;
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
                padding: 10px 20px;
                margin-right: 4px;
                margin-bottom: 8px;
                border-radius: 8px;
                color: rgba(0, 0, 0, 0.6);
                min-width: 100px;
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
        # tabs.addTab(..., "2. Выбор файла")
        # tabs.addTab(..., "3. Текст + кнопка")
        # tabs.addTab(..., "4. График (Tkinter)")
        # tabs.addTab(..., "5. Локальный чат")

        main_layout.addWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
