# Pi iOS Desktop Environment

A complete iOS-like desktop environment for Raspberry Pi that boots directly into an iOS-style interface. Optimized for 4.3-inch touchscreen displays.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Type](https://img.shields.io/badge/type-Desktop%20Environment-orange)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red)

## What's This?

A **full desktop environment** that:
- ✅ Boots directly into iOS-like interface
- ✅ Replaces the default LXDE desktop
- ✅ Appears in the login screen session selector
- ✅ Manages windows and applications
- ✅ Provides complete desktop functionality

## Features

### 🖥️ Full Desktop Environment
- Boots directly into iOS-style interface
- Selectable from login screen
- Window management for external apps
- System-wide integration

### 📱 iOS-Style Interface
- App grid with touch-optimized icons
- Status bar with time and system info
- Home button (press to return)
- App dock for quick access
- Smooth transitions

### 🛠️ Built-in Applications
- **File Manager**: Browse and open files
- **Terminal**: Full shell access
- **System Info**: CPU, memory, disk, network stats
- **Settings**: Quick access to system settings
- **Power Menu**: Shutdown, reboot, logout
- **External Apps**: Browser, calculator, text editor, etc.

### ⚙️ System Integration
- Works with existing Linux applications
- Power management (shutdown/reboot)
- Auto-login support
- Display configuration
- Touch input support

## Installation

### Quick Install

```bash
# 1. Build the package
cd deb-build
chmod +x build-desktop-deb.sh
./build-desktop-deb.sh

# 2. Install (package created in project root)
cd ..
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
sudo apt-get install -f

# 3. Set as default desktop (optional)
sudo /usr/share/doc/pi-ios-desktop/set-default.sh
sudo reboot
```

### Manual Setup

If you prefer to set up without package:

```bash
# 1. Install dependencies
sudo apt-get install -y python3 python3-pyqt5 openbox lightdm xinit

# 2. Run setup script
cd scripts
chmod +x setup-desktop-environment.sh
sudo ./setup-desktop-environment.sh
```

## Usage

### Three Ways to Use

#### Method 1: Set as Default (Auto-login)

Boot directly into Pi iOS Desktop:

```bash
sudo /usr/share/doc/pi-ios-desktop/set-default.sh
sudo reboot
```

Your Pi will now boot straight into the iOS-like interface!

#### Method 2: Select at Login

Keep your existing desktop and switch when needed:

1. Logout from current session
2. At the login screen, click the **session icon** (usually top-right)
3. Select **"Pi iOS Desktop"**
4. Login

#### Method 3: Try Without Installing

Test it first:

```bash
pi-ios-desktop
```

## Built-in Applications

### File Manager 📁
- Navigate folders
- Open files with default apps
- Quick access to home directory
- Visual folder/file icons

### Terminal 💻
- Execute shell commands
- View output
- Full system access
- Green-on-black retro style

### System Info ℹ️
- CPU temperature
- Memory usage
- Disk space
- Network information
- System details

### Power Menu ⏻
- Shutdown system
- Reboot
- Logout to login screen
- Confirmation dialogs

### External App Integration

Launch installed applications:
- **Browser**: Chromium (install: `sudo apt-get install chromium-browser`)
- **Calculator**: Galculator (install: `sudo apt-get install galculator`)
- **Text Editor**: Leafpad
- **Task Manager**: LXTask
- **Screenshots**: Scrot (install: `sudo apt-get install scrot`)

## Configuration

### Display Setup (4.3" Screen)

Edit `/boot/config.txt`:

```bash
sudo nano /boot/config.txt
```

Add:

```ini
# 4.3" Display Configuration (800x480)
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
hdmi_drive=2
gpu_mem=128
disable_overscan=1

# Optional: Rotate display
#display_rotate=0  # 0°, 1=90°, 2=180°, 3=270°
```

Save and reboot:

```bash
sudo reboot
```

### Touch Calibration

If touch input is misaligned:

```bash
sudo apt-get install xinput-calibrator
DISPLAY=:0 xinput_calibrator
```

Follow instructions and save calibration.

### Customizing Apps

Edit the desktop environment file:

```bash
sudo nano /usr/bin/pi-ios-desktop
```

Find the `apps` list around line 140 and add your apps:

```python
apps = [
    ("My App", "🎮", self.launch_callback),
    # Add more here
]
```

For external apps, add to `launch_app()` method:

```python
elif app_name == "My App":
    self.launch_external("my-command")
```

## Keyboard Shortcuts

- **Windows/Super Key**: Return to home screen
- **Alt+F4**: Close current app/return home
- **Ctrl+Alt+T**: Terminal (if configured)

## Architecture

### How It Works

```
Boot
  ↓
LightDM (Login Manager)
  ↓
Pi iOS Session (/usr/bin/pi-ios-session)
  ↓
Openbox (Window Manager - background)
  ↓
Pi iOS Desktop (/usr/bin/pi-ios-desktop)
  ↓
Your Apps
```

### Components

1. **pi_ios_desktop.py**: Main desktop environment
2. **pi-ios-session**: X session wrapper script
3. **pi-ios-desktop.desktop**: Session definition for login screen
4. **Openbox**: Lightweight window manager (handles external app windows)

### Files Installed

- `/usr/bin/pi-ios-desktop` - Main executable
- `/usr/bin/pi-ios-session` - Session wrapper
- `/usr/share/xsessions/pi-ios-desktop.desktop` - Session file
- `/usr/share/doc/pi-ios-desktop/` - Documentation
- `/etc/lightdm/lightdm.conf` - Display manager config (modified)

## Project Structure

```
pi-ios-desktop/
├── pi_ios_desktop.py           # Main desktop environment application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
├── deb-build/                  # Debian package building
│   ├── build-desktop-deb.sh    # Package builder script
│   ├── pi-ios-session          # X session wrapper
│   └── pi-ios-desktop.desktop  # Desktop session definition
├── scripts/                    # Installation and management scripts
│   ├── setup-desktop-environment.sh  # Manual installer
│   └── uninstall-desktop.sh    # Uninstaller script
└── docs/                       # Documentation
    ├── START-HERE.md           # Getting started guide
    ├── QUICKSTART.md           # Quick setup guide
    ├── INSTALL.md              # Detailed installation
    ├── TROUBLESHOOTING.md      # Problem solving
    ├── SUMMARY.txt             # Quick reference
    └── README-FIRST.txt        # Overview
```

## Desktop Environment Features

| Feature | Capability |
|---------|-----------|
| Boot behavior | Boots directly into interface |
| Login screen | Selectable session |
| Window management | Full WM support |
| System integration | Complete |
| Auto-login | Supported |
| External apps | Fully managed |
| Use case | Primary desktop interface |

## Switching Between Desktops

### Back to LXDE/Default Desktop

**Temporary** (one session):
1. Logout
2. Select "LXDE" or "LXDE-pi" at login
3. Login

**Permanent**:

```bash
# Edit LightDM config
sudo nano /etc/lightdm/lightdm.conf

# Change:
user-session=pi-ios

# To:
user-session=LXDE-pi

# Reboot
sudo reboot
```

### Keep Both

Don't set as default, just select at login when needed!

## Troubleshooting

### Desktop Doesn't Appear in Login Screen

```bash
# Check session file exists
ls -l /usr/share/xsessions/pi-ios-desktop.desktop

# Check executable exists
ls -l /usr/bin/pi-ios-desktop
ls -l /usr/bin/pi-ios-session

# Restart login manager
sudo systemctl restart lightdm
```

### Black Screen After Login

```bash
# Check logs
cat ~/.xsession-errors

# Try from terminal
DISPLAY=:0 /usr/bin/pi-ios-desktop

# Check dependencies
dpkg -l | grep pyqt5
```

### Can't Shutdown/Reboot

```bash
# Fix sudo permissions
sudo visudo

# Add these lines:
pi ALL=(ALL) NOPASSWD: /sbin/shutdown
pi ALL=(ALL) NOPASSWD: /sbin/reboot
```

(Replace `pi` with your username)

### External Apps Don't Open

```bash
# Install missing apps
sudo apt-get install chromium-browser  # Browser
sudo apt-get install galculator         # Calculator
sudo apt-get install leafpad            # Text editor
sudo apt-get install lxtask             # Task manager
sudo apt-get install scrot              # Screenshots
```

### Touch Not Working

```bash
# Install calibration tool
sudo apt-get install xinput-calibrator

# Run calibration
xinput_calibrator

# Follow instructions
```

### Performance Issues

Edit `/boot/config.txt`:

```ini
# Increase GPU memory
gpu_mem=256

# Overclock (optional, at your own risk)
# See: sudo raspi-config
```

## Uninstallation

### Remove Package

```bash
sudo apt-get remove pi-ios-desktop
sudo systemctl restart lightdm
```

This automatically restores your previous desktop configuration.

### Manual Uninstall

```bash
chmod +x uninstall-desktop.sh
sudo ./uninstall-desktop.sh
```

## Development

### Project Structure

```
pi-ios-desktop/
├── pi_ios_desktop.py          # Main desktop environment
├── pi-ios-session             # X session wrapper
├── pi-ios-desktop.desktop     # Session definition
├── build-desktop-deb.sh       # Package builder
├── setup-desktop-environment.sh  # Manual installer
├── uninstall-desktop.sh       # Uninstaller
└── DESKTOP-README.md          # This file
```

### Testing Changes

```bash
# Edit the desktop file
nano pi_ios_desktop.py

# Test without installing
python3 pi_ios_desktop.py

# Or rebuild and reinstall
./build-desktop-deb.sh
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
```

### Adding Apps

1. Add app icon to home screen:

```python
# In HomePage.__init__(), apps list:
apps = [
    ("My New App", "🆕", self.launch_callback),
]
```

2. Add app handler:

```python
# In DesktopEnvironment.launch_app():
elif app_name == "My New App":
    self.launch_external("my-app-command")
```

3. Rebuild and reinstall

## Advanced

### Creating Kiosk Mode

For a locked-down kiosk:

```bash
# Edit /usr/bin/pi-ios-desktop
# Add after line: self.showFullScreen()

# Disable Alt+F4
def keyPressEvent(self, event):
    if event.key() == Qt.Key_F4:
        event.ignore()
```

### Custom Themes

Edit gradient colors:

```python
# Find in pi_ios_desktop.py:
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #YOUR_COLOR_1, stop:1 #YOUR_COLOR_2);
```

### Multi-User Support

Each user can choose their desktop:

```bash
# User 1 uses Pi iOS Desktop
# User 2 uses LXDE
# Each selects at login
```

## FAQ

**Q: Does this replace my entire desktop?**  
A: You can choose! Set it as default OR select when needed at login.

**Q: Can I still use my regular desktop?**  
A: Yes! Just select "LXDE" or your default desktop at the login screen.

**Q: Will my files and apps be affected?**  
A: No! This only changes the desktop interface, not your files or applications.

**Q: Can I uninstall it?**  
A: Absolutely. `sudo apt-get remove pi-ios-desktop` and it's gone.

**Q: Does it work with other Raspberry Pi models?**  
A: Yes! Works on Pi 3, 4, and 5. Optimized for 4.3" displays but works on any screen.

**Q: Can I use this without a touchscreen?**  
A: Yes! Mouse and keyboard work perfectly.

**Q: Is this production-ready?**  
A: It's stable for personal use, kiosks, and projects. Test thoroughly for critical applications.

## Support

- **Documentation**: See this file and `/usr/share/doc/pi-ios-desktop/`
- **Issues**: Report bugs on GitHub
- **Community**: Raspberry Pi forums

## License

MIT License - Free to use, modify, and distribute!

## Credits

Created for Raspberry Pi enthusiasts who want a modern, touch-friendly desktop environment.

---

**Boot directly into iOS-style beauty! 🍎🥧**
