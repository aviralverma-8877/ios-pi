# Troubleshooting Guide - Pi iOS Launcher

## Display Issues

### Error: "qt.qpa.xcb: could not connect to display"

This error occurs when Qt cannot connect to the X server.

**Solutions:**

1. **Running from SSH?**
   ```bash
   # Enable X forwarding when connecting
   ssh -X pi@raspberrypi.local
   
   # Or set DISPLAY manually
   export DISPLAY=:0
   pi-ios-launcher
   ```

2. **Not in graphical session?**
   ```bash
   # Start the X server first
   startx
   
   # Then run launcher
   pi-ios-launcher
   ```

3. **Use the startup script:**
   ```bash
   chmod +x start-pi-ios.sh
   ./start-pi-ios.sh
   ```

4. **Run from the desktop terminal** (not SSH):
   - Open Terminal from Raspberry Pi Desktop
   - Run: `pi-ios-launcher`

### Error: "Could not load the Qt platform plugin"

**Solutions:**

1. **Try different platform plugins:**
   ```bash
   # Try X11 (most common)
   QT_QPA_PLATFORM=xcb pi-ios-launcher
   
   # Try framebuffer (no X required)
   QT_QPA_PLATFORM=linuxfb pi-ios-launcher
   
   # Try Wayland (if installed)
   QT_QPA_PLATFORM=wayland pi-ios-launcher
   ```

2. **Install missing Qt plugins:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y \
       python3-pyqt5 \
       python3-pyqt5.qtsvg \
       libqt5gui5 \
       qt5-qmltooling-plugins
   ```

3. **Check available plugins:**
   ```bash
   python3 -c "from PyQt5.QtWidgets import QApplication; import sys; app = QApplication(sys.argv)"
   ```

### Screen Resolution Wrong

**Solutions:**

1. **Edit boot configuration:**
   ```bash
   sudo nano /boot/config.txt
   ```

2. **Add these lines for 4.3" (800x480):**
   ```ini
   hdmi_group=2
   hdmi_mode=87
   hdmi_cvt=800 480 60 6 0 0 0
   ```

3. **For other resolutions:**
   - 480x320: `hdmi_cvt=480 320 60 6 0 0 0`
   - 640x480: `hdmi_cvt=640 480 60 6 0 0 0`
   - 1024x600: `hdmi_cvt=1024 600 60 6 0 0 0`

4. **Save and reboot:**
   ```bash
   sudo reboot
   ```

### Display is Rotated

Add to `/boot/config.txt`:
```ini
display_rotate=0  # 0°
# display_rotate=1  # 90°
# display_rotate=2  # 180°
# display_rotate=3  # 270°
```

## Touch Screen Issues

### Touch Not Working

1. **Check if touch device is detected:**
   ```bash
   ls /dev/input/event*
   xinput list
   ```

2. **Test touch input:**
   ```bash
   sudo apt-get install evtest
   sudo evtest
   # Select your touch device
   # Touch screen and verify events appear
   ```

3. **Set Qt touch device:**
   ```bash
   export QT_QPA_EVDEV_TOUCHSCREEN_PARAMETERS=/dev/input/event0
   pi-ios-launcher
   ```

### Touch Calibration Off

1. **Install calibration tool:**
   ```bash
   sudo apt-get install xinput-calibrator
   ```

2. **Run calibration:**
   ```bash
   DISPLAY=:0 xinput_calibrator
   ```

3. **Follow on-screen instructions** - touch the crosshairs

4. **Save configuration:**
   ```bash
   sudo nano /etc/X11/xorg.conf.d/99-calibration.conf
   ```

5. **Paste the calibration output** and reboot

## Permission Issues

### Error: "Permission denied" when accessing display

**Solutions:**

1. **Add user to video group:**
   ```bash
   sudo usermod -a -G video $USER
   sudo usermod -a -G input $USER
   sudo usermod -a -G tty $USER
   ```

2. **Log out and back in** for group changes to take effect

3. **Allow X server access:**
   ```bash
   xhost +local:
   ```

### Cannot write to framebuffer

```bash
sudo chmod 666 /dev/fb0
# Or better, add to video group (see above)
```

## Installation Issues

### Missing PyQt5

```bash
# Method 1: System package
sudo apt-get install python3-pyqt5

# Method 2: pip (if method 1 fails)
pip3 install PyQt5

# Method 3: Build from source (last resort)
sudo apt-get install python3-pyqt5-dev
```

### Package Installation Fails

```bash
# Fix dependencies
sudo apt-get install -f

# Clean package cache
sudo apt-get clean
sudo apt-get update

