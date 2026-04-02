# 🎯 Pi iOS Desktop Environment

**Boot your Raspberry Pi directly into an iOS-like interface!**

Optimized for 4.3-inch touchscreen displays (800x480).

---

## ⚡ Quick Install

```bash
# 1. Build the package
chmod +x build-desktop-deb.sh
./build-desktop-deb.sh

# 2. Install
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
sudo apt-get install -f

# 3. Set as default (auto-boot into iOS desktop)
sudo /usr/share/doc/pi-ios-desktop/set-default.sh

# 4. Reboot
sudo reboot
```

**That's it!** Your Pi now boots into an iOS-style desktop! 🎉

---

## 🖥️ What You Get

✅ **Full Desktop Environment** - Boots directly into iOS interface  
✅ **Touch Optimized** - Perfect for 4.3" displays  
✅ **App Grid** - iOS-style home screen with icons  
✅ **File Manager** - Browse files and folders  
✅ **Terminal** - Full shell access  
✅ **System Info** - CPU, RAM, disk, network stats  
✅ **Power Menu** - Shutdown, reboot, logout  
✅ **Window Management** - Handles external apps  
✅ **Status Bar** - Time and system information  

---

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[README.md](README.md)** - Complete manual
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Fix problems
- **[INSTALL.md](INSTALL.md)** - Detailed installation

---

## 🖥️ Display Configuration

For 4.3" displays (800x480), edit `/boot/config.txt`:

```bash
sudo nano /boot/config.txt
```

Add:
```ini
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
gpu_mem=128
disable_overscan=1
```

Reboot:
```bash
sudo reboot
```

---

## 🎯 Usage Options

### Option 1: Set as Default (Auto-boot)
```bash
sudo /usr/share/doc/pi-ios-desktop/set-default.sh
sudo reboot
```
Pi boots straight into iOS desktop every time.

### Option 2: Select at Login
Don't run `set-default.sh`. Instead:
1. Logout
2. Click session icon at login screen
3. Select "Pi iOS Desktop"
4. Login

### Option 3: Try Without Installing
```bash
sudo apt-get install -y python3-pyqt5 openbox
python3 pi_ios_desktop.py
```

---

## 🆘 Quick Troubleshooting

**Desktop doesn't show at login:**
```bash
ls -l /usr/share/xsessions/pi-ios-desktop.desktop
sudo systemctl restart lightdm
```

**"Could not connect to display" error:**
```bash
# Run from Pi desktop terminal, not SSH
export DISPLAY=:0
python3 pi_ios_desktop.py
```

**Touch screen not working:**
```bash
sudo apt-get install xinput-calibrator
xinput_calibrator
```

**Can't shutdown/reboot:**
```bash
sudo visudo
# Add: pi ALL=(ALL) NOPASSWD: /sbin/shutdown
# Add: pi ALL=(ALL) NOPASSWD: /sbin/reboot
```

📖 **Full troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🗑️ Uninstall

```bash
# Using package manager
sudo apt-get remove pi-ios-desktop
sudo reboot

# Or using script
chmod +x uninstall-desktop.sh
sudo ./uninstall-desktop.sh
```

Your original desktop (LXDE) is automatically restored.

---

## 📦 Files Included

**Main Files:**
- `pi_ios_desktop.py` - Desktop environment
- `pi-ios-session` - X session wrapper
- `pi-ios-desktop.desktop` - Login screen entry

**Installation:**
- `build-desktop-deb.sh` - Build .deb package
- `setup-desktop-environment.sh` - Manual installer
- `uninstall-desktop.sh` - Uninstaller

**Documentation:**
- `README.md` - Complete manual
- `QUICKSTART.md` - Fast start guide
- `INSTALL.md` - Detailed installation
- `TROUBLESHOOTING.md` - Problem solving

---

## 🚀 Next Steps

1. **Read** [QUICKSTART.md](QUICKSTART.md) for 5-minute setup
2. **Build** the package
3. **Install** and configure display
4. **Reboot** into your iOS desktop!

---

## 🎨 Features in Detail

### Home Screen
- iOS-style app grid (3 columns)
- Touch-optimized icons
- App dock at bottom
- Smooth scrolling

### Built-in Apps
- **Files** 📁 - Navigate folders, open files
- **Terminal** 💻 - Full command line access
- **System Info** ℹ️ - Real-time system stats
- **Browser** 🌐 - Launch Chromium
- **Calculator** 🔢 - Galculator integration
- **Power** ⏻ - Shutdown/reboot/logout

### Status Bar
- Current time
- CPU temperature
- System indicators

### Window Management
- Launches and manages external apps
- OpenBox integration
- Clean interface

---

## 💡 Pro Tips

- **Kiosk Mode**: Enable auto-login for dedicated displays
- **Multi-User**: Each user can choose their desktop at login
- **Custom Apps**: Edit `pi_ios_desktop.py` to add your apps
- **Performance**: Increase `gpu_mem` in `/boot/config.txt` for smoothness

---

## 📄 License

MIT License - Free to use, modify, and share!

---

## 🎉 Ready to Transform Your Pi?

**Read:** [QUICKSTART.md](QUICKSTART.md)  
**Build:** `./build-desktop-deb.sh`  
**Enjoy:** Your iOS-style Raspberry Pi! 🥧📱
