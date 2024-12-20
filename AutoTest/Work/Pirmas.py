from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time
from random import choice

# Set the path to the ChromeDriver executable
chrome_driver_path = 'C:/Users/Sidas/Desktop/Webdriver/chromedriver.exe'

# Initialize the WebDriver with Service object
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Verify the existence of the file
photo_path = 'C:/Users/Sidas/Desktop/AutoTest/yoda.jpg'
if not os.path.exists(photo_path):
    print(f"File not found: {photo_path}")
else:
    print(f"Using photo path: {photo_path}")

# Track used supervisor names
used_supervisor_names = set()

# Function to select a random but unique supervisor name
def select_unique_supervisor_name(employee_names):
    # Remove duplicates by converting to a set and back to a list
    unique_employee_names = list(set(employee_names))
    available_names = [name for name in unique_employee_names if name not in used_supervisor_names]
    if not available_names:
        raise ValueError("No unique supervisor names available.")
    random_supervisor_name = choice(available_names)
    used_supervisor_names.add(random_supervisor_name)
    return random_supervisor_name

# Navigate to login page
driver.get('https://opensource-demo.orangehrmlive.com/')
print("Navigated to login page.")

# Explicit wait
wait = WebDriverWait(driver, 10)  # Increased wait time for stability

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

    # Navigate to Employee List page to get supervisor names
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList')
    print("Navigated to Employee List page.")

    # Wait for the list of employees to load
    employee_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="oxd-table-card"]//div[@role="row"]')))
    employee_names = [employee.find_element(By.XPATH, './div[3]').text for employee in employee_list]
    print(f"Employee names: {employee_names}")

    # Select a random but unique employee name from the list
    random_supervisor_name = select_unique_supervisor_name(employee_names)
    print(f"Selected random supervisor name: {random_supervisor_name}")

    # Navigate to Add Employee page
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee')
    print("Navigated to Add Employee page.")

    # Wait for Add Employee form to render
    first_name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="firstName"]')))
    first_name_field.send_keys('Yoda')
    print("First Name entered.")

    last_name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="lastName"]')))
    last_name_field.send_keys('Master')
    print("Last Name entered.")

    # Upload profile picture
    if os.path.exists(photo_path):
        photo_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        photo_field.send_keys(photo_path)
        print("Photo uploaded.")

    # Enable Create Login Details
    login_details_toggle = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="oxd-switch-wrapper"]//span')))
    login_details_toggle.click()
    print("Create Login Details checkbox enabled.")

    # Adding a short sleep to ensure fields are visible and interactable
    time.sleep(2)

    # Locate the Username field by the text label
    username_label = wait.until(
        EC.presence_of_element_located((By.XPATH, '//label[contains(text(),"Username")]/following::input[1]')))
    username_label.send_keys('yodamaster')
    print("Username entered.")

    # Locate the Password field by the text label
    password_label = wait.until(
        EC.presence_of_element_located((By.XPATH, '//label[contains(text(),"Password")]/following::input[1]')))
    password_label.send_keys('ForceStrong123!')
    print("Password entered.")

    # Locate the Confirm Password field by the text label
    confirm_password_label = wait.until(
        EC.presence_of_element_located((By.XPATH, '//label[contains(text(),"Confirm Password")]/following::input[1]')))
    confirm_password_label.send_keys('ForceStrong123!')
    print("Confirm password entered.")

    # Save Employee
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    save_button.click()
    print("Employee saved.")

    # Wait for the Job tab and fill in job information
    job_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Job"]')))
    job_tab.click()
    print("Job tab clicked.")
    time.sleep(2)

    # Extract employee ID from the URL
    current_url = driver.current_url
    employee_id = current_url.split('/')[-1]
    print(f"Extracted Employee ID: {employee_id}")

    # Write the employee ID to id.txt
    with open('id.txt', 'w') as file:
        file.write(employee_id)
    print("Employee ID written to id.txt")

    # Ensure the elements in the Job tab are interactable
    joined_date_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="yyyy-dd-mm"]')))
    joined_date_field.send_keys('2024-01-01')
    print("Joined Date entered.")
    time.sleep(1)

    # Locate the Job Title dropdown by the text label
    job_title_label = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 '//label[text()="Job Title"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
    job_title_dropdown = job_title_label
    job_title_dropdown.click()
    time.sleep(1)

    # Get all job title options
    job_title_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listbox"]//span')))
    print(f"Found job title options: {[option.text for option in job_title_options]}")

    # Select a random option
    random_job_title_option = choice(job_title_options)
    random_job_title_option.click()
    print(f"Job Title selected")
    time.sleep(1)

    # Wait for a second and click on a blank spot to close the dropdown
    driver.find_element(By.XPATH, '//div[@class="orangehrm-edit-employee-content"]').click()
    print("Clicked on a blank spot to close the dropdown.")
    time.sleep(1)

    # Locate the Job Category dropdown by the text label
    job_category_label = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    '//label[text()="Job Category"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
    job_category_dropdown = job_category_label
    job_category_dropdown.click()
    print("Job Category dropdown clicked.")
    time.sleep(1)

    job_category_option = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Professionals"]')))
    job_category_option.click()
    print("Job Category selected.")
    time.sleep(1)

    # Wait for a second and click on a blank spot to close the dropdown
    driver.find_element(By.XPATH, '//div[@class="orangehrm-edit-employee-content"]').click()
    print("Clicked on a blank spot to close the dropdown.")
    time.sleep(1)

    # Locate the Location dropdown by the text label
    location_label = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                '//label[text()="Location"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
    location_dropdown = location_label
    location_dropdown.click()
    print("Location dropdown clicked.")
    time.sleep(1)

    location_option = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Canadian Regional HQ"]')))
    location_option.click()
    print("Location selected.")
    time.sleep(1)

    # Wait for a second and click on a blank spot to close the dropdown
    driver.find_element(By.XPATH, '//div[@class="orangehrm-edit-employee-content"]').click()
    print("Clicked on a blank spot to close the dropdown.")
    time.sleep(1)

    # Locate the Employment Status dropdown by the text label
    employment_status_label = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                         '//label[text()="Employment Status"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
    employment_status_dropdown = employment_status_label
    employment_status_dropdown.click()
    time.sleep(1)

    employment_status_option = wait.until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Full-Time Permanent"]')))
    employment_status_option.click()
    print("Employment Status selected.")
    time.sleep(1)

    # Save Job details
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    save_button.click()
    print("Job details saved.")
    time.sleep(1)

    # Adding supervisor
    report_to_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Report-to"]')))
    report_to_tab.click()
    print("Report-to tab clicked.")
    time.sleep(1)

    add_supervisor_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()=" Add "]')))
    add_supervisor_button.click()
    print("Add Supervisor button clicked.")
    time.sleep(1)

    supervisor_name_field = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Type for hints..."]')))
    supervisor_name_field.send_keys(random_supervisor_name)
    print(f"Supervisor Name entered: {random_supervisor_name}")
    time.sleep(3)  # Wait a second for the dropdown to load

    select_supervisor_option = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    select_supervisor_option.click()
    print("Supervisor selected.")
    time.sleep(1)

    # Locate the Reporting Method dropdown by the text label
    reporting_method_label = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        '//label[contains(text(),"Reporting Method")]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
    reporting_method_dropdown = reporting_method_label
    reporting_method_dropdown.click()
    print("Reporting Method dropdown clicked.")
    time.sleep(1)

    # Get all reporting method options
    reporting_method_options = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listbox"]//span')))
    print(f"Found reporting method options: {[option.text for option in reporting_method_options]}")

    # Select a random option
    random_reporting_method_option = choice(reporting_method_options)
    random_reporting_method_option.click()
    print(f"Reporting Method selected")
    time.sleep(1)

    # Save Report-to details
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    save_button.click()
    print("Report-to details saved.")
    time.sleep(1)

    # Verify the employee in the employee list
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList')
    print("Navigated to Employee List page.")

    # Select Employment Status
    employment_status_dropdown = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="oxd-select-text-input"]')))
    employment_status_dropdown.click()

    employment_status_option = wait.until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Full-Time Permanent"]')))
    employment_status_option.click()
    print("Employment Status selected.")

    # Find the Supervisor Name label and enter the name in the box below it
    supervisor_name_label = wait.until(
        EC.presence_of_element_located((By.XPATH, '//label[contains(text(),"Supervisor Name")]/following::input[1]')))
    supervisor_name_field = supervisor_name_label
    supervisor_name_field.send_keys(random_supervisor_name)
    print(f"Supervisor Name entered: {random_supervisor_name}")
    time.sleep(3)  # Wait for the dropdown to load

    # Select the first option from the dropdown
    select_supervisor_option = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    select_supervisor_option.click()
    print("Supervisor selected.")
    time.sleep(1)

    # Initiate search
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    search_button.click()
    print("Search initiated.")

    # Verify the employee in the search results
    try:
        # Debugging: List all employees found in the search results
        employee_rows = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="oxd-table-card"]//div[@role="row"]')))

        found_employee = False
        for index, row in enumerate(employee_rows):
            # Adjust the XPaths to correctly locate the first name and last name
            first_name = row.find_element(By.XPATH, './div[3]').text
            last_name = row.find_element(By.XPATH, './div[4]').text
            print(f"Employee {index + 1}: First Name: {first_name}, Last Name: {last_name}")

            if first_name == 'Yoda' and last_name == 'Master':
                found_employee = True
                print(f"Employee found: {first_name} {last_name}")
                break

        if not found_employee:
            raise Exception("Employee not found in the list.")

        print("Employee found in the list.")
    except Exception as e:
        print(f"An error occurred while verifying the employee: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

# Keep browser open
input("Press Enter to close the browser...")

# Close the browser
driver.quit()

