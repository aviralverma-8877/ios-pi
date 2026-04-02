# Pi iOS Desktop Environment - Architecture

## Overview

A GNOME-like desktop environment for Raspberry Pi with iOS-inspired aesthetics. This is a **complete desktop shell**, not just an application launcher.

---

## Architecture

### Desktop Shell Components

```
┌─────────────────────────────────────────────────┐
│  Top Panel (Activities, Title, System, Power)  │ ← Always visible
├─────────────────────────────────────────────────┤
│                                                 │
│                                                 │
│            Desktop Background Area              │ ← Stays behind windows
│              (Gradient background)              │
│                                                 │
│                                                 │
├─────────────────────────────────────────────────┤
│          Dock (Favorite Apps)                   │ ← Always visible
└─────────────────────────────────────────────────┘

       Application Windows
       ┌──────────────┐
       │ File Manager │  ← Separate movable windows
       └──────────────┘
            ┌──────────┐
            │ Terminal │
            └──────────┘
```

---

## Components

### 1. Top Panel (`TopPanel`)

**Purpose:** Main control bar like GNOME's top bar

**Features:**
- **Activities Button** (🏠) - Opens application launcher
- **App Title** - Shows current desktop name
- **System Indicators** - CPU temperature
- **Clock** - Current time (HH:MM format)
- **Power Button** (⏻) - Shutdown/reboot/logout menu

**Styling:**
- Semi-transparent black background
- White text and icons
- Hover effects on buttons
- 35px height

**Code:** Lines 19-76

---

### 2. Desktop Area (`DesktopArea`)

**Purpose:** Background desktop where windows appear

**Features:**
- Beautiful gradient background (purple to blue)
- Stays behind all windows
- Full screen coverage

**Styling:**
- iOS-inspired gradient: `#667eea` → `#764ba2`
- No borders or decorations

**Code:** Lines 78-88

---

### 3. Dock (`Dock`)

**Purpose:** Quick-launch bar for favorite apps (like macOS Dock or Ubuntu Launcher)

**Apps in Dock:**
- 📁 Files
- 💻 Terminal
- 🌐 Browser
- ⚙️ Settings
- ⚡ Apps (opens launcher)

**Features:**
- Centered at bottom
- Transparent rounded background
- Large touch-friendly icons (55x55px)
- Hover effects
- Tooltips on hover

**Styling:**
- Semi-transparent white background
- Rounded corners (15px radius)
- Icon-only buttons with emoji
- 70px height

**Code:** Lines 90-132

---

### 4. Application Launcher (`ApplicationLauncher`)

**Purpose:** Full-screen overlay to launch apps (like GNOME Activities)

**Activation:**
- Click "Activities" button in top panel
- Click "Apps" icon in dock
- Keyboard shortcut (planned)

**Features:**
- **Search Bar** - Type to filter applications
- **App Grid** - 4 columns of app icons
- **19 Built-in Apps:**
  - Files, Terminal, Browser, Text Editor
  - Calculator, Settings, System Info
  - Images, Music, Videos
  - Calendar, Mail, Clock, Weather
  - Notes, Camera, Maps, Store
  - Power

**Interaction:**
- Click app to launch
- ESC key to close
- Search updates grid in real-time

**Styling:**
- Dark semi-transparent overlay (220 alpha)
- White search box with purple border
- App buttons with rounded corners
- Large, touch-friendly (100x100px)

**Code:** Lines 134-233

---

### 5. Application Windows

All apps open as **standalone windows** that can be:
- Moved around the screen
- Resized
- Minimized/Maximized (via window manager)
- Stacked (proper z-order)

#### File Manager Window (`FileManagerWindow`)

**Features:**
- Browse file system
- Navigate with back/home buttons
- Double-click to open folders/files
- Shows folders (📁) and files (📄)
- Opens files with default apps (xdg-open)

**Size:** 600x400px  
**Code:** Lines 235-287

#### Terminal Window (`TerminalWindow`)

**Features:**
- Command execution
- Colored output (Nord theme)
- Command history in output area
- Error handling
- Shows current user and home directory

