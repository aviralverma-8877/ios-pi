#!/bin/bash
#
# Pi iOS Desktop Environment Setup Script
# Makes Pi iOS the default desktop environment
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Pi iOS Desktop Environment Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root: sudo $0${NC}"
    exit 1
fi

echo -e "${GREEN}[1/6]${NC} Installing required packages..."
apt-get update -qq
apt-get install -y \
    python3 \
    python3-pyqt5 \
    openbox \
    lightdm \
    x11-xserver-utils \
    xinit \
    xserver-xorg \
    -qq 2>&1 | grep -v "^Reading" || true

echo -e "${GREEN}[2/6]${NC} Installing Pi iOS Desktop files..."

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Copy main desktop executable
cp "$PROJECT_ROOT/pi_ios_desktop.py" /usr/bin/pi-ios-desktop
chmod +x /usr/bin/pi-ios-desktop

# Copy session file
cp "$PROJECT_ROOT/deb-build/pi-ios-session" /usr/bin/pi-ios-session
chmod +x /usr/bin/pi-ios-session

echo -e "${GREEN}[3/6]${NC} Creating desktop session..."

# Create xsessions directory if it doesn't exist
mkdir -p /usr/share/xsessions

# Install desktop session file
cp "$PROJECT_ROOT/deb-build/pi-ios-desktop.desktop" /usr/share/xsessions/

echo -e "${GREEN}[4/6]${NC} Configuring LightDM..."

# Configure LightDM to show Pi iOS in session list
if [ -f /etc/lightdm/lightdm.conf ]; then
    # Backup original
    cp /etc/lightdm/lightdm.conf /etc/lightdm/lightdm.conf.backup
fi

# Create or update lightdm config
cat > /etc/lightdm/lightdm.conf << 'EOF'
[Seat:*]
autologin-user=pi
autologin-user-timeout=0
user-session=pi-ios
greeter-session=lightdm-gtk-greeter
xserver-command=X -s 0 -dpms
EOF

echo -e "${GREEN}[5/6]${NC} Setting up auto-login..."

# Get the actual username (in case not 'pi')
ACTUAL_USER="${SUDO_USER:-pi}"

# Set autologin user
sed -i "s/autologin-user=.*/autologin-user=$ACTUAL_USER/" /etc/lightdm/lightdm.conf

# Configure default session for user
mkdir -p /home/$ACTUAL_USER/.dmrc
cat > /home/$ACTUAL_USER/.dmrc << 'EOF'
[Desktop]
Session=pi-ios
EOF
chown $ACTUAL_USER:$ACTUAL_USER /home/$ACTUAL_USER/.dmrc

echo -e "${GREEN}[6/6]${NC} Configuring sudo permissions for power actions..."

# Allow user to shutdown/reboot without password
if ! grep -q "# Pi iOS Desktop power commands" /etc/sudoers; then
    echo "" >> /etc/sudoers
    echo "# Pi iOS Desktop power commands" >> /etc/sudoers
    echo "$ACTUAL_USER ALL=(ALL) NOPASSWD: /sbin/shutdown" >> /etc/sudoers
    echo "$ACTUAL_USER ALL=(ALL) NOPASSWD: /sbin/reboot" >> /etc/sudoers
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Pi iOS Desktop Environment is now installed."
echo ""
echo "What happens next:"
echo "  1. On next boot, you'll automatically log into Pi iOS Desktop"
echo "  2. Or select 'Pi iOS Desktop' from the login screen"
echo ""
echo -e "${YELLOW}Choose an option:${NC}"
echo ""
echo "  [1] Reboot now to start Pi iOS Desktop"
echo "  [2] Start Pi iOS Desktop now (logout current session)"
echo "  [3] Exit (start manually later)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Rebooting in 3 seconds...${NC}"
        sleep 3
        reboot
        ;;
    2)
        echo ""
        echo -e "${BLUE}Starting Pi iOS Desktop...${NC}"
        systemctl restart lightdm
        ;;
    3)
        echo ""
        echo "To start Pi iOS Desktop:"
        echo "  - Reboot: sudo reboot"
        echo "  - Or logout and select 'Pi iOS Desktop' from login screen"
        echo "  - Or run: sudo systemctl restart lightdm"
        ;;
esac

echo ""
echo -e "${GREEN}Enjoy your Pi iOS Desktop!${NC}"
