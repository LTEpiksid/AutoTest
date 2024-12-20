from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time
from datetime import datetime, timedelta

# Set the path to the ChromeDriver executable
chrome_driver_path = 'C:/Users/Sidas/Desktop/Webdriver/chromedriver.exe'
image_path = 'C:/Users/Sidas/Desktop/AutoTest/static/Zane.jpg'  # Updated path

# Verify the existence of the image file
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Attachment file {image_path} does not exist.")

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

    # Navigate to Buzz page
    driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/buzz/viewBuzz')
    print("Navigated to Buzz page.")

    # Wait for Buzz page to load
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    print("Buzz page fully loaded.")
    time.sleep(2)

    # Click on the Share Photos button
    share_photos_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="oxd-glass-button-icon oxd-glass-button-icon--cameraglass"]/ancestor::button')))
    share_photos_button.click()
    time.sleep(2)

    # Wait for modal to appear and attach the image
    image_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
    image_input.send_keys(image_path)
    print(f"Selected image for attachment: {image_path}")
    time.sleep(2)

    # Write something in the second post text area
    post_textareas = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//textarea[@class="oxd-buzz-post-input"]')))
    if len(post_textareas) > 1:
        post_textareas[1].send_keys("ZANE!")
    else:
        print("Unable to find the second text area.")
    time.sleep(2)

    # Capture the current time and add 1 minute
    post_time = (datetime.now() + timedelta(minutes=1)).strftime('%Y-%d-%m %I:%M %p')
    print(f"Captured post time: {post_time}")

    # Post the update by clicking the "Share" button in the modal
    share_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="oxd-form-actions orangehrm-buzz-post-modal-actions"]/button[@type="submit" and contains(@class, "oxd-button--main")]')))
    share_button.click()
    print("Post submitted.")
    time.sleep(2)

    # Adding delay to allow the post to appear
    time.sleep(5)

    # Locate the post with the captured time, click the comment button, type "Wow!" and press enter to submit the comment
    try:
        # Find all posts
        posts = driver.find_elements(By.XPATH, '//div[@class="orangehrm-buzz-post"]')
        print(f"Found {len(posts)} posts.")

        found = False
        for index, post in enumerate(posts):
            try:
                # Print the content of the post for debugging
                print(f"Checking post {index + 1}")
                post_content = post.text
                print(f"Post {index + 1} content: {post_content}")

                # Check if the post matches the captured post time
                post_time_element = post.find_element(By.XPATH, f'.//p[@class="oxd-text oxd-text--p orangehrm-buzz-post-time" and text()="{post_time}"]')
                post_time_text = post_time_element.text
                print(f"Post {index + 1} time: {post_time_text}")

                if post_time_text == post_time:
                    # Scroll the post into view
                    driver.execute_script("arguments[0].scrollIntoView();", post)
                    print("Scrolled to the post with the captured post time.")

                    # Find the comment button within the post and click it
                    comment_button = post.find_element(By.XPATH, './/button[@class="oxd-icon-button" and i[@class="oxd-icon bi-chat-text-fill"]]')
                    comment_button.click()
                    print("Comment button clicked.")

                    # Wait for the comment input field to appear, type the comment, and press enter
                    comment_input = WebDriverWait(post, 10).until(
                        EC.presence_of_element_located((By.XPATH, './/input[@placeholder="Write your comment..."]'))
                    )
                    comment_input.send_keys("Wow!")
                    comment_input.send_keys(u'\ue007')  # Press Enter key
                    print("Comment submitted.")
                    found = True
                    break
            except Exception as e:
                print(f"Error in post {index + 1}: {e}")
                continue

        if not found:
            print("Post with the captured post time not found.")
    except Exception as e:
        print(f"Error while trying to submit a comment: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

# Keep browser open
input("Press Enter to close the browser...")

# Close the browser
driver.quit()
