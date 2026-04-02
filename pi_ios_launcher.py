#!/usr/bin/env python3
"""
Pi iOS Launcher - iOS-like interface for Raspberry Pi 4.3" display
"""

import sys
import os
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                             QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QScrollArea, QFrame, QListWidget,
                             QTextEdit, QLineEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QPainter

class StatusBar(QWidget):
    """iOS-like status bar"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 150);
                color: white;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        # Time label
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 10, QFont.Bold))

        # Battery/Status indicators
        self.status_label = QLabel("●●●●●")
        self.status_label.setFont(QFont("Arial", 10))

        layout.addWidget(self.time_label)
        layout.addStretch()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Update time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M")
        self.time_label.setText(current_time)

class AppIcon(QPushButton):
    """iOS-style app icon button"""
    def __init__(self, name, icon_text, callback, parent=None):
        super().__init__(parent)
        self.app_name = name
        self.callback = callback

        # Style the button
        self.setFixedSize(80, 100)
        self.setText(f"{icon_text}\n{name}")
        self.setFont(QFont("Arial", 10))
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 15px;
                color: black;
                padding: 5px;
                border: 2px solid rgba(255, 255, 255, 100);
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 200);
            }
        """)

        self.clicked.connect(self.on_click)

    def on_click(self):
        if self.callback:
            self.callback(self.app_name)

class HomePage(QWidget):
    """iOS-like home screen with app grid"""
    def __init__(self, launch_callback, parent=None):
        super().__init__(parent)
        self.launch_callback = launch_callback

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 80)
        main_layout.setSpacing(20)

        # Create scrollable area for apps
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Container for app grid
        container = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # Define apps with emoji icons
        apps = [
            ("Settings", "⚙️", self.launch_callback),
            ("Files", "📁", self.launch_callback),
            ("Terminal", "💻", self.launch_callback),
            ("Browser", "🌐", self.launch_callback),
            ("Calculator", "🔢", self.launch_callback),
            ("Notes", "📝", self.launch_callback),
            ("Photos", "📷", self.launch_callback),
            ("Music", "🎵", self.launch_callback),
            ("Videos", "🎬", self.launch_callback),
            ("Clock", "⏰", self.launch_callback),
            ("Weather", "🌤️", self.launch_callback),
            ("Mail", "✉️", self.launch_callback),
        ]

        # Add apps to grid (3 columns for 4.3" display)
        row, col = 0, 0
        for app_name, icon, callback in apps:
            app_icon = AppIcon(app_name, icon, callback)
            grid_layout.addWidget(app_icon, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        container.setLayout(grid_layout)
        scroll.setWidget(container)

        main_layout.addWidget(scroll)

        # Dock at bottom
        dock = self.create_dock()
        main_layout.addWidget(dock)

        self.setLayout(main_layout)

    def create_dock(self):
        """Create iOS-like dock"""
        dock = QFrame()
        dock.setFixedHeight(70)
        dock.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 150);
                border-radius: 20px;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        # Dock apps
        dock_apps = [
            ("Phone", "📞", self.launch_callback),
            ("Messages", "💬", self.launch_callback),
            ("Camera", "📸", self.launch_callback),
        ]

        for app_name, icon, callback in dock_apps:
            btn = AppIcon(app_name, icon, callback)
            btn.setFixedSize(60, 60)
            layout.addWidget(btn)

        dock.setLayout(layout)
        return dock

