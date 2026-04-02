# Installation Guide - Pi iOS Launcher

Complete installation guide for Raspberry Pi OS.

## Quick Start (5 Minutes)

```bash
# 1. Download or clone the repository
cd ~
git clone https://github.com/yourusername/pi-ios-launcher.git
cd pi-ios-launcher

# 2. Build the Debian package
chmod +x build-deb.sh
./build-deb.sh

# 3. Install
sudo dpkg -i pi-ios-launcher_1.0.0_all.deb
sudo apt-get install -f

# 4. Run
pi-ios-launcher
```

## Detailed Installation Steps

### Step 1: Prepare Your Raspberry Pi

1. **Update System**:
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

2. **Install Required Packages**:
```bash
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-pyqt5 \
    python3-pyqt5.qtsvg \
    git \
    dpkg-dev
```

### Step 2: Configure Your 4.3" Display

1. **Identify Your Display**:
```bash
tvservice -s  # Check current display status
```

2. **Edit Boot Configuration**:
```bash
sudo nano /boot/config.txt
```

3. **Add Display Settings** (example for 800x480):
```ini
# Disable overscan if black borders appear
disable_overscan=1

# Force HDMI output
hdmi_force_hotplug=1

# Set display resolution for 4.3" (800x480)
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0

# Set HDMI drive mode
hdmi_drive=2

# Increase GPU memory for better performance
gpu_mem=128

# Optional: Rotate display if needed (0, 90, 180, 270)
#display_rotate=0
```

4. **Save and Reboot**:
```bash
sudo reboot
```

### Step 3: Set Up Touch Screen (If Applicable)

1. **Test Touch Input**:
```bash
xinput list  # Should show your touch device
```

2. **Calibrate Touch** (if needed):
```bash
sudo apt-get install -y xinput-calibrator
DISPLAY=:0 xinput_calibrator
```

3. **Save Calibration**:
   - Follow on-screen instructions
   - Copy the output configuration
   - Add to: `sudo nano /etc/X11/xorg.conf.d/99-calibration.conf`

### Step 4: Install Pi iOS Launcher

#### Option A: Using Debian Package (Recommended)

1. **Get the Files**:
```bash
cd ~
git clone https://github.com/yourusername/pi-ios-launcher.git
cd pi-ios-launcher
```

Or download as ZIP and extract.

2. **Build the Package**:
```bash
chmod +x build-deb.sh
./build-deb.sh
```

You should see:
```
========================================
Pi iOS Launcher - Debian Package Builder
========================================

[1/6] Cleaning previous builds...
[2/6] Creating package structure...
[3/6] Creating DEBIAN/control file...
[4/6] Creating post-installation script...
[5/6] Installing application files...
[6/6] Building Debian package...

========================================
Package built successfully!
========================================

Package: pi-ios-launcher_1.0.0_all.deb
```

3. **Install the Package**:
```bash
sudo dpkg -i pi-ios-launcher_1.0.0_all.deb
```

4. **Fix Dependencies** (if needed):
```bash
sudo apt-get install -f
```

#### Option B: Manual Installation

1. **Install Python Dependencies**:
```bash
pip3 install PyQt5
```

2. **Copy Files**:
```bash
sudo cp pi_ios_launcher.py /usr/local/bin/pi-ios-launcher
sudo chmod +x /usr/local/bin/pi-ios-launcher
```

3. **Create Desktop Entry**:
```bash
sudo nano /usr/share/applications/pi-ios-launcher.desktop
```

Add:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Pi iOS Launcher
Comment=iOS-like interface for Raspberry Pi
Exec=/usr/local/bin/pi-ios-launcher
Icon=application-default-icon
Terminal=false
Categories=System;Utility;
StartupNotify=true
```

### Step 5: Launch and Test

1. **Test from Terminal**:
```bash
pi-ios-launcher
```

2. **Or from Applications Menu**:
   - Open Start Menu
   - Look for "Pi iOS Launcher"
   - Click to launch

### Step 6: Set as Default Desktop (Optional)

#### For Current User Only:

1. **Edit Autostart**:
```bash
mkdir -p ~/.config/lxsession/LXDE-pi
nano ~/.config/lxsession/LXDE-pi/autostart
```

2. **Add Launcher**:
```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@/usr/local/bin/pi-ios-launcher
```

#### For Kiosk Mode (Fullscreen on Boot):

1. **Edit System Autostart**:
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

2. **Replace Content**:
```
@xset s off
@xset -dpms
@xset s noblank
@/usr/local/bin/pi-ios-launcher
```

3. **Disable Screen Blanking**:
```bash
sudo nano /etc/lightdm/lightdm.conf
```

Add under `[Seat:*]`:
```ini
xserver-command=X -s 0 -dpms
```

4. **Reboot**:
```bash
sudo reboot
```

## Advanced Configuration

### Auto-Start on Boot (Systemd Service)

1. **Create Service File**:
```bash
sudo nano /etc/systemd/system/pi-ios-launcher.service
```

2. **Add Configuration**:
```ini
[Unit]
Description=Pi iOS Launcher
After=graphical.target

