"""Take screenshots of the Streamlit UI — uses sidebar nav clicks."""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_render(driver, seconds=10):
    """Wait for Streamlit to finish rendering."""
    time.sleep(3)
    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.querySelectorAll('[data-testid=\"stAppViewContainer\"]').length > 0")
        )
    except:
        pass
    time.sleep(seconds)

def capture_page(driver, filepath, name):
    """Capture a full-page screenshot."""
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)
    total_height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
    )
    driver.set_window_size(1920, min(total_height + 200, 5000))
    time.sleep(2)
    driver.save_screenshot(filepath)
    fsize = __import__('os').path.getsize(filepath)
    print(f"  ✓ Saved: {filepath} ({fsize:,} bytes)")
    driver.set_window_size(1920, 1200)

def take_screenshots():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    # 1. Main page (app.py)
    print("1. Capturing Main Dashboard...")
    driver.get("http://localhost:8501/")
    wait_for_render(driver, 10)
    capture_page(driver, "screenshots/01_main_dashboard.png", "Main Dashboard")
    
    # 2. Click "Dashboard" in sidebar
    print("2. Capturing Dashboard page...")
    try:
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='stSidebarNavLink']")
        for link in links:
            text = link.text.strip()
            print(f"   Found nav link: '{text}'")
            if "Dashboard" in text:
                link.click()
                wait_for_render(driver, 10)
                capture_page(driver, "screenshots/02_dashboard.png", "Dashboard")
                break
    except Exception as e:
        print(f"  ✗ Dashboard failed: {e}")
    
    # 3. Click "SAR Editor" in sidebar
    print("3. Capturing SAR Editor page...")
    try:
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='stSidebarNavLink']")
        for link in links:
            text = link.text.strip()
            if "SAR" in text or "Editor" in text:
                link.click()
                wait_for_render(driver, 10)
                capture_page(driver, "screenshots/03_sar_editor.png", "SAR Editor")
                break
    except Exception as e:
        print(f"  ✗ SAR Editor failed: {e}")
    
    # 4. Click "Audit Trail" in sidebar
    print("4. Capturing Audit Trail page...")
    try:
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='stSidebarNavLink']")
        for link in links:
            text = link.text.strip()
            if "Audit" in text:
                link.click()
                wait_for_render(driver, 10)
                capture_page(driver, "screenshots/04_audit_trail.png", "Audit Trail")
                break
    except Exception as e:
        print(f"  ✗ Audit Trail failed: {e}")
    
    driver.quit()
    print("\nDone!")

if __name__ == "__main__":
    take_screenshots()
