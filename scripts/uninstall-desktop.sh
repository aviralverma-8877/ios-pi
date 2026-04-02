#!/bin/bash
#
# Uninstall Pi iOS Desktop Environment
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Pi iOS Desktop Environment Uninstall${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root: sudo $0${NC}"
    exit 1
fi

echo -e "${YELLOW}This will remove Pi iOS Desktop and restore the default desktop.${NC}"
read -p "Are you sure? [y/N]: " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Removing Pi iOS Desktop Environment..."

# Remove files
rm -f /usr/bin/pi-ios-desktop
rm -f /usr/bin/pi-ios-session
rm -f /usr/share/xsessions/pi-ios-desktop.desktop

# Restore original lightdm config
if [ -f /etc/lightdm/lightdm.conf.backup ]; then
    mv /etc/lightdm/lightdm.conf.backup /etc/lightdm/lightdm.conf
    echo "Restored original LightDM configuration"
else
    # Set back to LXDE
    sed -i 's/user-session=pi-ios/user-session=LXDE-pi/' /etc/lightdm/lightdm.conf
    echo "Switched back to LXDE desktop"
fi

# Remove .dmrc
ACTUAL_USER="${SUDO_USER:-pi}"
rm -f /home/$ACTUAL_USER/.dmrc

# Remove sudo entries (optional)
sed -i '/# Pi iOS Desktop power commands/,+2d' /etc/sudoers

echo ""
echo -e "${GREEN}Pi iOS Desktop Environment has been removed.${NC}"
echo ""
echo "Restart LightDM to return to default desktop:"
echo "  sudo systemctl restart lightdm"
echo ""
echo "Or reboot:"
echo "  sudo reboot"
