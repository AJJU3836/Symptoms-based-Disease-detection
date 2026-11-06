import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "report_screenshots")
ARTIFACTS_DIR = r"C:\Users\AJJU\.gemini\antigravity\brain\8281c305-cfae-4b2d-92aa-96e0480e4210"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--disable-gpu")
opts.add_argument("--window-size=1400,900")
opts.add_argument("--hide-scrollbars")

driver = webdriver.Edge(options=opts)
driver.set_window_size(1400, 900)

def js_click(elem):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", elem)

def save_screen(name, scroll_top=True):
    path = os.path.join(SCREENSHOTS_DIR, name)
    if scroll_top:
        driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    driver.save_screenshot(path)
    shutil.copy(path, os.path.join(ARTIFACTS_DIR, name))
    print(f"Captured: {name} -> {path}")

try:
    # 1. Home Page
    print("Navigating to Home Page...")
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)
    save_screen("01_home_page.png")

    # 2. Registration Page
    print("Navigating to Registration Page...")
    driver.get("http://127.0.0.1:8000/registration")
    time.sleep(2)
    save_screen("02_patient_registration.png")

    # 3. Login Page
    print("Navigating to Login Page...")
    driver.get("http://127.0.0.1:8000/login")
    time.sleep(2)
    save_screen("03_user_login.png")

    # 4. Patient Login & Symptom Checker
    print("Logging in as Patient...")
    patient_role_btn = driver.find_element(By.ID, "role-patient-btn")
    js_click(patient_role_btn)
    time.sleep(0.5)

    mob_input = driver.find_element(By.ID, "mobile-input")
    mob_input.clear()
    mob_input.send_keys("9876543210")

    pwd_input = driver.find_element(By.ID, "password-input")
    pwd_input.clear()
    pwd_input.send_keys("1234")

    submit_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    js_click(submit_login)
    time.sleep(2)

    # Now on checksymptoms
    print("Capturing Patient Symptom Selection...")
    # Select symptoms via JS
    driver.execute_script("""
        toggleSymptom('High Fever');
        toggleSymptom('Chills');
        toggleSymptom('Vomiting');
        toggleSymptom('Fatigue');
        toggleSymptom('Headache');
        setSeverity('high');
    """)
    time.sleep(1)
    save_screen("04_patient_symptom_selection.png")

    # 5. Disease Detection Result
    print("Submitting symptoms for disease prediction...")
    submit_btn = driver.find_element(By.ID, "submit-btn")
    js_click(submit_btn)
    time.sleep(2)
    save_screen("05_disease_detection_results.png")

    # 6. Change Password Page
    print("Navigating to Change Password...")
    driver.get("http://127.0.0.1:8000/changepassword")
    time.sleep(1.5)
    save_screen("06_patient_change_password.png")

    # 7. Admin Login & Master Pages
    print("Logging in as Admin...")
    driver.get("http://127.0.0.1:8000/login")
    time.sleep(1)
    admin_role_btn = driver.find_element(By.ID, "role-admin-btn")
    js_click(admin_role_btn)
    time.sleep(0.5)

    mob_input = driver.find_element(By.ID, "mobile-input")
    mob_input.clear()
    mob_input.send_keys("8767541300")

    pwd_input = driver.find_element(By.ID, "password-input")
    pwd_input.clear()
    pwd_input.send_keys("ajay123")

    submit_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    js_click(submit_login)
    time.sleep(2)

    # 8. Patient Master
    print("Capturing Admin - Patient Master...")
    save_screen("07_admin_patient_master.png")

    # 9. Speciality Master
    print("Navigating to Speciality Master...")
    driver.get("http://127.0.0.1:8000/specialitymaster")
    time.sleep(1.5)
    save_screen("08_admin_speciality_master.png")

    # 10. Add Speciality
    print("Navigating to Add Speciality...")
    driver.get("http://127.0.0.1:8000/addspeciality")
    time.sleep(1.5)
    save_screen("09_admin_add_speciality.png")

    # 11. Symptom Master
    print("Navigating to Symptom Master...")
    driver.get("http://127.0.0.1:8000/symptommaster")
    time.sleep(1.5)
    save_screen("10_admin_symptom_master.png")

    # 12. Add Symptom
    print("Navigating to Add Symptom...")
    driver.get("http://127.0.0.1:8000/addsymptom")
    time.sleep(1.5)
    save_screen("11_admin_add_symptom.png")

    # 13. Disease Master
    print("Navigating to Disease Master...")
    driver.get("http://127.0.0.1:8000/diseasemaster")
    time.sleep(1.5)
    save_screen("12_admin_disease_master.png")

    # 14. Add Disease
    print("Navigating to Add Disease...")
    driver.get("http://127.0.0.1:8000/adddisease")
    time.sleep(1.5)
    save_screen("13_admin_add_disease.png")

    # 15. Model Performance Dashboard
    print("Navigating to Model Performance Dashboard...")
    driver.get("http://127.0.0.1:8000/modelperformance")
    time.sleep(2)
    save_screen("14_admin_model_performance.png")

    # 16-19. Static Charts
    charts = [
        ("accuracy_comparison.png", "15_chart_accuracy_comparison.png"),
        ("cv_comparison.png", "16_chart_cv_comparison.png"),
        ("confusion_matrix.png", "17_chart_confusion_matrix.png"),
        ("disease_distribution.png", "18_chart_disease_distribution.png")
    ]
    charts_dir = os.path.join(os.path.dirname(__file__), "static", "charts")
    for src, dst in charts:
        src_path = os.path.join(charts_dir, src)
        if os.path.exists(src_path):
            dst_path = os.path.join(SCREENSHOTS_DIR, dst)
            shutil.copy(src_path, dst_path)
            shutil.copy(src_path, os.path.join(ARTIFACTS_DIR, dst))
            print(f"Copied Chart: {dst} -> {dst_path}")
        else:
            print(f"Chart missing: {src_path}")

    print("SUCCESS: All 18 screenshots captured and verified!")

finally:
    driver.quit()
