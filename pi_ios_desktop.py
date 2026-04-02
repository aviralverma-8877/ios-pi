#!/usr/bin/env python3
"""
Pi iOS Desktop Environment - GNOME-like desktop environment for Raspberry Pi
Provides a complete desktop shell with panels, desktop, and window management
"""

import sys
import os
import subprocess
import signal
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QWidget, QGridLayout,
                             QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QScrollArea, QFrame, QListWidget,
                             QTextEdit, QLineEdit, QMessageBox, QMenu, QDialog,
                             QFileDialog, QSystemTrayIcon)
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QProcess, pyqtSignal, QRect
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QCursor, QPixmap, QPainter

class TopPanel(QWidget):
    """GNOME-like top panel with activities and system tray"""

    show_activities = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(35)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 200);
                color: white;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 4px;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(10)

        # Activities button (left)
        self.activities_btn = QPushButton("🏠 Activities")
        self.activities_btn.clicked.connect(self.show_activities.emit)
        self.activities_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.activities_btn)

        # Application title (center)
        self.title_label = QLabel("Pi iOS Desktop")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.title_label, stretch=1)

        # System indicators (right)
        self.system_info = QLabel()
        self.system_info.setFont(QFont("Arial", 9))
        layout.addWidget(self.system_info)

        # Time/Date
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.time_label)

        # Power button
        self.power_btn = QPushButton("⏻")
        self.power_btn.setFixedSize(30, 30)
        self.power_btn.setFont(QFont("Arial", 14))
        self.power_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.power_btn)

        self.setLayout(layout)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)
        self.update_info()

    def update_info(self):
        # Update time
        current_time = datetime.now().strftime("%H:%M")
        self.time_label.setText(current_time)

        # Update system info
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read().strip()) / 1000
                self.system_info.setText(f"🌡️ {temp:.0f}°C")
        except:
            self.system_info.setText("")

class DesktopArea(QWidget):
    """Desktop background area - like GNOME desktop"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

class Dock(QWidget):
    """macOS/Ubuntu-like dock at bottom"""

    app_launched = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 150);
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 12px;
                color: black;
                font-size: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 220);
                border: 2px solid rgba(100, 100, 255, 150);
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 200);
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Dock apps with icons
        dock_apps = [
            ("Files", "📁"),
            ("Terminal", "💻"),
            ("Browser", "🌐"),
            ("Settings", "⚙️"),
            ("Apps", "⚡"),
        ]

        for app_name, icon in dock_apps:
            btn = QPushButton(icon)
            btn.setFixedSize(55, 55)
            btn.setToolTip(app_name)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, name=app_name: self.app_launched.emit(name))
            layout.addWidget(btn)

        self.setLayout(layout)

class ApplicationLauncher(QDialog):
    """Application launcher overlay - like GNOME Activities"""

    app_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(0, 0, 0, 220);
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #667eea;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 100);
                color: black;
                padding: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 255);
                border: 2px solid #667eea;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Search box
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Search applications...")
        self.search.setFixedHeight(50)
        self.search.textChanged.connect(self.filter_apps)
        layout.addWidget(self.search)

        # App grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)

        # All available apps
        self.all_apps = [
            ("Files", "📁", "file manager"),
            ("Terminal", "💻", "terminal console"),
            ("Browser", "🌐", "web browser"),
            ("Text Editor", "📝", "text editor"),
            ("Calculator", "🔢", "calculator math"),
            ("Settings", "⚙️", "settings configuration"),
            ("System Info", "ℹ️", "system information"),
            ("Images", "🖼️", "image viewer photos"),
            ("Music", "🎵", "music player audio"),
            ("Videos", "🎬", "video player movies"),
            ("Calendar", "📅", "calendar date"),
            ("Mail", "✉️", "email mail"),
            ("Clock", "⏰", "clock time alarm"),
            ("Weather", "🌤️", "weather forecast"),
            ("Notes", "📋", "notes notepad"),
            ("Camera", "📷", "camera photo"),
            ("Maps", "🗺️", "maps navigation"),
            ("Store", "🛍️", "app store software"),
            ("Power", "⏻", "power shutdown reboot"),
        ]

        self.app_buttons = []
        self.populate_apps()

        container.setLayout(self.grid_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def populate_apps(self, filter_text=""):
        # Clear existing
        for btn in self.app_buttons:
            btn.deleteLater()
        self.app_buttons.clear()

        # Filter apps
        filtered_apps = [
            app for app in self.all_apps
            if filter_text.lower() in app[0].lower() or filter_text.lower() in app[2]
        ] if filter_text else self.all_apps

        # Add apps to grid (4 columns)
        row, col = 0, 0
        for app_name, icon, keywords in filtered_apps:
            btn = QPushButton(f"{icon}\n{app_name}")
            btn.setFixedSize(100, 100)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, name=app_name: self.launch_app(name))
            self.grid_layout.addWidget(btn, row, col)
            self.app_buttons.append(btn)

            col += 1
            if col >= 4:
                col = 0
                row += 1

    def filter_apps(self, text):
        self.populate_apps(text)

    def launch_app(self, app_name):
        self.app_selected.emit(app_name)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def showEvent(self, event):
        super().showEvent(event)
        self.search.setFocus()
        self.search.clear()
        self.populate_apps()

class FileManagerWindow(QWidget):
    """Standalone file manager window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Files")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.Window)

        layout = QVBoxLayout()

        # Path bar
        path_layout = QHBoxLayout()
        self.path_label = QLabel(os.path.expanduser("~"))
        self.path_label.setStyleSheet("padding: 5px; background: white; border-radius: 4px;")
        back_btn = QPushButton("⬅️")
        back_btn.clicked.connect(self.go_back)
        home_btn = QPushButton("🏠")
        home_btn.clicked.connect(self.go_home)
        path_layout.addWidget(back_btn)
        path_layout.addWidget(home_btn)
        path_layout.addWidget(self.path_label, stretch=1)
        layout.addLayout(path_layout)

        # File list
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background: white; font-size: 12px;")
        self.file_list.itemDoubleClicked.connect(self.open_item)
        layout.addWidget(self.file_list)

        self.setLayout(layout)
        self.current_path = os.path.expanduser("~")
        self.load_directory()

    def load_directory(self):
        self.file_list.clear()
        self.path_label.setText(self.current_path)

        try:
            items = sorted(os.listdir(self.current_path))
            for item in items:
                full_path = os.path.join(self.current_path, item)
                icon = "📁" if os.path.isdir(full_path) else "📄"
                self.file_list.addItem(f"{icon} {item}")
        except Exception as e:
            self.file_list.addItem(f"Error: {e}")

    def open_item(self, item):
        name = item.text()[2:].strip()
        new_path = os.path.join(self.current_path, name)
        if os.path.isdir(new_path):
            self.current_path = new_path
            self.load_directory()
        else:
            try:
                subprocess.Popen(['xdg-open', new_path])
            except:
                pass

    def go_back(self):
        self.current_path = os.path.dirname(self.current_path)
        self.load_directory()

    def go_home(self):
        self.current_path = os.path.expanduser("~")
        self.load_directory()

