#!/bin/bash
#
# Quick Migration Script - Upgrade to GNOME-like Desktop
# Removes old version and installs new GNOME desktop environment
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║       Pi iOS Desktop - Migration to GNOME Desktop            ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/cpuinfo ] || ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo -e "${YELLOW}Warning: This doesn't appear to be a Raspberry Pi${NC}"
    echo -e "${YELLOW}Continue anyway? [y/N]${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Migration cancelled."
        exit 0
    fi
fi

echo -e "${YELLOW}This will:${NC}"
echo "  1. Remove old Pi iOS launcher/desktop"
echo "  2. Pull latest code from git"
echo "  3. Build new GNOME-like desktop package"
echo "  4. Install the new version"
echo "  5. Set as default desktop"
echo "  6. Reboot your system"
echo ""
echo -e "${YELLOW}Continue? [y/N]${NC}"
read -r confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Migration cancelled."
    exit 0
fi

echo ""
echo -e "${GREEN}[1/7]${NC} Removing old version..."
sudo apt-get remove -y pi-ios-launcher pi-ios-desktop 2>/dev/null || echo "No old package found (OK)"
sudo apt-get autoremove -y

echo ""
echo -e "${GREEN}[2/7]${NC} Cleaning up old files..."
sudo rm -f /usr/local/bin/pi-ios-launcher 2>/dev/null || true
sudo rm -f /usr/bin/pi-ios-launcher 2>/dev/null || true

echo ""
echo -e "${GREEN}[3/7]${NC} Updating repository..."
if [ -d ".git" ]; then
    git pull origin main
    echo "Repository updated!"
else
    echo -e "${YELLOW}Not a git repository. Skipping git pull.${NC}"
    echo "Make sure you have the latest files!"
fi

echo ""
echo -e "${GREEN}[4/7]${NC} Building new package..."
if [ ! -f "deb-build/build-desktop-deb.sh" ]; then
    echo -e "${RED}Error: build-desktop-deb.sh not found!${NC}"
    echo "Make sure you're in the pi-ios-desktop directory"
    exit 1
fi

cd deb-build
chmod +x build-desktop-deb.sh
./build-desktop-deb.sh
cd ..

if [ ! -f "pi-ios-desktop_1.0.0_all.deb" ]; then
    echo -e "${RED}Error: Package build failed!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}[5/7]${NC} Installing new version..."
sudo dpkg -i pi-ios-desktop_1.0.0_all.deb
sudo apt-get install -f -y

echo ""
echo -e "${GREEN}[6/7]${NC} Setting as default desktop..."
if [ -f "/usr/share/doc/pi-ios-desktop/set-default.sh" ]; then
    sudo /usr/share/doc/pi-ios-desktop/set-default.sh
else
    echo -e "${YELLOW}Warning: set-default.sh not found${NC}"
    echo "You can set it manually after reboot"
fi

echo ""
echo -e "${GREEN}[7/7]${NC} Migration complete!"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Old version removed${NC}"
echo -e "${GREEN}✓ New GNOME-like desktop installed${NC}"
echo -e "${GREEN}✓ Configured as default${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}What's new:${NC}"
echo "  • Top panel with Activities button"
echo "  • Desktop background (not fullscreen)"
echo "  • Dock at bottom with favorites"
echo "  • Apps open as windows"
echo "  • Multiple windows simultaneously"
echo "  • GNOME-like workflow"
echo ""
echo -e "${YELLOW}Reboot now? [Y/n]${NC}"
read -r reboot_response

if [[ ! "$reboot_response" =~ ^[Nn]$ ]]; then
    echo ""
    echo -e "${BLUE}Rebooting in 3 seconds...${NC}"
    sleep 3
    sudo reboot
else
    echo ""
    echo "Please reboot manually when ready:"
    echo "  ${YELLOW}sudo reboot${NC}"
fi
