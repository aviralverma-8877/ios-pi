# Migration Guide - Upgrading to GNOME-like Desktop

## From Old iOS Launcher App to New GNOME Desktop Environment

---

## Quick Migration (5 Minutes)

```bash
# 1. Uninstall old version
sudo apt-get remove pi-ios-launcher pi-ios-desktop
sudo apt-get autoremove

# 2. Pull latest code
cd ~/pi-ios-desktop  # or wherever you cloned
git pull origin main

# 3. Build new package
cd deb-build
chmod +x build-desktop-deb.sh
./build-desktop-deb.sh

# 4. Install new version
cd ..
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
sudo apt-get install -f

# 5. Set as default
sudo /usr/share/doc/pi-ios-desktop/set-default.sh

# 6. Reboot
sudo reboot
```

---

## Detailed Step-by-Step Migration

### Step 1: Check Current Installation

First, see if you have an old version installed:

```bash
# Check for installed packages
dpkg -l | grep pi-ios

# Check what's running
ps aux | grep pi_ios
```

### Step 2: Uninstall Old Version

#### If installed via .deb package:

```bash
# Remove the old package
sudo apt-get remove pi-ios-launcher
# OR
sudo apt-get remove pi-ios-desktop

# Clean up unused dependencies
sudo apt-get autoremove
```

#### If running manually:

```bash
# Just stop it if running
killall pi_ios_desktop.py
killall pi_ios_launcher.py
```

#### Clean up autostart entries:

```bash
# Remove from user autostart (if configured)
nano ~/.config/lxsession/LXDE-pi/autostart
# Remove any lines containing pi-ios

# Remove from system autostart (if configured)
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Remove any lines containing pi-ios
```

### Step 3: Update Your Repository

```bash
# Navigate to your project directory
cd ~/pi-ios-desktop  # or wherever you cloned it

# Pull latest changes
git pull origin main

# Verify you have the new version
git log --oneline -3
# Should show:
# 7320844 docs: add GNOME desktop architecture documentation
# 26dab05 feat: transform into GNOME-like desktop environment
# f21094d refactor: reorganize project structure
```

### Step 4: Build New Package

```bash
# Navigate to build directory
cd deb-build

# Make build script executable
chmod +x build-desktop-deb.sh

# Build the package
./build-desktop-deb.sh
```

You should see output like:
```
================================================
Pi iOS Desktop Environment - Package Builder
================================================

[1/7] Cleaning previous builds...
[2/7] Creating package structure...
[3/7] Creating control file...
[4/7] Creating post-installation script...
[5/7] Installing application files...
[6/7] Creating documentation...
[7/7] Building Debian package...

================================================
Package built successfully!
================================================

Package: pi-ios-desktop_1.0.0_all.deb
```

### Step 5: Install New Version

```bash
# Go back to project root
cd ..

# Install the package
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb

# Fix any dependency issues
sudo apt-get install -f
```

Expected output:
```
Selecting previously unselected package pi-ios-desktop.
Preparing to unpack pi-ios-desktop_1.0.0_all.deb ...
Unpacking pi-ios-desktop (1.0.0) ...
Setting up pi-ios-desktop (1.0.0) ...
Configuring Pi iOS Desktop Environment...
Pi iOS Desktop installed successfully!
```

### Step 6: Configure as Default Desktop

```bash
# Set Pi iOS Desktop as default
sudo /usr/share/doc/pi-ios-desktop/set-default.sh
```

This will:
- Configure LightDM to use Pi iOS Desktop
- Set up auto-login
- Configure the session

### Step 7: Reboot

```bash
sudo reboot
```

After reboot, you should see the new GNOME-like desktop!

---

## What's Different?

### Before (Old Launcher)

```
┌─────────────────────┐
│   Status Bar        │
├─────────────────────┤
│                     │
│   App Grid          │
│   (Fullscreen)      │
│                     │
├─────────────────────┤
│   Dock              │
│   ● Home Button     │
└─────────────────────┘
```