class TerminalWindow(QWidget):
    """Standalone terminal window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminal")
        self.setGeometry(100, 100, 700, 450)
        self.setWindowFlags(Qt.Window)

        layout = QVBoxLayout()

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            background-color: #2e3440;
            color: #88c0d0;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            padding: 10px;
        """)
        layout.addWidget(self.output)

        # Input
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setStyleSheet("""
            background-color: #3b4252;
            color: #eceff4;
            border: 1px solid #4c566a;
            padding: 8px;
            font-family: 'Courier New', monospace;
        """)
        self.input.setPlaceholderText("Enter command...")
        self.input.returnPressed.connect(self.execute_command)

        exec_btn = QPushButton("Run")
        exec_btn.clicked.connect(self.execute_command)
        exec_btn.setStyleSheet("padding: 8px 15px;")

        input_layout.addWidget(self.input)
        input_layout.addWidget(exec_btn)
        layout.addLayout(input_layout)

        self.setLayout(layout)
        self.output.append("Pi iOS Terminal v1.0")
        self.output.append(f"User: {os.getenv('USER', 'pi')}")
        self.output.append(f"Home: {os.path.expanduser('~')}\n")
        self.output.append("$ ")

    def execute_command(self):
        command = self.input.text()
        if not command:
            return

        self.output.append(f"$ {command}")
        self.input.clear()

        try:
            result = subprocess.run(command, shell=True, capture_output=True,
                                   text=True, timeout=10, cwd=os.path.expanduser("~"))
            output = result.stdout + result.stderr
            if output:
                self.output.append(output.strip())
        except Exception as e:
            self.output.append(f"Error: {e}")

        self.output.append("\n$ ")
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