class FileManager(QWidget):
    """Simple file manager"""
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Current path
        self.path_label = QLabel("/home/pi")
        self.path_label.setStyleSheet("QLabel { background: white; padding: 5px; border-radius: 5px; }")
        layout.addWidget(self.path_label)

        # File list
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                background: white;
                border-radius: 10px;
                padding: 5px;
                font-size: 12px;
            }
        """)
        self.file_list.itemDoubleClicked.connect(self.open_item)
        layout.addWidget(self.file_list)

        # Buttons
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("⬅️ Back")
        back_btn.clicked.connect(self.go_back)
        home_btn = QPushButton("🏠 Home")
        home_btn.clicked.connect(self.go_home)

        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(home_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.current_path = "/home/pi"
        self.load_directory()

    def load_directory(self):
        self.file_list.clear()
        self.path_label.setText(self.current_path)

        try:
            items = os.listdir(self.current_path)
            for item in sorted(items):
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    self.file_list.addItem(f"📁 {item}")
                else:
                    self.file_list.addItem(f"📄 {item}")
        except Exception as e:
            self.file_list.addItem(f"Error: {e}")

    def open_item(self, item):
        name = item.text()[2:].strip()
        new_path = os.path.join(self.current_path, name)
        if os.path.isdir(new_path):
            self.current_path = new_path
            self.load_directory()

    def go_back(self):
        self.current_path = os.path.dirname(self.current_path)
        self.load_directory()

    def go_home(self):
        self.current_path = os.path.expanduser("~")
        self.load_directory()

class Terminal(QWidget):
    """Simple terminal emulator"""
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: #00ff00;
                font-family: monospace;
                font-size: 10px;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.output)

        # Input area
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        self.input.returnPressed.connect(self.execute_command)

        exec_btn = QPushButton("Run")
        exec_btn.clicked.connect(self.execute_command)

        input_layout.addWidget(self.input)
        input_layout.addWidget(exec_btn)
        layout.addLayout(input_layout)

        self.setLayout(layout)
        self.output.append("Welcome to Pi iOS Terminal\n$ ")

    def execute_command(self):
        command = self.input.text()
        if not command:
            return

        self.output.append(f"$ {command}")
        self.input.clear()

        try:
            result = subprocess.run(command, shell=True, capture_output=True,
                                   text=True, timeout=10)
            output = result.stdout + result.stderr
            self.output.append(output if output else "(no output)")
        except Exception as e:
            self.output.append(f"Error: {e}")

        self.output.append("$ ")

class SettingsApp(QWidget):
    """Settings application"""
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Settings list
        settings_list = QListWidget()
        settings_list.setStyleSheet("""
            QListWidget {
                background: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
        """)

        settings_items = [
            "📶 Wi-Fi",
            "🔊 Sound",
            "🔆 Display & Brightness",
            "🏠 Wallpaper",
            "🔋 Battery",
            "⚙️ General",
            "🔒 Privacy & Security",
            "ℹ️ About",
        ]

        for item in settings_items:
            settings_list.addItem(item)

        layout.addWidget(settings_list)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pi iOS Launcher")

        # Set window size for 4.3" display (common resolutions)
        # 800x480 is typical for 4.3" displays
        self.setFixedSize(800, 480)

        # Set iOS-like background
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Status bar
        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)

        # Stacked widget for different pages
        self.stack = QStackedWidget()

        # Home page
        self.home_page = HomePage(self.launch_app)
        self.stack.addWidget(self.home_page)

        # App pages
        self.file_manager = FileManager()
        self.stack.addWidget(self.file_manager)

        self.terminal = Terminal()
        self.stack.addWidget(self.terminal)

        self.settings = SettingsApp()
        self.stack.addWidget(self.settings)

        layout.addWidget(self.stack)

        # Home button
        home_btn = QPushButton("●")
        home_btn.setFixedHeight(20)
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 20px;
            }
        """)
        home_btn.clicked.connect(self.go_home)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)

        main_widget.setLayout(layout)

        # Enable touch events
        self.setAttribute(Qt.WA_AcceptTouchEvents)

    def launch_app(self, app_name):
        """Launch an application"""
        if app_name == "Files":
            self.stack.setCurrentWidget(self.file_manager)
        elif app_name == "Terminal":
            self.stack.setCurrentWidget(self.terminal)
        elif app_name == "Settings":
            self.stack.setCurrentWidget(self.settings)
        elif app_name == "Browser":
            try:
                subprocess.Popen(["chromium-browser"])
            except:
                QMessageBox.information(self, "Browser", "Browser not available")
        elif app_name == "Calculator":
            try:
                subprocess.Popen(["galculator"])
            except:
                QMessageBox.information(self, "Calculator", "Calculator not available")
        else:
            QMessageBox.information(self, app_name, f"{app_name} app coming soon!")

    def go_home(self):
        """Return to home screen"""
        self.stack.setCurrentWidget(self.home_page)

def main():
    app = QApplication(sys.argv)

    # Set global font
    font = QFont("Arial", 11)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
