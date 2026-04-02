#!/bin/bash
#
# Debian Package Builder for Pi iOS Launcher
# Usage: ./build-deb.sh
#

set -e

# Configuration
APP_NAME="pi-ios-launcher"
VERSION="1.0.0"
ARCH="all"
MAINTAINER="Pi iOS Team <info@pi-ios.local>"
DESCRIPTION="iOS-like interface for Raspberry Pi with 4.3 inch display"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Pi iOS Launcher - Debian Package Builder${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Clean previous builds
echo -e "${YELLOW}[1/6]${NC} Cleaning previous builds..."
rm -rf build dist *.egg-info debian-pkg
mkdir -p debian-pkg

# Create directory structure
echo -e "${YELLOW}[2/6]${NC} Creating package structure..."
PKG_DIR="debian-pkg/${APP_NAME}_${VERSION}_${ARCH}"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/local/bin"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/share/pixmaps"
mkdir -p "$PKG_DIR/usr/share/doc/${APP_NAME}"
mkdir -p "$PKG_DIR/etc/xdg/autostart"

# Create control file
echo -e "${YELLOW}[3/6]${NC} Creating DEBIAN/control file..."
cat > "$PKG_DIR/DEBIAN/control" << EOF
Package: ${APP_NAME}
Version: ${VERSION}
Section: x11
Priority: optional
Architecture: ${ARCH}
Depends: python3 (>= 3.7), python3-pyqt5, python3-pip
Maintainer: ${MAINTAINER}
Description: ${DESCRIPTION}
 A modern iOS-like desktop interface optimized for Raspberry Pi
 with 4.3 inch LCD displays. Features include:
  - iOS-style home screen with app grid
  - Touch-optimized interface
  - Built-in file manager, terminal, and settings
  - Status bar with time and system info
  - Dock with favorite apps
  - Perfect for small touchscreen displays
Homepage: https://github.com/pi-ios-launcher
EOF

# Create postinst script
echo -e "${YELLOW}[4/6]${NC} Creating post-installation script..."
cat > "$PKG_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

echo "Configuring Pi iOS Launcher..."

# Install Python dependencies if pip is available
if command -v pip3 &> /dev/null; then
    pip3 install -q PyQt5 2>/dev/null || true
fi

# Make executable
chmod +x /usr/local/bin/pi-ios-launcher

echo "Pi iOS Launcher installed successfully!"
echo ""
echo "To start the launcher:"
echo "  1. Run: pi-ios-launcher"
echo "  2. Or use the desktop icon: 'Pi iOS Launcher'"
echo ""
echo "To set as default desktop:"
echo "  1. Edit ~/.config/lxsession/LXDE-pi/autostart"
echo "  2. Add: @/usr/local/bin/pi-ios-launcher"
echo ""

exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/postinst"

# Create prerm script
cat > "$PKG_DIR/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
echo "Removing Pi iOS Launcher..."
exit 0
EOF
chmod 755 "$PKG_DIR/DEBIAN/prerm"

# Copy main application
echo -e "${YELLOW}[5/6]${NC} Installing application files..."
cp pi_ios_launcher.py "$PKG_DIR/usr/local/bin/pi-ios-launcher"
chmod +x "$PKG_DIR/usr/local/bin/pi-ios-launcher"

# Create desktop entry
cat > "$PKG_DIR/usr/share/applications/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Pi iOS Launcher
Comment=iOS-like interface for Raspberry Pi
Exec=/usr/local/bin/pi-ios-launcher
Icon=pi-ios-launcher
Terminal=false
Categories=System;Utility;
StartupNotify=true
EOF

# Create autostart entry (optional)
cat > "$PKG_DIR/etc/xdg/autostart/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Pi iOS Launcher
Comment=iOS-like interface for Raspberry Pi
Exec=/usr/local/bin/pi-ios-launcher
Icon=pi-ios-launcher
Terminal=false
Categories=System;
X-GNOME-Autostart-enabled=false
EOF

# Create a simple icon (text-based)
cat > "$PKG_DIR/usr/share/pixmaps/${APP_NAME}.xpm" << 'EOF'
/* XPM */
static char * pi_ios_launcher_xpm[] = {
"32 32 3 1",
" 	c None",
".	c #667eea",
"+	c #764ba2",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
"................................",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
".....+++++++++++++++++++++.....",
"................................",
"................................"};
EOF

# Create README
cat > "$PKG_DIR/usr/share/doc/${APP_NAME}/README" << EOF
Pi iOS Launcher v${VERSION}
============================

An iOS-like desktop interface for Raspberry Pi with 4.3" displays.

Features:
- iOS-style home screen with app grid
- Touch-optimized interface
- Built-in apps (File Manager, Terminal, Settings)
- Status bar with time and indicators
- App dock for quick access

Usage:
------
Run from terminal: pi-ios-launcher
Or launch from applications menu: Pi iOS Launcher

Configuration:
--------------
To set as default desktop environment:
1. Edit: ~/.config/lxsession/LXDE-pi/autostart
2. Add line: @/usr/local/bin/pi-ios-launcher

For kiosk mode (fullscreen on boot):
1. Edit: /etc/xdg/lxsession/LXDE-pi/autostart
2. Add: @/usr/local/bin/pi-ios-launcher

Display Optimization:
--------------------
For best results on 4.3" displays (800x480), add to /boot/config.txt:
  hdmi_group=2
  hdmi_mode=87
  hdmi_cvt=800 480 60 6 0 0 0

Touch Calibration:
------------------
If touch input needs calibration, use: xinput-calibrator

Support:
--------
Report issues at: https://github.com/pi-ios-launcher/issues

License: MIT
EOF

# Create copyright file
cat > "$PKG_DIR/usr/share/doc/${APP_NAME}/copyright" << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: pi-ios-launcher
Source: https://github.com/pi-ios-launcher

Files: *
Copyright: 2024 Pi iOS Team
License: MIT
 Permission is hereby granted, free of charge, to any person obtaining a
 copy of this software and associated documentation files (the "Software"),
 to deal in the Software without restriction, including without limitation
 the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following conditions:
 .
 The above copyright notice and this permission notice shall be included
 in all copies or substantial portions of the Software.
 .
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 DEALINGS IN THE SOFTWARE.
EOF

# Build the package
echo -e "${YELLOW}[6/6]${NC} Building Debian package..."
dpkg-deb --build "$PKG_DIR"

# Move to output directory
DEB_FILE="${APP_NAME}_${VERSION}_${ARCH}.deb"
mv "debian-pkg/${DEB_FILE}" .

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Package built successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Package: ${GREEN}${DEB_FILE}${NC}"
echo -e "Size: $(du -h ${DEB_FILE} | cut -f1)"
echo ""
echo "Installation:"
echo -e "  ${YELLOW}sudo dpkg -i ${DEB_FILE}${NC}"
echo -e "  ${YELLOW}sudo apt-get install -f${NC}  (if dependencies missing)"
echo ""
echo "Removal:"
echo -e "  ${YELLOW}sudo apt-get remove ${APP_NAME}${NC}"
echo ""
echo "Package info:"
echo -e "  ${YELLOW}dpkg -I ${DEB_FILE}${NC}"
echo ""