class SettingsWindow(QWidget):
    """System settings window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 500, 450)
        self.setWindowFlags(Qt.Window)

        layout = QVBoxLayout()

        # Settings categories
        self.settings_list = QListWidget()
        self.settings_list.setStyleSheet("""
            QListWidget {
                background: white;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)

        categories = [
            "📶 Wi-Fi & Network",
            "🔊 Sound & Volume",
            "🔆 Display & Brightness",
            "🏠 Wallpaper & Appearance",
            "🔋 Power & Battery",
            "⚙️ General Settings",
            "👤 Users & Accounts",
            "🔒 Privacy & Security",
            "🕐 Date & Time",
            "🌐 Language & Region",
            "♿ Accessibility",
            "ℹ️ About This System",
        ]

        for category in categories:
            self.settings_list.addItem(category)

        self.settings_list.itemClicked.connect(self.show_setting_detail)

        layout.addWidget(QLabel("<b>System Settings</b>"))
        layout.addWidget(self.settings_list)

        self.setLayout(layout)

    def show_setting_detail(self, item):
        QMessageBox.information(self, "Settings",
            f"Settings panel for:\n{item.text()}\n\nConfiguration options coming soon!")

class DesktopEnvironment(QWidget):
    """Main desktop environment shell - like GNOME Shell"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pi iOS Desktop Environment")

        # Get screen geometry
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top panel
        self.top_panel = TopPanel()
        self.top_panel.show_activities.connect(self.show_activities)
        self.top_panel.power_btn.clicked.connect(self.show_power_menu)
        layout.addWidget(self.top_panel)

        # Desktop area (middle)
        self.desktop = DesktopArea()
        layout.addWidget(self.desktop, stretch=1)

        # Dock container (bottom with margins)
        dock_container = QWidget()
        dock_container.setStyleSheet("background: transparent;")
        dock_layout = QVBoxLayout()
        dock_layout.setContentsMargins(20, 0, 20, 15)

        self.dock = Dock()
        self.dock.app_launched.connect(self.launch_application)
        dock_layout.addWidget(self.dock, alignment=Qt.AlignCenter)

        dock_container.setLayout(dock_layout)
        layout.addWidget(dock_container)

        self.setLayout(layout)

        # Application launcher
        self.launcher = ApplicationLauncher(self)
        self.launcher.app_selected.connect(self.launch_application)

        # Track open windows
        self.open_windows = {}

        # Show desktop
        self.show()
        self.lower()  # Keep desktop behind other windows

    def show_activities(self):
        """Show the Activities overlay"""
        self.launcher.exec_()

    def launch_application(self, app_name):
        """Launch an application window"""

        # If window already open, raise it
        if app_name in self.open_windows and self.open_windows[app_name].isVisible():
            self.open_windows[app_name].raise_()
            self.open_windows[app_name].activateWindow()
            return

        # Create new window
        if app_name == "Files":
            window = FileManagerWindow()
        elif app_name == "Terminal":
            window = TerminalWindow()
        elif app_name == "Settings":
            window = SettingsWindow()
        elif app_name == "Browser":
            try:
                subprocess.Popen(["chromium-browser"])
                return
            except:
                QMessageBox.warning(self, "Browser", "Chromium not installed")
                return
        elif app_name == "Calculator":
            try:
                subprocess.Popen(["galculator"])
                return
            except:
                QMessageBox.warning(self, "Calculator", "Calculator not installed")
                return
        elif app_name == "Apps":
            self.show_activities()
            return
        elif app_name == "Power":
            self.show_power_menu()
            return
        else:
            QMessageBox.information(self, app_name, f"{app_name} will be available soon!")
            return

        # Show window
        window.show()
        window.raise_()
        window.activateWindow()
        self.open_windows[app_name] = window

    def show_power_menu(self):
        """Show power options menu"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 2px solid #667eea;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 30px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #667eea;
                color: white;
            }
        """)

        logout_action = menu.addAction("🚪 Logout")
        menu.addSeparator()
        reboot_action = menu.addAction("🔄 Reboot")
        shutdown_action = menu.addAction("⏻ Shutdown")

        # Show menu at cursor
        action = menu.exec_(QCursor.pos())

        if action == logout_action:
            self.power_action("logout")
        elif action == reboot_action:
            self.power_action("reboot")
        elif action == shutdown_action:
            self.power_action("shutdown")

    def power_action(self, action):
        """Execute power action"""
        reply = QMessageBox.question(self, "Confirm",
            f"Are you sure you want to {action}?",
            QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            if action == "shutdown":
                subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            elif action == "reboot":
                subprocess.run(['sudo', 'reboot'])
            elif action == "logout":
                QApplication.quit()

def main():
    """Main entry point for desktop environment"""

    # Set up environment
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'

    # Detect best platform
    if 'QT_QPA_PLATFORM' not in os.environ:
        if os.path.exists('/dev/fb0') and not os.environ.get('DISPLAY'):
            os.environ['QT_QPA_PLATFORM'] = 'linuxfb'

    # Disable Qt warnings
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

    # Create application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # Set font
    font = QFont("Arial", 10)
    app.setFont(font)

    # Create desktop environment
    desktop = DesktopEnvironment()

    # Handle signals
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, lambda *args: app.quit())

    # Run
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
