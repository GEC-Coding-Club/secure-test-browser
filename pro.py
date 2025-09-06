from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
import tempfile
import os
import hashlib

# Configure test timing - SIMPLE!
TEST_START_TIME = "11:21"  # When test entry opens (HH:MM format)
TEST_DURATION_MINUTES = 30  # How long entry is allowed (in minutes)
TEST_URL = "https://www.hackerrank.com/<contest>"
MAX_ATTEMPTS = 2                   # Maximum number of test attempts allowed

def get_attempt_file_path():
    """Generate unique temp file path based on test URL"""
    # Create hash of test URL to make unique filename
    url_hash = hashlib.md5(TEST_URL.encode()).hexdigest()[:8]
    filename = f"coding_club_test_attempts_{url_hash}.tmp"
    return os.path.join(tempfile.gettempdir(), filename)

def get_attempt_count():
    """Get current number of test attempts"""
    attempt_file = get_attempt_file_path()
    try:
        if os.path.exists(attempt_file):
            with open(attempt_file, 'r') as f:
                count = int(f.read().strip())
                return count
        return 0
    except:
        return 0

def increment_attempt_count():
    """Increment and save attempt count"""
    attempt_file = get_attempt_file_path()
    current_count = get_attempt_count()
    new_count = current_count + 1
    
    try:
        with open(attempt_file, 'w') as f:
            f.write(str(new_count))
        return new_count
    except Exception as e:
        print(f"⚠️ Warning: Could not save attempt count: {e}")
        return new_count

def check_attempt_limit():
    """Check if user has exceeded maximum attempts"""
    current_attempts = get_attempt_count()
    attempt_file = get_attempt_file_path()
    
    print(f"📊 Test Attempt Status:")
    print(f"📁 Tracking file: {os.path.basename(attempt_file)}")
    print(f"🔢 Previous attempts: {current_attempts}/{MAX_ATTEMPTS}")
    
    if current_attempts >= MAX_ATTEMPTS:
        print(f"❌ MAXIMUM ATTEMPTS EXCEEDED!")
        print(f"🚫 You have already used all {MAX_ATTEMPTS} allowed attempts for this test")
        print(f"📝 Contact administrator if you believe this is an error")
        
        # Countdown timer
        for i in range(60, 0, -1):
            print(f"\r⏰ Closing in {i} seconds... ", end="", flush=True)
            time.sleep(1)
        print("\n")
        return False
    
    # Increment attempt count for this session
    new_count = increment_attempt_count()
    print(f"✅ Starting attempt {new_count}/{MAX_ATTEMPTS}")
    
    if new_count == MAX_ATTEMPTS:
        print(f"⚠️ WARNING: This is your FINAL attempt!")
    
    return True

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
        
        # Countdown timer
        for i in range(10, 0, -1):
            print(f"\r⏰ Closing in {i} seconds... ", end="", flush=True)
            time.sleep(1)
        print("\n")
        return False
    elif current_time > end_time:
        print("❌ TEST ENTRY CLOSED!")
        print(f"🔒 Entry closed at {end_time.strftime('%H:%M')}")
        
        # Countdown timer
        for i in range(10, 0, -1):
            print(f"\r⏰ Closing in {i} seconds... ", end="", flush=True)
            time.sleep(1)
        print("\n")
        return False
    else:
        print("✅ TEST ENTRY ALLOWED")
        return True

# Check entry permission before starting browser
if not check_entry_permission():
    print("\n🛑 Exiting program - Test access denied")
    # No additional sleep needed here since check_entry_permission() already has delay
    exit(1)

# Check attempt limit before starting browser
if not check_attempt_limit():
    print("\n🛑 Exiting program - Maximum attempts exceeded")
    # No additional sleep needed here since check_attempt_limit() already has delay
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
