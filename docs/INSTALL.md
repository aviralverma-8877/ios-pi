# Installation Guide - Pi iOS Desktop Environment

Complete installation guide for Raspberry Pi OS.

---

## Prerequisites

### Hardware
- Raspberry Pi (3, 4, or 5)
- 4.3-inch LCD display (800x480 recommended)
- Touch screen (optional but recommended)
- MicroSD card (8GB minimum, 16GB+ recommended)

### Software
- Raspberry Pi OS (Raspbian) Buster or newer
- Python 3.7+
- PyQt5
- OpenBox window manager
- LightDM display manager

---

## Quick Installation (Recommended)

```bash
# 1. Update system
sudo apt-get update
sudo apt-get upgrade -y

# 2. Build package
chmod +x build-desktop-deb.sh
./build-desktop-deb.sh

# 3. Install
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
sudo apt-get install -f

# 4. Set as default
sudo /usr/share/doc/pi-ios-desktop/set-default.sh

# 5. Reboot
sudo reboot
```

---

## Step-by-Step Installation

### Step 1: Prepare System

Update your Raspberry Pi:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

Install required packages:

```bash
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-pyqt5 \
    python3-pyqt5.qtsvg \
    openbox \
    lightdm \
    xinit \
    xserver-xorg \
    x11-xserver-utils
```

### Step 2: Configure Display

Edit boot configuration:

```bash
sudo nano /boot/config.txt
```

For 4.3" displays (800x480), add:

```ini
# Disable overscan
disable_overscan=1

# Force HDMI output
hdmi_force_hotplug=1

# Display resolution
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0

# HDMI drive mode
hdmi_drive=2

# GPU memory
gpu_mem=128

# Optional: Rotate display
# display_rotate=0  # 0°, 1=90°, 2=180°, 3=270°
```

Save (Ctrl+O, Enter, Ctrl+X) and reboot:

```bash
sudo reboot
```

### Step 3: Configure Touch Screen (If Applicable)

Test touch input:

```bash
xinput list
```

You should see your touch device listed.

Calibrate if needed:

```bash
sudo apt-get install xinput-calibrator
DISPLAY=:0 xinput_calibrator
```

Follow on-screen instructions, then save the configuration:

```bash
sudo nano /etc/X11/xorg.conf.d/99-calibration.conf
```

Paste the calibration output and save.

### Step 4: Install Pi iOS Desktop

#### Method A: Using Debian Package (Recommended)

Build the package:

```bash
chmod +x build-desktop-deb.sh
./build-desktop-deb.sh
```

This creates: `pi-ios-desktop_1.0.0_all.deb`

Install it:

```bash
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
```

Fix dependencies if needed:

```bash
sudo apt-get install -f
```

#### Method B: Manual Installation

Run the setup script:

```bash
chmod +x setup-desktop-environment.sh
sudo ./setup-desktop-environment.sh
```

Follow the prompts to complete installation.

### Step 5: Configure Desktop Environment

You have three options:

#### Option A: Auto-Boot (Dedicated Device)

Set Pi iOS as default desktop:

```bash
sudo /usr/share/doc/pi-ios-desktop/set-default.sh
sudo reboot
```

Your Pi will boot directly into the iOS desktop.

#### Option B: Select at Login (Shared Device)

Don't run the `set-default.sh` script. Instead:

1. Reboot: `sudo reboot`
2. At login screen, click the session icon (gear or similar)
3. Select "Pi iOS Desktop"
4. Login

This selection is remembered for future logins.

#### Option C: Manual Start (Testing)

Keep your current desktop and launch manually:

```bash
pi-ios-desktop
```

Or from the applications menu.

---

## Advanced Configuration

### Auto-Login Setup

Edit LightDM configuration:

```bash
sudo nano /etc/lightdm/lightdm.conf
```

Add or modify:

```ini
[Seat:*]
autologin-user=pi
autologin-user-timeout=0
user-session=pi-ios
greeter-session=lightdm-gtk-greeter
xserver-command=X -s 0 -dpms
```

Replace `pi` with your username if different.

### Sudo Permissions for Power Actions

Allow shutdown/reboot without password:

```bash
sudo visudo
```

Add at the end (replace `pi` with your username):

```
# Pi iOS Desktop power commands
pi ALL=(ALL) NOPASSWD: /sbin/shutdown
pi ALL=(ALL) NOPASSWD: /sbin/reboot
```

Save (Ctrl+O, Enter, Ctrl+X).

### Kiosk Mode (Fullscreen, No Escape)

For a locked-down kiosk:

1. Enable auto-login (see above)
2. Disable virtual terminals:

```bash
sudo systemctl mask getty@tty1.service
sudo systemctl mask getty@tty2.service
```

3. Disable Alt+F4 by editing `/usr/bin/pi-ios-desktop` (requires Python knowledge)

### Performance Tuning

Optimize for your Pi model:

```bash
sudo nano /boot/config.txt
```

Add:

```ini
# Increase GPU memory for better graphics
gpu_mem=256

# Disable Bluetooth if not needed
dtoverlay=disable-bt

# Optional: Overclock (Pi 4, at your own risk)
# over_voltage=6
# arm_freq=2000
```

Reboot after changes.

### Installing Additional Apps

Install apps that integrate with the desktop:

