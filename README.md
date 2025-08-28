# Secure Test Browser 🔒

A secure browser application that enforces time-based test access control and monitors window focus to prevent cheating during online tests.

## Features ✨

- **Time-based Access Control**: Only allows test entry within specified time windows
- **Efficient Focus Monitoring**: Single comprehensive check that detects tab switching, desktop switching, and minimizing
- **Kiosk Mode**: Opens browser in fullscreen with no address bar or controls
- **Lightweight Detection**: Uses one optimized JavaScript API call for maximum efficiency

## Configuration ⚙️

### 1. Test Timing Settings

Edit the configuration variables in `pro.py`:

```python
# Configure test timing - SIMPLE!
TEST_START_TIME = "19:00"          # When test entry opens (HH:MM format)
TEST_DURATION_MINUTES = 20         # How long entry is allowed (in minutes)  
TEST_URL = "https://www.hackerrank.com/<contest>"  # Your test URL
```

### 2. Configuration Examples

**Example 1: Morning Test**
```python
TEST_START_TIME = "09:00"          # 9:00 AM
TEST_DURATION_MINUTES = 15         # 15 minutes entry window
TEST_URL = "https://www.hackerrank.com/morning-test"
```
*Students can enter from 9:00 AM to 9:15 AM only*

**Example 2: Afternoon Test**
```python
TEST_START_TIME = "14:30"          # 2:30 PM
TEST_DURATION_MINUTES = 30         # 30 minutes entry window
TEST_URL = "https://www.hackerrank.com/afternoon-exam"
```
*Students can enter from 2:30 PM to 3:00 PM only*

**Example 3: Evening Test**
```python
TEST_START_TIME = "18:00"          # 6:00 PM  
TEST_DURATION_MINUTES = 5          # 5 minutes entry window (strict)
TEST_URL = "https://www.hackerrank.com/evening-quiz"
```
*Students can enter from 6:00 PM to 6:05 PM only*

## Installation & Setup 🚀

### Prerequisites
- Python 3.7+ installed
- Google Chrome browser installed
- ChromeDriver (automatically handled by Selenium)

### 1. Install Dependencies
```powershell
pip install selenium pyinstaller
```

### 2. Test the Python Script
```powershell
python pro.py
```

## Compilation to Executable 📦

### Simple Compilation
```powershell
pyinstaller --onefile --console pro.py
```
- Creates: `dist\pro.exe`
- Size: ~18-25 MB
- Shows console output


## Distribution 📤

After compilation, you'll find the executable in the `dist/` folder:
```
pro/
├── dist/
│   └── pro.exe          # ← This is your standalone executable
├── build/               # (temporary build files)
├── pro.py              # (source code)
└── pro.spec            # (PyInstaller configuration)
```

### Distribute the Executable
1. Copy `dist\pro.exe` to target computers
2. No Python installation required on target machines
3. Chrome browser must be installed on target machines

## Usage Instructions 👥

### For Administrators:
1. Configure `TEST_START_TIME`, `TEST_DURATION_MINUTES`, and `TEST_URL`
2. Compile to executable: `pyinstaller --onefile --console pro.py`
3. Distribute `dist\pro.exe` to students

### For Students:
1. Run `pro.exe` at test time
2. Browser will open automatically if within allowed time window
3. **DO NOT** switch tabs, minimize, or switch desktops - browser will close!
4. Focus only on the test - HackerRank handles test duration

## Access Control Logic 🕐

```
Current Time vs Test Window:

Before Start Time:     ❌ "TEST NOT YET AVAILABLE"
During Entry Window:   ✅ "TEST ENTRY ALLOWED" 
After Entry Window:    ❌ "TEST ENTRY CLOSED"

Example with TEST_START_TIME="14:00", TEST_DURATION_MINUTES=20:
- 13:59:59 → ❌ Not available yet
- 14:00:00 → ✅ Entry allowed  
- 14:19:59 → ✅ Entry allowed
- 14:20:00 → ❌ Entry closed
```

## Focus Detection 👁️

The application uses a single, efficient focus detection method that combines multiple JavaScript APIs into one check:

```javascript
return document.visibilityState === 'visible' && 
       !document.hidden && 
       document.hasFocus();
```

**This single indicator detects:**
- ✅ Tab switching (`document.hasFocus()`)
- ✅ Desktop switching (`document.visibilityState`) 
- ✅ Window minimizing (`document.hidden`)
- ✅ Window hiding or becoming invisible

**Triggers browser closure when ANY of these occur:**
- Switching to another browser tab
- Switching to another application  
- Minimizing the browser window
- Switching virtual desktops (Windows 10/11)
- Hiding the browser window

**Console Output:**
```
🔍 WindowActive: True    # ← All focus conditions met
🔍 WindowActive: False   # ← Focus lost, browser will close
```

## Troubleshooting 🔧

### Common Issues:

**"ChromeDriver not found"**
```powershell
pip install --upgrade selenium
```

**"Permission denied" when running .exe**
- Run as Administrator
- Check Windows Defender/Antivirus settings

**Browser doesn't open**
- Ensure Chrome is installed
- Check if TEST_URL is accessible
- Verify time configuration

**Focus detection not working**
- Try running as Administrator
- Check if browser extensions are interfering
- Test with `python pro.py` first

### Debug Mode:
The console output shows the single focus status indicator:
```
🔍 WindowActive: True
Current time: 14:05:23
Test entry window: 14:00 - 14:20
✅ TEST ENTRY ALLOWED
```

When focus is lost:
```
🔍 WindowActive: False
❌ Browser lost focus/visibility! Closing browser...
```

## Security Features 🛡️

- **Kiosk Mode**: Prevents access to browser controls
- **Focus Monitoring**: Detects attempts to leave the test
- **Time Enforcement**: Strict entry window control
- **Automatic Closure**: Immediate termination on focus loss

## License 📄

This project is for educational and testing purposes. Ensure compliance with your institution's policies and applicable laws.

---

**Need help?** Check the console output for detailed status messages and error information.