**Navigation:**
- Home button to return
- Tap apps → Takes over screen
- One screen at a time

### After (New GNOME Desktop)

```
┌─────────────────────┐
│ 🏠 Activities  ⏻    │ ← Panel (always visible)
├─────────────────────┤
│  ┌─────┐            │
│  │Win1 │ ┌─────┐    │ ← Desktop (windows)
│  └─────┘ │Win2 │    │
│          └─────┘    │
├─────────────────────┤
│  📁 💻 🌐 ⚙️ ⚡     │ ← Dock
└─────────────────────┘
```

**Navigation:**
- Activities button → Opens launcher
- Apps open as windows
- Multiple windows simultaneously
- Proper desktop environment

---

## Verification Checklist

After reboot, verify these work:

### ✓ Top Panel
- [ ] Top panel is visible
- [ ] Activities button is there
- [ ] Time displays correctly
- [ ] Temperature shows (if Pi has sensor)
- [ ] Power button responds

### ✓ Desktop
- [ ] Desktop background appears (purple gradient)
- [ ] Background stays behind windows

### ✓ Dock
- [ ] Dock visible at bottom
- [ ] All icons present (📁 💻 🌐 ⚙️ ⚡)
- [ ] Icons respond to clicks
- [ ] Hover effects work

### ✓ Applications
- [ ] Click Activities → Launcher opens
- [ ] Search bar works
- [ ] Apps launch as windows
- [ ] Files app opens
- [ ] Terminal opens
- [ ] Settings opens
- [ ] Multiple windows can be open

### ✓ Window Management
- [ ] Windows can be moved (drag title bar)
- [ ] Windows can be resized (drag edges)
- [ ] Windows can be closed (X button)
- [ ] Reopening app raises existing window

### ✓ Power Menu
- [ ] Power button shows menu
- [ ] Logout option works
- [ ] Reboot option works
- [ ] Shutdown option works

---

## Troubleshooting Migration

### Issue: Old version still appears

**Solution:**
```bash
# Force remove all old packages
sudo apt-get purge pi-ios-launcher pi-ios-desktop
sudo apt-get autoremove

# Clean up old files
sudo rm -f /usr/local/bin/pi-ios-launcher
sudo rm -f /usr/bin/pi-ios-launcher
sudo find /usr -name "*pi-ios*" -type f

# Remove any found files
sudo rm /path/to/old/file

# Then install new version
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
```

### Issue: Desktop doesn't appear at login

**Solution:**
```bash
# Check session file exists
ls -l /usr/share/xsessions/pi-ios-desktop.desktop

# Check executables exist
ls -l /usr/bin/pi-ios-desktop
ls -l /usr/bin/pi-ios-session

# Restart LightDM
sudo systemctl restart lightdm

# Or manually select at login
# At login screen, click session icon → Select "Pi iOS Desktop"
```

### Issue: Still seeing fullscreen app instead of desktop

**Solution:**
```bash
# Verify you have the latest version
python3 /usr/bin/pi-ios-desktop << 'EOF'
import sys
sys.path.insert(0, '/usr/bin')
exec(open('/usr/bin/pi-ios-desktop').read())
EOF

# Check for "TopPanel" and "DesktopEnvironment" classes
grep -n "class TopPanel" /usr/bin/pi-ios-desktop
grep -n "class DesktopEnvironment" /usr/bin/pi-ios-desktop

# If not found, you have old version
# Reinstall:
cd ~/pi-ios-desktop
git pull
cd deb-build
./build-desktop-deb.sh
cd ..
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb --force-overwrite
```

### Issue: Panel or dock not visible

**Solution:**
```bash
# Check display resolution
xrandr

# Ensure it's set to 800x480 (or your display size)
# Edit /boot/config.txt if needed
sudo nano /boot/config.txt

# Should have:
hdmi_group=2
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0

# Reboot if changed
sudo reboot
```

