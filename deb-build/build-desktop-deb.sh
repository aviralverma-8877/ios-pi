#!/bin/bash
#
# Debian Package Builder for Pi iOS Desktop Environment
# Creates a full desktop environment package
#

set -e

# Configuration
APP_NAME="pi-ios-desktop"
VERSION="1.0.0"
ARCH="all"
MAINTAINER="Pi iOS Team <info@pi-ios.local>"
DESCRIPTION="iOS-like Desktop Environment for Raspberry Pi"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Pi iOS Desktop Environment - Package Builder${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Clean
echo -e "${YELLOW}[1/7]${NC} Cleaning previous builds..."
rm -rf build dist *.egg-info debian-pkg
mkdir -p debian-pkg

# Create structure
echo -e "${YELLOW}[2/7]${NC} Creating package structure..."
PKG_DIR="debian-pkg/${APP_NAME}_${VERSION}_${ARCH}"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/usr/share/xsessions"
mkdir -p "$PKG_DIR/usr/share/doc/${APP_NAME}"
mkdir -p "$PKG_DIR/usr/share/pixmaps"

# Control file
echo -e "${YELLOW}[3/7]${NC} Creating control file..."
cat > "$PKG_DIR/DEBIAN/control" << EOF
Package: ${APP_NAME}
Version: ${VERSION}
Section: x11
Priority: optional
Architecture: ${ARCH}
Depends: python3 (>= 3.7), python3-pyqt5, openbox, lightdm, x11-xserver-utils, xinit, xserver-xorg
Maintainer: ${MAINTAINER}
Description: ${DESCRIPTION}
 A complete iOS-like desktop environment for Raspberry Pi
 with 4.3 inch LCD displays. Features include:
  - Full desktop environment that boots directly
  - iOS-style interface with app grid
  - Touch-optimized for small displays
  - Built-in file manager, terminal, system info
  - Window management for external apps
  - Power management (shutdown, reboot)
  - Selectable from login screen
Homepage: https://github.com/pi-ios-desktop
EOF

# Post-install script
echo -e "${YELLOW}[4/7]${NC} Creating installation scripts..."
cat > "$PKG_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

echo "Configuring Pi iOS Desktop Environment..."

# Get the user who invoked sudo
ACTUAL_USER="${SUDO_USER:-pi}"

# Configure LightDM if it exists
if [ -f /etc/lightdm/lightdm.conf ]; then
    # Backup
    cp /etc/lightdm/lightdm.conf /etc/lightdm/lightdm.conf.pi-ios-backup 2>/dev/null || true
fi

# Add sudo permissions for power commands
if ! grep -q "# Pi iOS Desktop power commands" /etc/sudoers 2>/dev/null; then
    echo "" >> /etc/sudoers
    echo "# Pi iOS Desktop power commands" >> /etc/sudoers
    echo "$ACTUAL_USER ALL=(ALL) NOPASSWD: /sbin/shutdown" >> /etc/sudoers
    echo "$ACTUAL_USER ALL=(ALL) NOPASSWD: /sbin/reboot" >> /etc/sudoers
fi

echo ""
echo "================================================================"
echo "  Pi iOS Desktop Environment installed successfully!"
echo "================================================================"
echo ""
echo "To use Pi iOS Desktop:"
echo ""
echo "  Option 1: Set as default (auto-login)"
echo "    Run: sudo /usr/share/doc/pi-ios-desktop/set-default.sh"
echo ""
echo "  Option 2: Select at login"
echo "    1. Logout"
echo "    2. Click the session icon at login screen"
echo "    3. Select 'Pi iOS Desktop'"
echo "    4. Login"
echo ""
echo "  Option 3: Try it now"
echo "    Run: pi-ios-desktop"
echo ""
echo "Documentation: /usr/share/doc/pi-ios-desktop/"
echo ""

exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/postinst"

# Pre-remove script
cat > "$PKG_DIR/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e

# If this is the current session, warn user
if [ "$XDG_CURRENT_DESKTOP" = "PIOS" ]; then
    echo "Warning: You are currently running Pi iOS Desktop."
    echo "The desktop will be removed, but you'll need to logout/reboot."
fi

exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/prerm"

# Post-remove script
cat > "$PKG_DIR/DEBIAN/postrm" << 'EOF'
#!/bin/bash
set -e

# Remove sudo entries
sed -i '/# Pi iOS Desktop power commands/,+2d' /etc/sudoers 2>/dev/null || true

# Restore LightDM config if backup exists
if [ -f /etc/lightdm/lightdm.conf.pi-ios-backup ]; then
    mv /etc/lightdm/lightdm.conf.pi-ios-backup /etc/lightdm/lightdm.conf 2>/dev/null || true
fi

echo "Pi iOS Desktop Environment has been removed."

exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/postrm"

# Install files
echo -e "${YELLOW}[5/7]${NC} Installing application files..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Main desktop executable
cp "$PROJECT_ROOT/pi_ios_desktop.py" "$PKG_DIR/usr/bin/pi-ios-desktop"
chmod +x "$PKG_DIR/usr/bin/pi-ios-desktop"

# Session wrapper
cp "$SCRIPT_DIR/pi-ios-session" "$PKG_DIR/usr/bin/pi-ios-session"
chmod +x "$PKG_DIR/usr/bin/pi-ios-session"

# Desktop session file
cp "$SCRIPT_DIR/pi-ios-desktop.desktop" "$PKG_DIR/usr/share/xsessions/"

# Icon (simple text-based)
cat > "$PKG_DIR/usr/share/pixmaps/${APP_NAME}.xpm" << 'EOF'
/* XPM */
static char * pi_ios_desktop_xpm[] = {
"32 32 3 1",
" 	c None",
".	c #667eea",
"+	c #764ba2",
"................................",
"................................",
"..........          ............",
".........            ...........",
".......                .........",
"......     ......        .......",
".....    ..........       ......",
"....    ............      ......",
"...    ..............     ......",
"...   ...............+    .....+",
"..    ..............++    .....+",
"..   ...............++    .....+",
"..   ..............+++    .....+",
"..   .............++++    .....+",
"..   ............+++++   ......+",
"..    ..........++++++   ......+",
"..    .........+++++++   ......+",
"...   ........++++++++  .......+",
"...    ......+++++++++  .......+",
"....    ....++++++++++  .......+",
".....    ..+++++++++++  .......+",
"......     +++++++++++........++",
".......   ++++++++++++.......+++",
"........  +++++++++++++.....++++",
".........+++++++++++++++...+++++",
"........++++++++++++++++++++++++ ",
".......++++++++++++++++++++++++  ",
"......++++++++++++++++++++++     ",
".....+++++++++++++++++++++       ",
"....++++++++++++++++++++         ",
"..+++++++++++++++++++            ",
"................................"};
EOF

# Documentation
echo -e "${YELLOW}[6/7]${NC} Creating documentation..."

# Helper script to set as default
cat > "$PKG_DIR/usr/share/doc/${APP_NAME}/set-default.sh" << 'EOF'
#!/bin/bash
# Set Pi iOS Desktop as default

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo $0"
    exit 1
fi

ACTUAL_USER="${SUDO_USER:-pi}"

echo "Setting Pi iOS Desktop as default for user: $ACTUAL_USER"

# Configure LightDM
cat > /etc/lightdm/lightdm.conf << CONF
[Seat:*]
autologin-user=$ACTUAL_USER
autologin-user-timeout=0
user-session=pi-ios
greeter-session=lightdm-gtk-greeter
xserver-command=X -s 0 -dpms
CONF

# Set user default session
mkdir -p /home/$ACTUAL_USER/.dmrc
cat > /home/$ACTUAL_USER/.dmrc << CONF
[Desktop]
Session=pi-ios
CONF
chown $ACTUAL_USER:$ACTUAL_USER /home/$ACTUAL_USER/.dmrc

echo "Done! Reboot or restart LightDM to apply changes."
echo "  Restart LightDM: sudo systemctl restart lightdm"
echo "  Reboot: sudo reboot"
EOF
chmod +x "$PKG_DIR/usr/share/doc/${APP_NAME}/set-default.sh"

# README
cat > "$PKG_DIR/usr/share/doc/${APP_NAME}/README" << EOF
Pi iOS Desktop Environment v${VERSION}
======================================

A complete iOS-like desktop environment for Raspberry Pi.

FEATURES:
---------
• Full desktop environment (boots directly into it)
• iOS-style app grid and interface
• Touch-optimized for 4.3" displays
• Built-in apps: File Manager, Terminal, System Info
• Window management for external applications
• Power menu (shutdown, reboot, logout)
• Selectable from login screen

USAGE:
------
After installation, you have three options:

1. Set as default desktop (auto-login):
   sudo /usr/share/doc/pi-ios-desktop/set-default.sh
   sudo reboot

2. Select at login screen:
   - Logout
   - At login screen, click session icon
   - Select "Pi iOS Desktop"
   - Login

3. Try without making default:
   pi-ios-desktop

KEYBOARD SHORTCUTS:
-------------------
• Windows/Super key: Return to home screen
• Alt+F4: Close current app (return to home)

CUSTOMIZATION:
--------------
Edit /usr/bin/pi-ios-desktop to customize apps and appearance.

DISPLAY CONFIGURATION:
----------------------
For 4.3" displays, add to /boot/config.txt:
  hdmi_group=2
  hdmi_mode=87
  hdmi_cvt=800 480 60 6 0 0 0
  gpu_mem=128

UNINSTALL:
----------
  sudo apt-get remove pi-ios-desktop

To restore original desktop:
  sudo systemctl restart lightdm

SUPPORT:
--------
Report issues at: https://github.com/pi-ios-desktop/issues

LICENSE: MIT
EOF

# Copyright
cat > "$PKG_DIR/usr/share/doc/${APP_NAME}/copyright" << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: pi-ios-desktop
Source: https://github.com/pi-ios-desktop

Files: *
Copyright: 2024 Pi iOS Team
License: MIT
EOF

# Build package
echo -e "${YELLOW}[7/7]${NC} Building Debian package..."
dpkg-deb --build "$PKG_DIR"

# Move to output
DEB_FILE="${APP_NAME}_${VERSION}_${ARCH}.deb"
mv "debian-pkg/${DEB_FILE}" .

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Package built successfully!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "Package: ${GREEN}${DEB_FILE}${NC}"
echo -e "Size: $(du -h ${DEB_FILE} | cut -f1)"
echo ""
echo "INSTALLATION:"
echo -e "  ${YELLOW}sudo dpkg -i ${DEB_FILE}${NC}"
echo -e "  ${YELLOW}sudo apt-get install -f${NC}  (if dependencies missing)"
echo ""
echo "SET AS DEFAULT DESKTOP:"
echo -e "  ${YELLOW}sudo /usr/share/doc/pi-ios-desktop/set-default.sh${NC}"
echo -e "  ${YELLOW}sudo reboot${NC}"
echo ""
echo "OR SELECT AT LOGIN:"
echo "  1. Logout from current desktop"
echo "  2. At login screen, click the session icon"
echo "  3. Select 'Pi iOS Desktop'"
echo "  4. Login"
echo ""
echo "UNINSTALL:"
echo -e "  ${YELLOW}sudo apt-get remove pi-ios-desktop${NC}"
echo ""