**Styling:**
- Dark Nord theme (#2e3440 background)
- Blue text (#88c0d0)
- Monospace font (Courier New)

**Size:** 700x450px  
**Code:** Lines 289-351

#### Settings Window (`SettingsWindow`)

**Features:**
- 12 settings categories:
  - Wi-Fi & Network
  - Sound & Volume
  - Display & Brightness
  - Wallpaper & Appearance
  - Power & Battery
  - General Settings
  - Users & Accounts
  - Privacy & Security
  - Date & Time
  - Language & Region
  - Accessibility
  - About This System

**Size:** 500x450px  
**Code:** Lines 353-405

---

### 6. Desktop Environment Shell (`DesktopEnvironment`)

**Purpose:** Main coordinator that brings everything together

**Responsibilities:**
- Creates and positions all components
- Manages window lifecycle
- Handles application launching
- Coordinates panel, desktop, and dock
- Stays behind other windows

**Window Management:**
- Tracks open windows in dictionary
- Prevents duplicate windows
- Raises existing windows when re-launched
- Properly disposes of closed windows

**Code:** Lines 407-518

---

## User Interaction Flow

### Launching an App

```
User clicks app in Dock
    ↓
DesktopEnvironment.launch_application()
    ↓
Check if window already open
    ↓
If yes: Raise and focus existing window
If no:  Create new window instance
    ↓
Show window
Add to open_windows dict
    ↓
Window appears on desktop
```

### Using Activities Overlay

```
User clicks "Activities" button
    ↓
ApplicationLauncher dialog opens (modal)
    ↓
User types in search box
    ↓
App grid filters in real-time
    ↓
User clicks app icon
    ↓
app_selected signal emitted
    ↓
Dialog closes
Application launches
```

### Power Menu

```
User clicks power button (⏻)
    ↓
Dropdown menu appears at cursor
    ↓
User selects option:
  - Logout: Quit application
  - Reboot: sudo reboot
  - Shutdown: sudo shutdown -h now
    ↓
Confirmation dialog
    ↓
Execute if confirmed
```

---

## Technical Details

### Qt Window Flags

- **Desktop Area:** `Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint`
  - No title bar
  - Always behind other windows

- **Application Windows:** `Qt.Window`
  - Normal window with title bar
  - Can be moved, resized
  - Managed by window manager (OpenBox)

- **Application Launcher:** `Qt.FramelessWindowHint | Qt.Dialog`
  - No title bar
  - Modal (blocks input to other windows)
  - Full screen overlay

### Styling

All components use Qt Style Sheets (QSS) for styling:

- **Colors:**
  - Primary gradient: `#667eea` → `#764ba2`
  - Panel background: `rgba(0, 0, 0, 200)`
  - Dock background: `rgba(255, 255, 255, 180)`
  - Terminal: Nord color scheme

- **Effects:**
  - Rounded corners on panels and buttons
  - Hover effects with transparency changes
  - Smooth color transitions

### Signal/Slot Connections

```python
# Activities button → Show launcher
top_panel.show_activities.connect(show_activities)

# Dock app click → Launch app
dock.app_launched.connect(launch_application)

# Launcher app select → Launch app
launcher.app_selected.connect(launch_application)

# Power button → Show menu
top_panel.power_btn.clicked.connect(show_power_menu)
```

---

## Comparison: App vs Desktop Environment

### Before (Fullscreen App)

```
┌─────────────────────┐
│     Status Bar      │
├─────────────────────┤
│                     │
│    Single Screen    │
│    with App Grid    │
│   (takes entire     │
│     display)        │
│                     │
├─────────────────────┤
│       Dock          │
│    Home Button      │
└─────────────────────┘
```

**Limitations:**
- Only one screen visible at a time
- Apps replace the entire interface
- No multitasking
- Feels like mobile app

### After (Desktop Environment)

```
┌─────────────────────┐
│     Top Panel       │  ← Always visible
├─────────────────────┤
│  ┌──────┐           │
│  │ Win1 │ ┌──────┐  │  ← Multiple windows
│  └──────┘ │ Win2 │  │
│           └──────┘  │
│    Desktop Area     │
├─────────────────────┤
│       Dock          │  ← Always visible
└─────────────────────┘
```

**Benefits:**
- Multiple windows simultaneously
- Real desktop feel
- Proper window management
- Better for productivity
- Familiar to desktop users

---

## Integration with OpenBox

The pi-ios-session script starts OpenBox window manager before the desktop environment:

```bash
# Start window manager (lightweight fallback)
openbox &
WM_PID=$!

# Wait for WM to start
sleep 1

# Start the desktop environment
/usr/bin/pi-ios-desktop
```

**Why OpenBox?**
- Lightweight (minimal resource usage)
- Provides window decorations
- Handles window moving/resizing
- Manages window stacking
- Runs in background, invisible to user

---

## Performance Considerations

### Memory Usage

- **Desktop Shell:** ~30-40 MB
- **Each Window:** ~10-20 MB
- **Total:** ~50-100 MB (with 3 windows open)

### CPU Usage

- **Idle:** < 1%
- **Active:** 2-5%
- **Panel Updates:** Timer runs every 1 second (minimal impact)

### Optimization

- Qt logging disabled: `QT_LOGGING_RULES='*.debug=false'`
- No unnecessary redraws
- Lazy window creation (only when launched)
- Windows destroyed when closed

---

## Future Enhancements

### Planned Features

1. **Desktop Icons**
   - Files and folders on desktop
   - Drag and drop support

2. **Window Animations**
   - Fade in/out
   - Smooth minimize/maximize

3. **Task Switcher**
   - Alt+Tab functionality
   - Window thumbnails

4. **System Tray**
   - Notification icons
   - Background app indicators

5. **Workspace Switcher**
   - Multiple virtual desktops
   - Swipe gestures

6. **Keyboard Shortcuts**
   - Super key → Activities
   - Alt+F2 → Run dialog
   - Ctrl+Alt+T → Terminal

---

## Testing on Raspberry Pi

### Expected Behavior

1. **Boot:**
   - LightDM shows login
   - Select "Pi iOS Desktop"
   - Desktop environment starts
   - Top panel and dock appear
   - Desktop background visible

2. **Launching Apps:**
   - Click dock icon → Window opens
   - Click Activities → Launcher overlay
   - Search works → Grid filters
   - Multiple windows can be open

3. **Window Management:**
   - Windows can be moved
   - Windows can be resized
   - Windows can be closed (X button)
   - Reopening raises existing window

4. **System:**
   - Temperature shows in panel
   - Time updates every second
   - Power menu works
   - Shutdown/reboot require sudo permission

### Troubleshooting

**If panel doesn't appear:**
- Check X server is running
- Verify DISPLAY variable set
- Check for Qt errors in logs

**If windows don't open:**
- Ensure OpenBox is running
- Check application permissions
- Verify Python/Qt installation

**If performance is poor:**
- Increase `gpu_mem` in /boot/config.txt
- Close unnecessary applications
- Check system temperature

---

## Conclusion

This is a **complete desktop environment** that provides:
- Professional desktop experience
- Proper window management
- Multitasking capabilities
- Familiar GNOME-like workflow
- iOS-inspired aesthetics

It's designed to replace LXDE as the primary desktop for Raspberry Pi users who want a modern, touch-friendly interface.