# Try installing again
sudo dpkg -i pi-ios-launcher_1.0.0_all.deb
```

## Performance Issues

### Launcher is Slow/Laggy

1. **Increase GPU memory** in `/boot/config.txt`:
   ```ini
   gpu_mem=256  # or 128, 192
   ```

2. **Disable unused services:**
   ```bash
   sudo systemctl disable bluetooth
   sudo systemctl disable hciuart
   ```

3. **Close other applications** before running

4. **Overclock** (optional, at your own risk):
   ```bash
   sudo raspi-config
   # Performance Options -> Overclock
   ```

### High Memory Usage

1. **Check memory:**
   ```bash
   free -h
   ```

2. **Close background apps:**
   ```bash
   ps aux | grep python
   killall chromium-browser  # If running
   ```

3. **Reduce app complexity** by editing the launcher code

## Application Errors

### Browser Won't Open

**Solution:**

1. **Install Chromium:**
   ```bash
   sudo apt-get install chromium-browser
   ```

2. **Or use different browser:**
   - Edit `pi_ios_launcher.py`
   - Line ~424, change `chromium-browser` to `firefox` or `midori`

### Calculator Not Available

```bash
sudo apt-get install galculator
```

### Terminal Commands Don't Work

1. **Check shell:**
   ```bash
   echo $SHELL
   ```

2. **Set proper shell in code** if needed

3. **Increase timeout** in terminal execution code

## Boot/Autostart Issues

### Launcher Doesn't Start on Boot

1. **Check autostart file exists:**
   ```bash
   cat ~/.config/lxsession/LXDE-pi/autostart
   ```

2. **Verify entry is correct:**
   ```
   @/usr/local/bin/pi-ios-launcher
   ```

3. **Check file permissions:**
   ```bash
   ls -l /usr/local/bin/pi-ios-launcher
   # Should be executable: -rwxr-xr-x
   ```

4. **Check logs:**
   ```bash
   journalctl -xe | grep pi-ios
   cat ~/.xsession-errors
   ```

### Black Screen on Boot

1. **Try booting to desktop normally**
2. **Remove autostart temporarily:**
   ```bash
   nano ~/.config/lxsession/LXDE-pi/autostart
   # Comment out the pi-ios-launcher line with #
   ```

3. **Reboot and debug** from desktop

## General Debugging

### Enable Debug Output

```bash
# Run with verbose Qt logging
export QT_LOGGING_RULES='*.debug=true'
pi-ios-launcher

# Or check system logs
journalctl -f | grep pi-ios
```

### Check Process

```bash
# See if launcher is running
ps aux | grep pi-ios

# Kill if stuck
killall pi-ios-launcher
```

### Test in Different Modes

```bash
# Test 1: Direct X11
DISPLAY=:0 python3 pi_ios_launcher.py

# Test 2: Framebuffer
QT_QPA_PLATFORM=linuxfb python3 pi_ios_launcher.py

# Test 3: With startup script
./start-pi-ios.sh
```

## Getting More Help

### Collect System Information

```bash
# Create debug report
cat > debug-info.txt << EOF
=== System Info ===
$(uname -a)
$(cat /proc/cpuinfo | grep Model)

=== Display Info ===
DISPLAY=$DISPLAY
$(xdpyinfo 2>&1 | head -20)

=== Qt Info ===
$(python3 -c "from PyQt5.QtCore import QT_VERSION_STR; print('Qt:', QT_VERSION_STR)")

=== Input Devices ===
$(ls -l /dev/input/)
$(xinput list)

=== Graphics ===
$(vcgencmd get_mem gpu)
$(tvservice -s)

=== Processes ===
$(ps aux | grep -E 'X|lx|python')
EOF

cat debug-info.txt
```

### Report Issues

Include in your bug report:
1. Error messages (full text)
2. How you're running the launcher
3. Your Pi model
4. Display type and size
5. Output of debug-info.txt
6. Steps to reproduce

## Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Can't connect to display | `export DISPLAY=:0` |
| Qt plugin error | Try `QT_QPA_PLATFORM=linuxfb` |
| Touch not working | Run `xinput_calibrator` |
| Wrong resolution | Edit `/boot/config.txt` |
| Permission denied | `sudo usermod -a -G video,input $USER` |
| Slow performance | Increase gpu_mem in `/boot/config.txt` |
| Won't start on boot | Check `~/.config/lxsession/LXDE-pi/autostart` |
| PyQt5 missing | `sudo apt-get install python3-pyqt5` |

## Still Having Issues?

1. **Use the startup script:** `./start-pi-ios.sh`
2. **Run from desktop terminal** not SSH
3. **Check README.md** for installation instructions
4. **Try a fresh install** of Raspberry Pi OS
5. **Report the issue** with debug information

---

Most issues are related to display/X server configuration. The startup script (`start-pi-ios.sh`) handles most common problems automatically.
