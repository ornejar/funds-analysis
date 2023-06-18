from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set the path to your Chrome user profile
user_data_dir = "/Users/<username>/Library/Application Support/Google/Chrome/Profile 1"

# Configure ChromeOptions to use the user profile
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={user_data_dir}")

URL = "https://digital.isracard.co.il/personalarea/Login/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)
time.sleep(10)

# # Wait for the login button to be visible and clickableS
# login_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.ID, "login_button_id"))
# )

# Wait for the username input field to be visible
username_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "otpLoginId_SMS"))
)


# Enter the username
username_input.send_keys("ID")

# Wait for the password input field to be visible
password_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "otpLoginLastDigits_SMS"))
)

# Submit the login form
password_input.send_keys("CREDIT_CARD")

# Find the login button by its text
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='שלח קוד לנייד']"))
)
login_button.click()

# Open a new tab for the Google Messages website
driver.execute_script("window.open('https://messages.google.com/web/conversations', 'new_tab')")
driver.switch_to.window(driver.window_handles[1])  # Switch to the newly opened tab

# Wait for the conversation element to be visible and click it
conversation_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Isracard')]"))
)
conversation_element.click()

# Wait for the last message element to be visible
last_message_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-msg.ng-star-inserted:last-child"))
)

# Extract the text from the last message element
message_text = last_message_element.text

# Extract only the numbers from the message text
numbers_only = ''.join(filter(str.isdigit, message_text))

# Switch back to the credit card tab
driver.switch_to.window(driver.window_handles[0])  # Switch back to the original tab

# Find the input field for the code and enter the extracted numbers
code_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "otpInput"))
)
code_input.send_keys(numbers_only)

# Find and click the "enter my account" button
enter_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'כניסה לחשבון שלי')]"))
)
enter_button.click()