```bash
# Web browser
sudo apt-get install chromium-browser

# Calculator
sudo apt-get install galculator

# Text editor
sudo apt-get install leafpad

# Image viewer
sudo apt-get install gpicview

# Task manager
sudo apt-get install lxtask

# Screenshots
sudo apt-get install scrot
```

These apps will be accessible from the desktop.

---

## Post-Installation

### Verify Installation

Check files are in place:

```bash
# Main executable
ls -l /usr/bin/pi-ios-desktop

# Session files
ls -l /usr/bin/pi-ios-session
ls -l /usr/share/xsessions/pi-ios-desktop.desktop

# Documentation
ls -l /usr/share/doc/pi-ios-desktop/
```

### Test the Desktop

Before setting as default, test it:

```bash
pi-ios-desktop
```

Verify:
- [ ] Window opens fullscreen
- [ ] Status bar shows time
- [ ] App icons are visible
- [ ] Touch input works (if applicable)
- [ ] Home button returns to home screen
- [ ] Apps launch correctly

### First Run Checklist

After booting into Pi iOS Desktop:

- [ ] Display resolution is correct
- [ ] Touch screen responds accurately
- [ ] File manager opens and navigates
- [ ] Terminal executes commands
- [ ] System Info shows correct data
- [ ] Power menu responds
- [ ] External apps launch (browser, etc.)

---

## Troubleshooting Installation

### Package Installation Fails

**Error:** `dpkg: dependency problems`

**Solution:**

```bash
sudo apt-get update
sudo apt-get install -f
sudo apt-get install python3-pyqt5 openbox lightdm
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
```

### Desktop Doesn't Appear in Login Screen

**Solution:**

```bash
# Check session file
cat /usr/share/xsessions/pi-ios-desktop.desktop

# Restart LightDM
sudo systemctl restart lightdm
```

### Black Screen After Login

**Check logs:**

```bash
cat ~/.xsession-errors
journalctl -xe
```

**Common causes:**

1. Missing dependencies:
   ```bash
   sudo apt-get install python3-pyqt5 openbox
   ```

2. Display configuration issue:
   ```bash
   export DISPLAY=:0
   /usr/bin/pi-ios-desktop
   ```

3. Permission issues:
   ```bash
   sudo chmod +x /usr/bin/pi-ios-desktop
   sudo chmod +x /usr/bin/pi-ios-session
   ```

### Touch Screen Issues

**Not detected:**

```bash
# Check input devices
xinput list
ls -l /dev/input/

# Test manually
sudo evtest /dev/input/event0
```

**Misaligned:**

```bash
sudo apt-get install xinput-calibrator
xinput_calibrator
# Follow instructions
```

### Display Resolution Wrong

**Check current resolution:**

```bash
tvservice -s
xrandr
```

**Force specific resolution:**

Edit `/boot/config.txt` and verify settings match your display specs.

### Performance Issues

**Desktop is slow/laggy:**

1. Increase GPU memory:
   ```bash
   sudo nano /boot/config.txt
   # Set: gpu_mem=256
   ```

2. Disable unnecessary services:
   ```bash
   sudo systemctl disable bluetooth
   sudo systemctl disable hciuart
   ```

3. Close background apps:
   ```bash
   ps aux | grep python
   # Kill unnecessary processes
   ```

---

## Uninstallation

### Remove Desktop Environment

Using package manager:

```bash
sudo apt-get remove pi-ios-desktop
sudo apt-get autoremove
sudo systemctl restart lightdm
```

Using uninstall script:

```bash
chmod +x uninstall-desktop.sh
sudo ./uninstall-desktop.sh
```

### Manual Cleanup

If automatic removal didn't work:

```bash
# Remove files
sudo rm /usr/bin/pi-ios-desktop
sudo rm /usr/bin/pi-ios-session
sudo rm /usr/share/xsessions/pi-ios-desktop.desktop
sudo rm -rf /usr/share/doc/pi-ios-desktop/

# Restore LightDM config
sudo nano /etc/lightdm/lightdm.conf
# Change user-session back to LXDE-pi

# Restart
sudo systemctl restart lightdm
```

---

## Upgrading

To upgrade to a newer version:

```bash
# Remove old version
sudo apt-get remove pi-ios-desktop

# Install new version
sudo dpkg -i pi-ios-desktop_NEW_VERSION_all.deb
sudo apt-get install -f

# Reboot
sudo reboot
```

Settings and configurations are preserved.

---

## Network Installation

To install on multiple Pis:

1. Build package once:
   ```bash
   ./build-desktop-deb.sh
   ```

2. Copy `.deb` to other Pis via SSH:
   ```bash
   scp pi-ios-desktop_1.0.0_all.deb pi@raspberrypi:/home/pi/
   ```

3. Install on each Pi:
   ```bash
   ssh pi@raspberrypi
   sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
   sudo apt-get install -f
   sudo /usr/share/doc/pi-ios-desktop/set-default.sh
   sudo reboot
   ```

---

## Getting Help

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review logs: `cat ~/.xsession-errors`
3. Test manually: `DISPLAY=:0 /usr/bin/pi-ios-desktop`
4. Check dependencies: `dpkg -l | grep pyqt5`

---

## Next Steps

After successful installation:

1. Configure display resolution if needed
2. Calibrate touch screen
3. Install additional apps
4. Customize the interface (edit `/usr/bin/pi-ios-desktop`)
5. Set up auto-login for kiosk mode

---

**Installation complete!** Enjoy your Pi iOS Desktop Environment! 🎉
