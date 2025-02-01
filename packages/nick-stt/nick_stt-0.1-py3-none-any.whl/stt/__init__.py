# pip install selenium
# pip install webdriver-manager
from selenium import webdriver
from selenium.webdriver.common.by import By  # To locate elements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd  # To find the location of the file
# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--use-fake-ui-for-media-stream')  # Allow microphone access
chrome_options.add_argument('--headless=new')  # Run in background
#settig up the chrome option with webdriverManager and option
driver =webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = chrome_options)
#creating the url in the chrome browser
website ='https://allorizenproject1.netlify.app/'
#opening in chrome browser
driver.get(website)
rec_file=f'{getcwd()}\\input.txt'

def listen():
    try:
        # Wait for the start button to be clickable
        start_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.ID, 'startButton'))
        )
        start_button.click()
        print("Listening...")
        output_text = ''
        is_second_click = False  # Flag to track button state
        while True:
            # Wait for the output element to be present
            output_element = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()
            # Check if the button text changes
            if 'Start Listening' in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
            elif 'Listening...' in start_button.text:
                is_second_click = True

            # Update the output file if text changes
            if current_text != output_text:
                output_text = current_text
                with open(rec_file, 'w') as file:
                    file.write(output_text.lower())
                print(f"nick: {output_text}")
    except KeyboardInterrupt:
     pass
    except Exception as e:
        print(e)
listen()                                                                    