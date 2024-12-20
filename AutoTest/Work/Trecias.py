from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time
import random

# Set the path to the ChromeDriver executable
chrome_driver_path = 'C:/Users/Sidas/Desktop/Webdriver/chromedriver.exe'
file_path = 'C:/Users/Sidas/Desktop/AutoTest/static/resume.txt'

# Verify the existence of the file
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Attachment file {file_path} does not exist.")

# Print current working directory for debugging purposes
print("Current working directory:", os.getcwd())

# Initialize the WebDriver with Service object
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Navigate to login page
driver.get('https://opensource-demo.orangehrmlive.com/')
print("Navigated to login page.")

# Explicit wait
wait = WebDriverWait(driver, 10)

try:
    # Wait for page to load
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    print("Page fully loaded.")

    # Login
    username_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
    username_field.send_keys('Admin')

    password_field = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_field.send_keys('admin123')

    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    print("Login submitted.")

    # Wait for home page to load
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(1)

    # Navigate to Add Candidate page
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/recruitment/addCandidate')
    print("Navigated to Add Candidate page.")

    # Adding delay
    time.sleep(1)

    # Fill in candidate details by name
    def fill_in_field_by_name(field_name, value):
        print(f"Filling in {field_name}")
        field = wait.until(EC.presence_of_element_located((By.NAME, field_name)))
        field.send_keys(value)
        print(f"{field_name} updated.")
        time.sleep(1)

    fill_in_field_by_name("firstName", "Lloyd")
    fill_in_field_by_name("middleName", "Ninja")
    fill_in_field_by_name("lastName", "Garmadon")


    # Fill in candidate details by label
    def fill_in_field_by_label(label_text, value):
        print(f"Filling in {label_text}")
        field = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//label[contains(text(),"{label_text}")]/following::input[1]')))
        field.clear()
        field.send_keys(value)
        print(f"{label_text} updated.")
        time.sleep(1)

    fill_in_field_by_label("Email", "LloydGarmadom@gmail.com")
    fill_in_field_by_label("Contact Number", "123456789")
    fill_in_field_by_label("Keywords", "AutoTest, Selenium, Automation")

    # Add notes
    def fill_in_textarea_by_label(label_text, value):
        print(f"Filling in {label_text}")
        field = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//label[contains(text(),"{label_text}")]/following::textarea[1]')))
        field.clear()
        field.send_keys(value)
        print(f"{label_text} updated.")
        time.sleep(1)

    fill_in_textarea_by_label("Notes", "This is a test candidate.")

    # Function to select a random option from a dropdown
    def select_random_option(label_text):
        print(f"Selecting random option for {label_text}")
        dropdown_label = wait.until(EC.presence_of_element_located((By.XPATH, f'//label[text()="{label_text}"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
        dropdown_label.click()
        time.sleep(1)
        options = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listbox"]//span')))
        print(f"Found options for {label_text}: {[option.text for option in options]}")
        random_option = random.choice(options)
        random_option.click()
        print(f"{label_text} selected")
        time.sleep(1)

    # Select a vacancy
    select_random_option("Vacancy")

    # Attach a file
    resume_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
    resume_input.send_keys(file_path)
    print(f"Selected file for attachment: {file_path}")
    time.sleep(2)

    # Consent to keep data
    consent_checkbox = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="oxd-checkbox-wrapper"]//input[@type="checkbox"]')))
    driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", consent_checkbox)
    print("Consent checkbox clicked.")
    time.sleep(1)

    # Save the candidate
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    save_button.click()
    print("Candidate saved.")
    time.sleep(2)

    # Shortlist the candidate using JavaScript
    green_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "oxd-button--success")]')))
    driver.execute_script("arguments[0].click();", green_button)
    print("Shortlisted the candidate.")
    time.sleep(1)

    # Add notes for the candidate on the shortlist page
    def fill_in_textarea_by_label(label_text, value):
        print(f"Filling in {label_text}")
        field = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//label[contains(text(),"{label_text}")]/following::textarea[1]')))
        field.clear()
        field.send_keys(value)
        print(f"{label_text} updated.")
        time.sleep(1)

    fill_in_textarea_by_label("Notes", "Notes for the candidate after shortlisting.")
    print("You have been shortlisted :D.")
    time.sleep(1)

    # Save notes
    save_notes_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    save_notes_button.click()
    print("Shortlist notes saved.")
    time.sleep(2)

    # Click the "Schedule Interview" button
    schedule_interview_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "oxd-button--success") and text()=" Schedule Interview "]')))
    schedule_interview_button.click()
    print("Schedule Interview button clicked.")
    time.sleep(2)

    # Fill in interview details
    fill_in_field_by_label("Interview Title", "Technical Interview")

    # Select interviewer
    def select_interviewer(name):
        print(f"Selecting interviewer {name}")
        interviewer_input = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="Interviewer"]/following::input[1]')))
        interviewer_input.send_keys(name)
        time.sleep(2)  # Wait for suggestions to appear
        first_option = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="listbox"]//span')))
        first_option.click()
        print(f"Interviewer {name} selected")
        time.sleep(1)

    select_interviewer("Yoda")

    # Fill in date, time, and notes
    fill_in_field_by_label("Date", "2024-12-20")  # Use an appropriate date format
    fill_in_field_by_label("Time", "10:00")  # Use an appropriate time format
    fill_in_textarea_by_label("Notes", "This is a technical interview.")

    # Save the interview schedule
    save_interview_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(text(), "Save")]')))
    save_interview_button.click()
    print("Interview schedule saved.")

except Exception as e:
    print(f"An error occurred: {e}")

# Keep browser open
input("Press Enter to close the browser...")

# Close the browser
driver.quit()