[Service]
Type=simple
User=pi
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/pi/.Xauthority"
ExecStart=/usr/local/bin/pi-ios-launcher
Restart=on-failure

[Install]
WantedBy=graphical.target
```

3. **Enable Service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pi-ios-launcher.service
sudo systemctl start pi-ios-launcher.service
```

4. **Check Status**:
```bash
sudo systemctl status pi-ios-launcher.service
```

### Performance Tuning

1. **Optimize Memory**:
```bash
sudo nano /boot/config.txt
```

Add:
```ini
# Reduce GPU memory if not using graphics-heavy apps
gpu_mem=64

# Or increase for better graphics performance
gpu_mem=256
```

2. **Disable Unnecessary Services**:
```bash
sudo systemctl disable bluetooth.service
sudo systemctl disable hciuart.service
```

3. **Overclock** (optional, with caution):
```bash
sudo raspi-config
# Navigate to: Performance Options -> Overclock
```

### Network Configuration

To configure Wi-Fi through the interface:

1. **Install Network Manager**:
```bash
sudo apt-get install network-manager network-manager-gnome
```

2. **Edit launcher to integrate**:
Modify `pi_ios_launcher.py` to add network management features.

## Troubleshooting Installation

### Issue: Package Installation Fails

**Error**: `dpkg: dependency problems`

**Solution**:
```bash
sudo apt-get update
sudo apt-get install -f
sudo apt-get install python3-pyqt5
```

### Issue: Python Module Not Found

**Error**: `ModuleNotFoundError: No module named 'PyQt5'`

**Solution**:
```bash
pip3 install --user PyQt5
# Or system-wide:
sudo apt-get install python3-pyqt5
```

### Issue: Display Not Working

**Error**: Black screen or wrong resolution

**Solution**:
1. Check cable connections
2. Verify `/boot/config.txt` settings
3. Try different `hdmi_mode` values
4. Check `tvservice -s` output

### Issue: Touch Not Responding

**Solution**:
1. Check device: `xinput list`
2. Test: `evtest /dev/input/event0` (adjust event number)
3. Recalibrate: `xinput_calibrator`

### Issue: Permission Denied

**Error**: `Permission denied: '/usr/local/bin/pi-ios-launcher'`

**Solution**:
```bash
sudo chmod +x /usr/local/bin/pi-ios-launcher
sudo chown root:root /usr/local/bin/pi-ios-launcher
```

## Verification Checklist

After installation, verify:

- [ ] Display shows correct resolution (800x480)
- [ ] Touch input works (if applicable)
- [ ] Launcher starts without errors
- [ ] Home screen displays app grid
- [ ] Status bar shows time
- [ ] File manager opens and navigates
- [ ] Terminal executes commands
- [ ] Settings panel accessible
- [ ] Home button returns to main screen
- [ ] External apps launch (browser, calculator)

## Next Steps

1. **Customize**: Edit `pi_ios_launcher.py` to add your apps
2. **Configure**: Set up autostart and display preferences
3. **Optimize**: Adjust performance settings for your Pi model
4. **Expand**: Add more apps and features

## Getting Help

If you encounter issues:

1. Check the [README.md](README.md) troubleshooting section
2. Review system logs: `journalctl -xe`
3. Test in terminal: `python3 /usr/local/bin/pi-ios-launcher`
4. Report issues on GitHub with error logs

## Uninstallation

To remove Pi iOS Launcher:

```bash
# If installed via .deb:
sudo apt-get remove pi-ios-launcher
sudo apt-get autoremove

# Manual cleanup:
sudo rm /usr/local/bin/pi-ios-launcher
sudo rm /usr/share/applications/pi-ios-launcher.desktop
rm -rf ~/.config/pi-ios-launcher
```

---

**Installation complete!** 🎉

Run `pi-ios-launcher` to start your iOS-like interface.
