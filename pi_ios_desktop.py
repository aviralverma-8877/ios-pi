#!/usr/bin/env python3
"""
Pi iOS Desktop Environment - Complete desktop environment for Raspberry Pi
Boot directly into iOS-like interface
"""

import sys
import os
import subprocess
import signal
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QWidget, QGridLayout,
                             QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QScrollArea, QFrame, QListWidget,
                             QTextEdit, QLineEdit, QMessageBox, QMenu, QSystemTrayIcon)
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QProcess, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QCursor, QPixmap, QPainter

class WindowManager:
    """Simple window manager to track and manage application windows"""
    def __init__(self):
        self.windows = []
        self.active_window = None

    def add_window(self, process, name):
        self.windows.append({'process': process, 'name': name, 'pid': process.pid()})

    def remove_window(self, process):
        self.windows = [w for w in self.windows if w['process'] != process]

    def kill_all(self):
        for window in self.windows:
            try:
                window['process'].kill()
            except:
                pass

class StatusBar(QWidget):
    """iOS-like status bar with system info"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                color: white;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        # Time label
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 10, QFont.Bold))

        # System info
        self.system_label = QLabel()
        self.system_label.setFont(QFont("Arial", 9))

        # Status indicators
        self.status_label = QLabel("⚡ 🌡️ 📡")
        self.status_label.setFont(QFont("Arial", 10))

        layout.addWidget(self.time_label)
        layout.addWidget(self.system_label)
        layout.addStretch()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Update every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)
        self.update_info()

    def update_info(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)

        # Get system info
        try:
            # CPU temp
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read().strip()) / 1000
                self.system_label.setText(f" {temp:.0f}°C")
        except:
            self.system_label.setText("")

class AppIcon(QPushButton):
    """iOS-style app icon button"""
    def __init__(self, name, icon_text, callback, parent=None):
        super().__init__(parent)
        self.app_name = name
        self.callback = callback

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
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 220);
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
    """iOS-like home screen"""
    def __init__(self, launch_callback, parent=None):
        super().__init__(parent)
        self.launch_callback = launch_callback

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 80)
        main_layout.setSpacing(20)

        # Scrollable app grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # System apps
        apps = [
            ("Terminal", "💻", self.launch_callback),
            ("Files", "📁", self.launch_callback),
            ("Browser", "🌐", self.launch_callback),
            ("Settings", "⚙️", self.launch_callback),
            ("Calculator", "🔢", self.launch_callback),
            ("Text Editor", "📝", self.launch_callback),
            ("Task Manager", "📊", self.launch_callback),
            ("System Info", "ℹ️", self.launch_callback),
            ("Screenshot", "📷", self.launch_callback),
            ("Music", "🎵", self.launch_callback),
            ("Videos", "🎬", self.launch_callback),
            ("Images", "🖼️", self.launch_callback),
            ("Network", "📡", self.launch_callback),
            ("Power", "🔋", self.launch_callback),
            ("Shutdown", "⏻", self.launch_callback),
        ]

        # 3 columns for 4.3" display
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

        # Dock
        dock = self.create_dock()
        main_layout.addWidget(dock)

        self.setLayout(main_layout)

    def create_dock(self):
        """Create app dock"""
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

        # Quick access apps
        dock_apps = [
            ("Terminal", "💻", self.launch_callback),
            ("Files", "📁", self.launch_callback),
            ("Browser", "🌐", self.launch_callback),
        ]

        for app_name, icon, callback in dock_apps:
            btn = AppIcon(app_name, icon, callback)
            btn.setFixedSize(60, 60)
            layout.addWidget(btn)

        dock.setLayout(layout)
        return dock

class FileManager(QWidget):
    """File manager app"""
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
        self.current_path = os.path.expanduser("~")
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
        else:
            # Open file with default app
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

class Terminal(QWidget):
    """Terminal emulator"""
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Output
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

        # Input
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
        self.output.append("Pi iOS Terminal\n$ ")

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

class SystemInfoApp(QWidget):
    """System information display"""
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet("""
            QTextEdit {
                background: white;
                border-radius: 10px;
                padding: 10px;
                font-family: monospace;
                font-size: 10px;
            }
        """)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_info)

        layout.addWidget(self.info_text)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)
        self.load_info()

    def load_info(self):
        info = []

        # System info
        try:
            info.append("=== SYSTEM INFORMATION ===\n")

            # OS
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if 'PRETTY_NAME' in line:
                        info.append(line.strip())

            # Kernel
            uname = subprocess.check_output(['uname', '-r']).decode().strip()
            info.append(f"Kernel: {uname}\n")

            # CPU
            info.append("\n=== CPU ===")
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line or 'Model' in line:
                        info.append(line.strip())
                        break

            # Temperature
            try:
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                    temp = int(f.read().strip()) / 1000
                    info.append(f"Temperature: {temp:.1f}°C")
            except:
                pass

            # Memory
            info.append("\n=== MEMORY ===")
            mem = subprocess.check_output(['free', '-h']).decode()
            info.append(mem)

            # Disk
            info.append("\n=== DISK USAGE ===")
            disk = subprocess.check_output(['df', '-h', '/']).decode()
            info.append(disk)

            # Network
            info.append("\n=== NETWORK ===")
            try:
                ip = subprocess.check_output(['hostname', '-I']).decode().strip()
                info.append(f"IP Address: {ip}")
            except:
                pass

        except Exception as e:
            info.append(f"Error loading system info: {e}")

        self.info_text.setText('\n'.join(info))

class DesktopEnvironment(QWidget):
    """Main desktop environment shell"""

    shutdown_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pi iOS Desktop")
        self.window_manager = WindowManager()

        # Make fullscreen
        self.showFullScreen()

        # Set background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Status bar
        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)

        # Content area (stacked pages)
        self.stack = QStackedWidget()

        # Home page
        self.home_page = HomePage(self.launch_app)
        self.stack.addWidget(self.home_page)

        # Built-in apps
        self.file_manager = FileManager()
        self.stack.addWidget(self.file_manager)

        self.terminal = Terminal()
        self.stack.addWidget(self.terminal)

        self.system_info = SystemInfoApp()
        self.stack.addWidget(self.system_info)

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
            QPushButton:hover {
                color: #ffff00;
            }
        """)
        home_btn.clicked.connect(self.go_home)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Handle keyboard shortcuts
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Handle global keyboard shortcuts"""
        if event.type() == event.KeyPress:
            # Alt+F4 to quit app (not shutdown system)
            if event.key() == Qt.Key_F4 and event.modifiers() == Qt.AltModifier:
                self.go_home()
                return True
            # Super/Windows key for home
            elif event.key() == Qt.Key_Meta:
                self.go_home()
                return True
        return super().eventFilter(obj, event)

    def launch_app(self, app_name):
        """Launch application"""
        if app_name == "Files":
            self.stack.setCurrentWidget(self.file_manager)
            self.file_manager.load_directory()

        elif app_name == "Terminal":
            self.stack.setCurrentWidget(self.terminal)

        elif app_name == "System Info":
            self.stack.setCurrentWidget(self.system_info)
            self.system_info.load_info()

        elif app_name == "Browser":
            self.launch_external("chromium-browser", "--start-maximized")

        elif app_name == "Calculator":
            self.launch_external("galculator")

        elif app_name == "Text Editor":
            self.launch_external("leafpad")

        elif app_name == "Screenshot":
            try:
                screenshot_path = os.path.expanduser("~/Pictures/screenshot.png")
                subprocess.run(['scrot', screenshot_path])
                QMessageBox.information(self, "Screenshot", f"Saved to {screenshot_path}")
            except:
                QMessageBox.warning(self, "Screenshot", "Install scrot: sudo apt-get install scrot")

        elif app_name == "Task Manager":
            self.launch_external("lxtask")

        elif app_name == "Settings":
            QMessageBox.information(self, "Settings",
                "System Settings\n\n"
                "• Display: Edit /boot/config.txt\n"
                "• Network: Use nmtui or network icon\n"
                "• Date/Time: timedatectl\n"
                "• More: sudo raspi-config")

        elif app_name == "Power":
            self.show_power_menu()

        elif app_name == "Shutdown":
            self.show_power_menu()

        else:
            QMessageBox.information(self, app_name, f"{app_name} coming soon!")

    def launch_external(self, command, *args):
        """Launch external application"""
        try:
            process = QProcess(self)
            process.start(command, list(args))
            if process.waitForStarted():
                self.window_manager.add_window(process, command)
            else:
                QMessageBox.warning(self, "Error",
                    f"Could not start {command}\nMake sure it's installed.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to launch {command}: {e}")

    def show_power_menu(self):
        """Show power options"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Power Options")
        msg.setText("What would you like to do?")
        msg.setIcon(QMessageBox.Question)

        shutdown_btn = msg.addButton("Shutdown", QMessageBox.ActionRole)
        reboot_btn = msg.addButton("Reboot", QMessageBox.ActionRole)
        logout_btn = msg.addButton("Logout", QMessageBox.ActionRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)

        msg.exec_()

        if msg.clickedButton() == shutdown_btn:
            self.power_action("shutdown")
        elif msg.clickedButton() == reboot_btn:
            self.power_action("reboot")
        elif msg.clickedButton() == logout_btn:
            self.power_action("logout")

    def power_action(self, action):
        """Execute power action"""
        confirm = QMessageBox.question(self, "Confirm",
            f"Are you sure you want to {action}?",
            QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            if action == "shutdown":
                subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            elif action == "reboot":
                subprocess.run(['sudo', 'reboot'])
            elif action == "logout":
                self.shutdown_signal.emit()
                QApplication.quit()

    def go_home(self):
        """Return to home screen"""
        self.stack.setCurrentWidget(self.home_page)

    def closeEvent(self, event):
        """Handle window close"""
        self.window_manager.kill_all()
        event.accept()

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
    font = QFont("Arial", 11)
    app.setFont(font)

    # Create desktop environment
    desktop = DesktopEnvironment()
    desktop.show()

    # Handle signals for clean shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, lambda *args: app.quit())

    # Run
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
