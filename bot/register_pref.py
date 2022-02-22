from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

DEFAULT_BASE_URL = "https://whentowork.com/"

class RegisterPreference(webdriver.Chrome):
    def __init__(self) -> None:
        # --- SETTINGS CONFIGURATION ---
        options = webdriver.ChromeOptions()
        # Ignoring 'Failed to read descriptor from node connection' in the logs
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # Make chrome stay open
        options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def land_homepage(self):
        self.driver.get(DEFAULT_BASE_URL)
    
    def login(self, username, password):
        # Locate and access login button        
        try: 
            signin_req_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='collapse navbar-collapse']//button[@type='button'][normalize-space()='Sign In']"))
            ).click()
        except:
            print("Sign in button element is not found")
        
        try:
            signin_form = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > form:nth-child(2) > div:nth-child(1)"))
            )
        except:
            print("Sign in form is not found") 
            
        try:    
            WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@id='username']"))
                ).send_keys(username)
            WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@id='password']"))
                ).send_keys(password)
            signin_form.submit()
        except:
            print("Username and/or Password field is not found")
            
    def navigate_forward_a_week(self):
        WebDriverWait(self.driver, 5). until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='ndNextWeek']"))
        ).click()
            
    def register_hour_per_day(self, day, user_sh, user_sm, user_eh, user_em):
        # navigate to 'preference'
        self.driver.find_element(
            By.XPATH, 
            "//td[@title='Your work time preferences']"
        ).click()
        
        pref_table_rows = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@id='PrefTable']/tbody/tr"))
        )
        
        # Store the main window handles
        main_window = self.driver.window_handles[0]
        
        pref_table_rows[day].click()
        hour_pref_select_window = self.driver.window_handles[1]
        
        # Switch to pop up window
        self.driver.switch_to.window(hour_pref_select_window)
        
        Select(self.driver.find_element(
            By.XPATH, "//select[@name='SH']")
        ).select_by_visible_text(user_sh)

        Select(self.driver.find_element(
            By.XPATH, "//select[@name='SM']")
        ).select_by_visible_text(user_sm)

        Select(self.driver.find_element(
            By.XPATH, "//select[@name='EH']")
        ).select_by_visible_text(user_eh)

        Select(self.driver.find_element(
            By.XPATH, "//select[@name='EM']")
        ).select_by_visible_text(user_em)
        
        #add
        self.driver.find_element(By.XPATH, "//input[@name='B3']").click()
        #save
        self.driver.find_element(By.XPATH, "//input[@name='B4']").click()
    
        # Switch back to the main window 
        self.driver.switch_to.window(main_window)
            

