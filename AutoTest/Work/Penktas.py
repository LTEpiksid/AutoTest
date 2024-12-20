import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

# Set the path to the ChromeDriver executable
chrome_driver_path = 'C:/Users/Sidas/Desktop/Webdriver/chromedriver.exe'

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

    # Navigate to the predefined report creation page
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/pim/definePredefinedReport')
    print("Navigated to predefined report creation page.")

    # Wait for the page to load
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    print("Page fully loaded.")


    # Fill in the report name
    def fill_in_field_by_label(label_text, value):
        print(f"Filling in {label_text}")
        field = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//label[contains(text(),"{label_text}")]/following::input[1]')))
        field.clear()
        field.send_keys(value)
        print(f"{label_text} updated.")
        time.sleep(1)


    fill_in_field_by_label("Report Name", "My Test Report")


    # Function to select a random option from a dropdown
    def select_random_option(label_text):
        print(f"Selecting random option for {label_text}")
        dropdown_label = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    f'//label[text()="{label_text}"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
        dropdown_label.click()
        time.sleep(1)
        options = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listbox"]//span')))
        random_option = random.choice(options)
        random_option.click()
        print(f"{label_text} selected")
        time.sleep(1)


    # Add two criteria with slower execution
    select_random_option("Selection Criteria")
    add_criteria_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[@class="oxd-icon-button orangehrm-report-icon"]')))
    add_criteria_button.click()
    time.sleep(2)  # Slowing down
    select_random_option("Selection Criteria")
    add_criteria_button.click()
    print("Added two criteria.")
    time.sleep(2)  # Slowing down

    # Delete the criteria by pressing the trash icon with slower execution
    delete_criteria_buttons = driver.find_elements(By.XPATH,
                                                   '//button[contains(@class, "oxd-icon-button") and i[contains(@class, "bi-trash-fill")]]')
    for button in delete_criteria_buttons:
        button.click()
        time.sleep(1)  # Slowing down
    print("Deleted the criteria.")

    # Select "Current and Past Employees" in the Include field
    print('Selecting "Current and Past Employees" in the Include field')
    include_field = wait.until(EC.presence_of_element_located((By.XPATH,
                                                               '//label[text()="Include"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
    include_field.click()
    include_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Current and Past Employees"]')))
    include_option.click()
    print('"Current and Past Employees" selected')


    # Function to select a random display field group and fields
    def select_display_field_group_and_fields():
        print("Selecting random display field group")
        select_random_option("Select Display Field Group")

        # Select a random display field and press the + button, four times, keeping the same field group
        def select_display_field():
            # Select a random display field
            print("Selecting random display field")
            dropdown_label = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        '//label[text()="Select Display Field"]/ancestor::div[1]/following-sibling::div[1]//div[@class="oxd-select-text-input"]')))
            dropdown_label.click()
            options = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listbox"]//span')))
            random_option = random.choice(options)
            random_option.click()
            print("Select Display Field selected")

            # Press the + button
            add_field_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '(//button[@class="oxd-icon-button orangehrm-report-icon"])[2]')))
            add_field_button.click()
            print("Display field added")

        # Add four different display fields from the selected field group
        for _ in range(4):
            select_display_field()
        print("Added four different display fields from the selected field group.")


    # Repeat for four display field groups
    for _ in range(4):
        select_display_field_group_and_fields()


    # Mark all "Include Header" checkboxes
    def mark_include_header_checkboxes():
        print("Marking all Include Header checkboxes")
        checkboxes = driver.find_elements(By.XPATH,
                                          '//p[text()="Include Header"]/ancestor::div[contains(@class, "orangehrm-report-field")]//input[@type="checkbox"]')
        for checkbox in checkboxes:
            span = checkbox.find_element(By.XPATH, './following-sibling::span')
            driver.execute_script("arguments[0].click();", span)  # Clicking the span instead of checkbox
            time.sleep(1)
        print("All Include Header checkboxes marked")


    mark_include_header_checkboxes()


    # Delete three random display fields that have been posted
    def delete_random_display_fields():
        print("Deleting three random display fields")
        for _ in range(3):
            try:
                posted_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                                                '//span[contains(@class, "oxd-chip oxd-chip--default oxd-multiselect-chips-selected")]')))
                if len(posted_fields) > 0:
                    random_field = random.choice(posted_fields)
                    delete_button = random_field.find_element(By.XPATH, './/i[contains(@class, "bi-x --clear")]')
                    delete_button.click()
                    time.sleep(1)
                    print("Deleted a random display field")
                else:
                    print("No more display fields to delete.")
                    break
            except Exception as e:
                print(f"Error deleting display field: {e}")
                break


    delete_random_display_fields()


    # Delete a random display field group that has been posted
    def delete_random_display_field_group():
        print("Deleting one random display field group")
        try:
            field_groups = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                                           '//div[contains(@class, "oxd-grid-item oxd-grid-item--gutters orangehrm-report-field --offset-column-1")]')))
            if field_groups:
                random_group = random.choice(field_groups)
                delete_button = random_group.find_element(By.XPATH,
                                                          './/button[@class="oxd-icon-button" and i[contains(@class, "bi-trash-fill")]]')
                delete_button.click()
                print("Random display field group deleted")
            else:
                print("No display field groups found to delete")
        except Exception as e:
            print(f"Error deleting display field group: {e}")


    delete_random_display_field_group()


    # Click the save button
    def click_save_button():
        print("Clicking the Save button")
        save_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@type="submit" and contains(@class, "oxd-button--secondary")]')))
        save_button.click()
        print("Save button clicked")


    click_save_button()

    delete_random_display_field_group()

except Exception as e:
    print(f"An error occurred: {e}")

# Keep browser open
input("Press Enter to close the browser...")

# Close the browser
driver.quit()