### Issue: Windows don't open

**Solution:**
```bash
# Check if OpenBox is running
ps aux | grep openbox

# If not running, start it
openbox &

# Check session script
cat /usr/bin/pi-ios-session

# Should start OpenBox before desktop
# If not, reinstall package
```

### Issue: Permission denied for power actions

**Solution:**
```bash
# Add sudo permissions
sudo visudo

# Add these lines (replace 'pi' with your username):
pi ALL=(ALL) NOPASSWD: /sbin/shutdown
pi ALL=(ALL) NOPASSWD: /sbin/reboot

# Save and exit (Ctrl+O, Enter, Ctrl+X)
```

---

## Rolling Back (If Needed)

If you want to go back to the old version:

```bash
# 1. Uninstall new version
sudo apt-get remove pi-ios-desktop

# 2. Reinstall LXDE (or previous desktop)
sudo apt-get install lxde

# 3. Set LXDE as default
sudo nano /etc/lightdm/lightdm.conf
# Change: user-session=LXDE-pi

# 4. Reboot
sudo reboot
```

Or keep old version from Git:

```bash
# Go to older commit
git checkout f21094d  # Before GNOME transformation

# Build old version
cd deb-build
./build-desktop-deb.sh
cd ..
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
```

---

## Side-by-Side Comparison

| Feature | Old Launcher | New GNOME Desktop |
|---------|-------------|-------------------|
| **Type** | Fullscreen app | Desktop environment |
| **Panel** | Status bar only | Top panel + dock |
| **Navigation** | Home button | Activities button |
| **Apps** | Take over screen | Open as windows |
| **Multitasking** | Limited | Full support |
| **Window mgmt** | None | Move/resize |
| **Workflow** | Mobile-like | Desktop-like |
| **Use case** | Launcher | Full desktop |

---

## Post-Migration Tips

### Customize Your Desktop

1. **Change wallpaper:**
   - Edit `/usr/bin/pi-ios-desktop`
   - Find `DesktopArea` class
   - Change gradient colors

2. **Add more dock apps:**
   - Edit `/usr/bin/pi-ios-desktop`
   - Find `Dock` class `dock_apps` list
   - Add your apps

3. **Change panel position:**
   - Currently top-only
   - Can be modified to bottom if desired

### Learn the New Workflow

1. **Launch apps:**
   - Click Activities OR
   - Click dock icon OR
   - Search in Activities overlay

2. **Manage windows:**
   - Drag title bar to move
   - Drag edges/corners to resize
   - Click X to close
   - Minimize via window manager (right-click title bar)

3. **Power options:**
   - Click ⏻ in top-right
   - Select action
   - Confirm

---

## Getting Help

If you encounter issues during migration:

1. Check logs:
   ```bash
   cat ~/.xsession-errors
   journalctl -xe | grep pi-ios
   ```

2. Test manually:
   ```bash
   DISPLAY=:0 /usr/bin/pi-ios-desktop
   ```

3. Verify installation:
   ```bash
   dpkg -L pi-ios-desktop
   ```

4. Check documentation:
   - `DESKTOP_ARCHITECTURE.md` - Technical details
   - `GNOME_TRANSFORMATION.txt` - What changed
   - `docs/TROUBLESHOOTING.md` - Common issues

---

## Summary

**Quick Migration:**
```bash
# Uninstall old
sudo apt-get remove pi-ios-launcher pi-ios-desktop

# Update code
cd ~/pi-ios-desktop && git pull

# Build new
cd deb-build && ./build-desktop-deb.sh

# Install new
cd .. && sudo dpkg -i pi-ios-desktop_1.0.0_all.deb

# Set default
sudo /usr/share/doc/pi-ios-desktop/set-default.sh

# Reboot
sudo reboot
```

**Result:** GNOME-like desktop with iOS aesthetics! 🎉

---

**Need more help?** Check `DESKTOP_ARCHITECTURE.md` for full technical details.
