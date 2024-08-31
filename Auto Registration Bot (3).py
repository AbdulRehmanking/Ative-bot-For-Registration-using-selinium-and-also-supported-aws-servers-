import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Define the URL of the website
url = 'https://pieraksts.mfa.gov.lv/en/uited-arab-emirates/index'

# Define the data to be inserted into the input fields
data = {
    'input1': 'Bakhtawar Ali',
    'input2': 'Keyani',
    'input3': 'Bakhtawarali64@gmail.com',
    'input4': 'Bakhtawarali64@gmail.com',
    'input5': '+923133100601',
}
reference = "PAS31-276031"
# Define the locators for the input fields and the next button
locators = {
    'input1': (By.ID, 'Persons[0][first_name]'),
    'input2': (By.ID, 'Persons[0][last_name]'),
    'input3': (By.ID, 'e_mail'),
    'input4': (By.ID, 'e_mail_repeat'),
    'input5': (By.ID, 'phone'),
    'next_button': (By.CSS_SELECTOR, '#step1-next-btn > button')
}

# Create a new instance of the Chrome driver
options = uc.ChromeOptions()
# Add any necessary options here (optional)
# options.add_argument('--headless')  # Uncomment this line to run in headless mode

driver = uc.Chrome(options=options)
driver.implicitly_wait(3)


start_over = True



def step1():
    # Fill in the input fields
    driver.get(url)
    for key, value in data.items():
        input_element = driver.find_element(*locators[key])
        input_element.clear()
        input_element.send_keys(value)

    # Click the next button
    next_button = driver.find_element(*locators['next_button'])
    next_button.click()


def step2():
    select_service = driver.find_element(By.CSS_SELECTOR, "#mfa-form2 > div > div.dropdown > div > section > div > div.form-services--title.js-services")
    select_service.click()
    # Wait for some time to observe the result (optional)
    
    
    first_checkbox_div = driver.find_element(By.CSS_SELECTOR, '#mfa-form2 > div > div.dropdown > div > section > div > div.services--wrapper.active > div:nth-child(5)')
    first_checkbox_div.click()
    
    
    accept = driver.find_element(By.CSS_SELECTOR, '#mfa-form2 > div > div.dropdown > div > section > div > div.services--wrapper.active > section.description.active > div.description-text--wrapper > div.js-popup-checkbox.form-checkbox--wrapper')
    accept.click()
    
    add_button = driver.find_element(By.CSS_SELECTOR, '#mfa-form2 > div > div.dropdown > div > section > div > div.services--wrapper.active > section.description.active > div.description-text--wrapper > div.info-notification.margin-bottom-40 > button')
    add_button.click()
    
    
    next_step_button = driver.find_element(By.CSS_SELECTOR, '#step2-next-btn > button')
    
    next_step_button.click()
    

def step3():
    print(" ")
            
    while True:
        
        time.sleep(1)
        message = driver.find_element(By.CSS_SELECTOR, "#mfa-form3 > div > div.form-content--wrapper > div > div")

        if message.text != "Currently all dates are fully booked" or message.text == "":
            break
        driver.refresh()
    
    available_dates = None
    next_btn_selector = "#calendar > div > div > div.calendar-nav--wrapper > button.calendar-next"
    prev_btn_selector = "#calendar > div > div > div.calendar-nav--wrapper > button.calendar-prev"
    counts = 0
    next = True
    total_dates = 0
    next_months = 0
    available_dates
    
    while True:
        try:
            #calendar-daygrid
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar-daygrid'))
            )
        except: 
            pass
        message = driver.find_element(By.CSS_SELECTOR, "#mfa-form3 > div > div.form-content--wrapper > div > div")

        if message.text == "Currently all dates are fully booked":
            driver.refresh()
            continue
        
        # available_dates = driver.find_elements(By.CSS_SELECTOR, ".cal-active")
        try:
            available_dates = driver.execute_script("return document.getElementsByClassName('cal-active');")
        except: 
            available_dates = []
                
        if len(available_dates) > 0:
            total_dates = len(available_dates)
            next_months = counts
            break
        
        if counts == 4:
            driver.refresh()
            counts = 0
        
        counts += 1
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, next_btn_selector)
            next_btn.click()
        except:
            counts = 0
            driver.refresh()
        time.sleep(0.5)
        
        print("." , end="")
        
    first_date = available_dates[-1]
    first_date.click()
    
    WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#services > div.text__time > div > span > select'))
        )


    try:    
        # select last slot of the day
        driver.execute_script("""var name = 'ServiceGroups[0][visit_time]';
                            var element = document.getElementsByName(name)[0];
                            element.value = element.options[Number(element.options.length/2) - 1].value""")
    except:
        pass
    # Click next step button
    next_step_button = driver.find_element(By.CSS_SELECTOR, "#step3-next-btn > button")
    next_step_button.click()
    

def step4():
    # Add Reference Number
    try:
        input_elements = driver.find_elements(By.TAG_NAME, "input")
        for input_element in input_elements:
            # Check if the input type is "text"
            if input_element.get_attribute("type") == "text":
                # Set the value to "123SNK"
                input_element.send_keys("PAS31-276031")
                break
    except:
        pass
    # Agree 
    agree_checkbox_step4 = driver.find_element(By.CSS_SELECTOR, "#gdpr")
    agree_checkbox_step4.click()
        
    # Approve button click
    approve_button = driver.find_element(By.CSS_SELECTOR, "#mfa-form4 > div > div.btn-next-step--wrapper > button")
    # approve_button.click()
    print("Registration Successful")
    
    

STEP = 1

def Auto_Booking():
    global start_over
    global STEP
    

    while start_over:
        try:
            if STEP == 1:            
                step1()
                STEP = 2
            if STEP == 2:
                step2()
                STEP = 3
            if STEP == 3:
                step3()
                STEP = 4
            if STEP == 4:
                step4()
            
            start_over = False
            break
                
        except Exception as e:
            print(e)
            
            if "index" in driver.current_url:
                STEP = 1
            elif "step2" in driver.current_url:
                STEP = 2
            elif "step3" in driver.current_url:
                STEP = 3
            elif "step4" in driver.current_url:
                STEP = 4

        finally:
            # Close the driver
            pass

    time.sleep(10000)


Auto_Booking()
