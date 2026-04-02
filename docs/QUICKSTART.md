# Quick Start - Pi iOS Desktop Environment

## TL;DR - Boot Into iOS Desktop

```bash
# 1. Build & Install
chmod +x build-desktop-deb.sh
./build-desktop-deb.sh
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
sudo apt-get install -f

# 2. Make it default
sudo /usr/share/doc/pi-ios-desktop/set-default.sh

# 3. Reboot
sudo reboot
```

**Done!** Your Pi now boots into iOS-style desktop! 🎉

---

## What You Get

✅ **Boots directly** into iOS interface  
✅ **Replaces LXDE** (but you can switch back)  
✅ **Auto-login** to iOS desktop  
✅ **Touch optimized** for 4.3" displays  
✅ **Full desktop environment** with window management  

---

## Installation Options

### Option 1: Auto-Boot (Recommended)

```bash
./build-desktop-deb.sh
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
sudo /usr/share/doc/pi-ios-desktop/set-default.sh
sudo reboot
```

**Result**: Pi boots straight into iOS desktop every time

### Option 2: Choose at Login

```bash
./build-desktop-deb.sh
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
# Don't run set-default.sh
sudo reboot
```

**Result**: Select "Pi iOS Desktop" from login screen when you want it

### Option 3: Try First

```bash
sudo apt-get install -y python3-pyqt5 openbox
python3 pi_ios_desktop.py
```

**Result**: Test it before installing

---

## Display Configuration (One-Time)

For 4.3" displays, edit `/boot/config.txt`:

```bash
sudo nano /boot/config.txt
```

Add these lines:

```ini
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
gpu_mem=128
disable_overscan=1
```

Save (Ctrl+O, Enter, Ctrl+X), then:

```bash
sudo reboot
```

---

## Using the Desktop

### Navigation

- **Tap apps** to open them
- **Home button** (●) at bottom returns to home screen
- **Press Windows key** also returns home
- **Status bar** shows time and system info

### Built-in Apps

- **Terminal** 💻 - Full shell access
- **Files** 📁 - Browse your files
- **Browser** 🌐 - Web browsing (if installed)
- **System Info** ℹ️ - CPU, RAM, disk stats
- **Power** ⏻ - Shutdown, reboot, logout

### Installing More Apps

```bash
sudo apt-get install chromium-browser  # Web browser
sudo apt-get install galculator         # Calculator
sudo apt-get install scrot              # Screenshots
```

Apps appear automatically in the desktop!

---

## Switching Desktops

### Back to Normal Desktop (Temporary)

1. Logout (Power → Logout)
2. At login screen, click session icon
3. Select "LXDE-pi"
4. Login

### Back to Normal Desktop (Permanent)

```bash
sudo nano /etc/lightdm/lightdm.conf
```

Change:
```ini
user-session=pi-ios
```

To:
```ini
user-session=LXDE-pi
```

Reboot.

---

## Uninstall

```bash
sudo apt-get remove pi-ios-desktop
sudo reboot
```

Everything returns to normal automatically!

---

## Troubleshooting

### Desktop Doesn't Show Up

```bash
# Check it's installed
ls -l /usr/bin/pi-ios-desktop

# Restart login manager
sudo systemctl restart lightdm
```

### Black Screen After Login

```bash
# Check dependencies
sudo apt-get install -y python3-pyqt5 openbox

# Check logs
cat ~/.xsession-errors
```

### Can't Shutdown/Reboot from Power Menu

```bash
sudo visudo
```

Add:
```
pi ALL=(ALL) NOPASSWD: /sbin/shutdown
pi ALL=(ALL) NOPASSWD: /sbin/reboot
```

(Replace `pi` with your username)

### Touch Screen Not Working

```bash
sudo apt-get install xinput-calibrator
xinput_calibrator
```

---

## Usage Modes

**Auto-Boot Mode** (Default): Pi boots straight into iOS desktop
**Select Mode**: Choose at login screen
**Manual Mode**: Run `pi-ios-desktop` when needed

---

## Next Steps

1. ✅ Install and boot
2. 📱 Configure display for your screen
3. 🎨 Customize apps (edit `/usr/bin/pi-ios-desktop`)
4. 🔧 Install additional apps
5. ⚡ Optimize performance (increase gpu_mem)

---

## Files Created

After running `build-desktop-deb.sh`:

- `pi-ios-desktop_1.0.0_all.deb` - Installable package

After installing:

- `/usr/bin/pi-ios-desktop` - Main program
- `/usr/bin/pi-ios-session` - Session wrapper
- `/usr/share/xsessions/pi-ios-desktop.desktop` - Login entry
- `/usr/share/doc/pi-ios-desktop/` - Documentation

---

## Complete Documentation

- **[README.md](README.md)** - Full manual
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving
- **[INSTALL.md](INSTALL.md)** - Detailed installation

---

## One-Command Install (Copy-Paste Ready)

```bash
chmod +x build-desktop-deb.sh && ./build-desktop-deb.sh && sudo dpkg -i pi-ios-desktop_1.0.0_all.deb && sudo apt-get install -f && sudo /usr/share/doc/pi-ios-desktop/set-default.sh && sudo reboot
```

**Boom!** 💥 iOS desktop in one command!
