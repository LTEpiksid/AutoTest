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
employee_id_path = '//Work/id.txt'
attachment_paths = [
    'C:/Users/Sidas/Desktop/AutoTest/static/yes.gif',
    'C:/Users/Sidas/Desktop/AutoTest/static/build.jpg'
]

# Verify the existence of the files
for attachment_path in attachment_paths:
    if not os.path.exists(attachment_path):
        raise FileNotFoundError(f"Attachment file {attachment_path} does not exist.")

# Print current working directory for debugging purposes
print("Current working directory:", os.getcwd())

# Initialize the WebDriver with Service object
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Check if id.txt exists and read the employee ID
if not os.path.exists(employee_id_path):
    raise FileNotFoundError(f"{employee_id_path} does not exist. Make sure the file is created and the path is correct.")
else:
    with open(employee_id_path, 'r') as file:
        employee_id = file.read().strip()

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

    # Adding delay
    time.sleep(1)

    # Navigate to Employee Personal Details page
    driver.get(f'https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewPersonalDetails/empNumber/{employee_id}')
    print(f"Navigated to Employee Personal Details page for employee ID {employee_id}.")

    # Adding delay
    time.sleep(1)

    # Fill in Middle Name using the old method
    middle_name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="middleName"]')))
    middle_name_field.clear()
    middle_name_field.send_keys('Goblin')
    print("Middle Name updated.")
    time.sleep(1)

    # Function to fill in fields by locating the label and the input box underneath
    def fill_in_field_by_label(label_text, value):
        print(f"Filling in {label_text}")
        label = wait.until(EC.presence_of_element_located((By.XPATH, f'//label[contains(text(),"{label_text}")]/following::input[1]')))
        label.clear()
        label.send_keys(value)
        print(f"{label_text} updated.")
        time.sleep(1)

    # Fill in the other fields
    fill_in_field_by_label("Other Id", "12345")
    fill_in_field_by_label("Driver's License Number", "D1234567")
    fill_in_field_by_label("License Expiry Date", "2025-12-31")
    fill_in_field_by_label("Date of Birth", "1980-01-01")
    fill_in_field_by_label("Test_Field", "?")

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
        driver.find_element(By.XPATH, '//div[@class="orangehrm-edit-employee-content"]').click()
        print("Clicked on a blank spot to close the dropdown.")
        time.sleep(1)

    # Randomly select options
    select_random_option("Nationality")
    select_random_option("Marital Status")
    select_random_option("Blood Type")

    # Fill in gender
    gender_radio_male = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@value="1"]/following-sibling::span')))
    gender_radio_male.click()
    print("Gender updated to Male.")
    time.sleep(1)

    # Save the changes by clicking both save buttons
    save_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//button[@type="submit"]')))
    for save_button in save_buttons:
        save_button.click()
        time.sleep(1)
        print("Save button clicked.")

    print("Personal details saved.")

    # File manipulation part starts here
    for attachment_path in attachment_paths:
        # Click the + Add button for Attachments
        add_attachment_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//h6[text()="Attachments"]/following-sibling::button[contains(@class, "oxd-button--text")][1]')))
        add_attachment_button.click()
        print("Clicked + Add button for Attachments.")
        time.sleep(2)

        # Select the file for attachment
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        file_input.send_keys(attachment_path)
        print(f"Selected file for attachment: {attachment_path}")
        time.sleep(2)

        # Locate all save buttons and click the 3rd one (lowest on the page)
        save_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//button[@type="submit"]')))
        if len(save_buttons) >= 3:
            save_buttons[2].click()
            print("Clicked the third save button.")
        else:
            print("Less than 3 save buttons found.")
        time.sleep(2)

    # Wait for the attachments to be uploaded
    time.sleep(2)

    # Locate all trash icons and select a random one to delete the file
    trash_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//i[contains(@class, "bi-trash")]')))
    random_trash_icon = random.choice(trash_icons)
    random_trash_icon.click()
    print("Clicked a random trash icon.")
    time.sleep(2)

    # Confirm the deletion
    confirm_delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "oxd-button--label-danger")]')))
    confirm_delete_button.click()
    print("Confirmed the deletion.")
    time.sleep(2)

    # Wait for the deletion to complete
    time.sleep(2)

    # Locate all pencil icons and select a random one to edit the file
    pencil_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//i[contains(@class, "bi-pencil-fill")]')))
    random_pencil_icon = random.choice(pencil_icons)
    random_pencil_icon.click()
    print("Clicked a random pencil icon to edit the file.")
    time.sleep(2)

    # Enter the comment "Merry Christmas Katin" in the edit box
    comment_box = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="oxd-textarea oxd-textarea--active oxd-textarea--resize-vertical"]')))
    comment_box.send_keys("Merry Christmas Katin")
    print("Entered the comment 'Merry Christmas Katin'.")
    time.sleep(2)

    # Locate all save buttons and click the 3rd one (lowest on the page)
    save_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//button[@type="submit"]')))
    if len(save_buttons) >= 3:
        save_buttons[2].click()
        print("Clicked the third save button.")
    else:
        print("Less than 3 save buttons found.")
    time.sleep(2)

    # Locate all download icons and select a random one to download the file
    download_icons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//i[contains(@class, "bi-download")]')))
    random_download_icon = random.choice(download_icons)
    random_download_icon.click()
    print("Clicked a random download icon.")
    time.sleep(2)

except Exception as e:
    print(f"An error occurred: {e}")

# Keep browser open
input("Press Enter to close the browser...")

# Close the browser
driver.quit()
