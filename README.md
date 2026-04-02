# Pi iOS Launcher

An iOS-like desktop interface for Raspberry Pi OS, optimized for 4.3-inch LCD touchscreen displays.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red)
![Python](https://img.shields.io/badge/python-3.7%2B-green)

## Features

- 🍎 **iOS-Style Interface**: Beautiful home screen with app grid layout
- 📱 **Touch Optimized**: Perfect for 4.3" touchscreen displays (800x480)
- ⚡ **Lightweight**: Minimal resource usage, runs smoothly on all Raspberry Pi models
- 🎨 **Modern Design**: Gradient backgrounds, rounded corners, smooth animations
- 📦 **Built-in Apps**:
  - File Manager with folder navigation
  - Terminal emulator
  - Settings panel
  - System status bar
  - Quick-launch dock

## Screenshots

```
┌────────────────────────────────────────┐
│  ●●●●●    12:45 PM              📶 🔋 │ Status Bar
├────────────────────────────────────────┤
│                                        │
│   ⚙️        📁        💻               │
│ Settings   Files   Terminal            │
│                                        │
│   🌐        🔢        📝               │
│ Browser  Calculator  Notes             │
│                                        │
│   📷        🎵        🎬               │
│  Photos    Music    Videos             │
│                                        │
├────────────────────────────────────────┤
│   📞      💬      📸                   │ Dock
│  Phone  Messages Camera                │
└────────────────────────────────────────┘
```

## Requirements

### Hardware
- Raspberry Pi (any model with Raspberry Pi OS)
- 4.3-inch LCD display (800x480 recommended)
- Touch screen support (optional but recommended)

### Software
- Raspberry Pi OS (Raspbian) Buster or newer
- Python 3.7 or higher
- PyQt5

## Installation

### Method 1: Install from .deb package (Recommended)

1. Build the package:
```bash
chmod +x build-deb.sh
./build-deb.sh
```

2. Install:
```bash
sudo dpkg -i pi-ios-launcher_1.0.0_all.deb
sudo apt-get install -f  # Install dependencies if needed
```

3. Launch:
```bash
pi-ios-launcher
```

Or find it in your applications menu under "Pi iOS Launcher"

### Method 2: Install from source

1. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3-pyqt5 python3-pip
pip3 install -r requirements.txt
```

2. Run directly:
```bash
chmod +x pi_ios_launcher.py
./pi_ios_launcher.py
```

## Configuration

### Display Setup

For optimal display on 4.3" screens (800x480), add to `/boot/config.txt`:

```ini
# 4.3" Display Configuration
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
hdmi_drive=1
```

Reboot after making changes:
```bash
sudo reboot
```

### Set as Default Desktop

To launch Pi iOS Launcher on startup:

1. Edit autostart file:
```bash
nano ~/.config/lxsession/LXDE-pi/autostart
```

2. Add this line:
```
@/usr/local/bin/pi-ios-launcher
```

3. Save and reboot

### Kiosk Mode (Fullscreen)

For a dedicated kiosk display:

1. Edit system autostart:
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

2. Comment out existing desktop and add:
```
#@lxpanel --profile LXDE-pi
#@pcmanfm --desktop --profile LXDE-pi
@/usr/local/bin/pi-ios-launcher
```

### Touch Calibration

If touch input is misaligned:

```bash
sudo apt-get install xinput-calibrator
xinput-calibrator
```

Follow on-screen instructions and save the configuration.

## Usage

### Navigation
- **Tap** app icons to launch apps
- **Home button** (bottom center) returns to home screen
- **Scroll** vertically to see more apps

### Built-in Apps

#### File Manager
- Browse files and folders
- Double-tap to open folders
- Back button to navigate up
- Home button returns to /home/pi

#### Terminal
- Execute shell commands
- View command output
- Full terminal access to Raspberry Pi

#### Settings
- System configuration options
- Wi-Fi, display, sound settings
- System information

### Launching External Apps

The launcher can open installed system applications:
- **Browser**: Opens Chromium
- **Calculator**: Opens Galculator
- More integrations coming soon

## Customization

### Adding New Apps

Edit `pi_ios_launcher.py` and add to the `apps` list in `HomePage.__init__()`:

```python
apps = [
    ("My App", "🎮", self.launch_callback),
    # Add more apps here
]
```

### Changing Theme Colors

Modify the gradient in `MainWindow.__init__()`:

```python
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #YOUR_COLOR_1, stop:1 #YOUR_COLOR_2);
```

### Icon Customization

Replace emoji icons in `AppIcon` definitions with custom icon files or different emojis.

## Troubleshooting

### Display Issues

**Problem**: Screen shows wrong resolution
**Solution**: Check `/boot/config.txt` settings match your display specs

**Problem**: Display is rotated
**Solution**: Add to `/boot/config.txt`:
```ini
display_rotate=1  # 0=0°, 1=90°, 2=180°, 3=270°
```

### Touch Input Issues

**Problem**: Touch not working
**Solution**: 
1. Check display drivers are installed
2. Run `xinput list` to verify touch device
3. Calibrate with `xinput-calibrator`

**Problem**: Touch offset/inaccurate
**Solution**: Run calibration tool and save configuration

### Performance Issues

**Problem**: Slow/laggy interface
**Solution**:
1. Reduce animation effects
2. Close background applications
3. Increase GPU memory in `/boot/config.txt`:
```ini
gpu_mem=128
```

### Installation Issues

**Problem**: Missing dependencies
**Solution**:
```bash
sudo apt-get update
sudo apt-get install -y python3-pyqt5 python3-pyqt5.qtsvg
```

**Problem**: Permission denied
**Solution**:
```bash
chmod +x pi_ios_launcher.py
sudo chmod +x /usr/local/bin/pi-ios-launcher
```

## Uninstallation

### If installed via .deb:
```bash
sudo apt-get remove pi-ios-launcher
```

### If installed from source:
```bash
rm ~/.local/bin/pi-ios-launcher  # If copied to PATH
# Remove autostart entries if configured
```

## Development

### Project Structure
```
pi-ios-launcher/
├── pi_ios_launcher.py    # Main application
├── setup.py              # Python package setup
├── requirements.txt      # Python dependencies
├── build-deb.sh         # Debian package builder
└── README.md            # This file
```

### Building from Source

1. Clone repository:
```bash
git clone https://github.com/yourusername/pi-ios-launcher.git
cd pi-ios-launcher
```

2. Install development dependencies:
```bash
pip3 install -e .
```

3. Run:
```bash
python3 pi_ios_launcher.py
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Created for Raspberry Pi enthusiasts who want a modern, touch-friendly interface on small displays.

## Support

- **Issues**: Report bugs and feature requests on GitHub Issues
- **Documentation**: See this README and inline code documentation
- **Community**: Join discussions on Raspberry Pi forums

## Roadmap

- [ ] Weather widget integration
- [ ] Music player with playlist support
- [ ] Photo gallery with slideshow
- [ ] System resource monitor
- [ ] Wi-Fi configuration GUI
- [ ] App store for additional widgets
- [ ] Custom theme support
- [ ] Multi-page home screen
- [ ] Notification center
- [ ] Dark mode

## Changelog

### Version 1.0.0 (2024)
- Initial release
- iOS-style home screen
- File manager, terminal, settings apps
- Touch optimization for 4.3" displays
- Debian package support

---

Made with ❤️ for Raspberry Pi
