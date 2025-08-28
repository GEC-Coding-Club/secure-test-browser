from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options

# Configure test timing - SIMPLE!
TEST_START_TIME = "19:00"  # When test entry opens (HH:MM format)
TEST_DURATION_MINUTES = 20  # How long entry is allowed (in minutes)
TEST_URL = "https://www.hackerrank.com/<contest>"

def parse_time(time_str):
    """Convert time string (HH:MM) to datetime object for today"""
    hour, minute = map(int, time_str.split(':'))
    today = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    return today

def check_entry_permission():
    """Check if current time allows test entry"""
    current_time = datetime.now()
    start_time = parse_time(TEST_START_TIME)
    end_time = start_time + timedelta(minutes=TEST_DURATION_MINUTES)
    
    print(f"Current time: {current_time.strftime('%H:%M:%S')}")
    print(f"Test entry window: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
    
    if current_time < start_time:
        print("❌ TEST NOT YET AVAILABLE!")
        print(f"⏰ Test opens at {start_time.strftime('%H:%M')}")
        return False
    elif current_time > end_time:
        print("❌ TEST ENTRY CLOSED!")
        print(f"🔒 Entry closed at {end_time.strftime('%H:%M')}")
        return False
    else:
        print("✅ TEST ENTRY ALLOWED")
        return True

# Check entry permission before starting browser
if not check_entry_permission():
    print("\n🛑 Exiting program - Test access denied")
    input("Press Enter to exit...")
    exit(1)

print("\n🚀 Starting browser...")
options = Options()
options.add_argument("--kiosk")  # fullscreen, no URL bar, no controls

driver = webdriver.Chrome(options=options)
driver.get(TEST_URL)

def is_window_focused():
    """Comprehensive focus detection using Selenium's JavaScript APIs"""
    try:
        
        window_active = driver.execute_script("""
            return document.visibilityState === 'visible' && 
                   !document.hidden && 
                   document.hasFocus();
        """)
        
        
        print(f"🔍 WindowActive: {window_active}")
        
        
        # Return true only if ALL conditions are met
        return (window_active )
        
    except Exception as e:
        print(f"⚠️ Error checking focus: {e}")
        # Fallback to basic focus check
        try:
            return driver.execute_script("return document.hasFocus();")
        except:
            return False

try:
    print("🔍 Monitoring comprehensive browser focus...")
    print("📱 Detects: Tab switching, desktop switching, minimizing, hiding")
    print("⏰ HackerRank will handle test duration and automatic submission")
    
    while True:
        focused = is_window_focused()
        if not focused:
            print("❌ Browser lost focus/visibility! Closing browser...")
            driver.quit()
            break
        time.sleep(1)  # Check every four seconds
except KeyboardInterrupt:
    print("⛔ Ctrl+C detected. Closing browser...")
    driver.quit()
