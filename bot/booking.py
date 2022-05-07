from datetime import datetime
from bot.constants import BASE_URL
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotVisibleException,
    TimeoutException,
    NoSuchElementException
    )
from selenium.webdriver.common.keys import Keys


class MyBot():
    """My class"""

    def __init__(
        self,
        driver=webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=webdriver.FirefoxOptions()
            ),
        teardown=False,
        ):
        self.driver = driver
        self.teardown = teardown
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

    def __str__(self):
        return 'MyBot Class'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    
    def land_first_page(self):
        """My custom method"""

        self.driver.get(BASE_URL)

        try:
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located (
                (By.XPATH,'//div[@id="onetrust-policy"]')            
            ))

            accept_cookies = self.driver.find_element(
                by=By.XPATH,
                value='//button[@id="onetrust-accept-btn-handler"]'
            )
            accept_cookies.click()
        except TimeoutException as e:
            return


    def change_currency(self, currency):
        """Custom method that finds element that allows to change currency and then change it to value passed in the argument"""

        currency_set_by_default = self.driver.find_element(
            by=By.XPATH,
            value='//button[@data-tooltip-text="Choose your currency"]/span[1]/span[1]'
        )

        if currency in currency_set_by_default.text:
            pass
        else:
            currency_tab = self.driver.find_element(
                by=By.XPATH,
                value='//button[@data-tooltip-text="Choose your currency"]'
                )
            currency_tab.click()

            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located (
                (By.XPATH,'//div[@aria-label="Select your currency"]')            
            ))
            try:
                currency_picker = self.driver.find_element(
                    by=By.XPATH,
                    value=f'//a[@data-modal-header-async-url-param="changed_currency=1;selected_currency={currency};top_currency=1"]'
                )
                currency_picker.click()
            except NoSuchElementException as e:

                picker_tab = self.driver.find_element(
                    by=By.XPATH,
                    value='//body',
                )
                picker_tab.send_keys(Keys.PAGE_DOWN)
                currency_picker = self.driver.find_element(
                    by=By.XPATH,
                    value=f'//a[contains(@data-modal-header-async-url-param, "selected_currency={currency}")]'
                )
                currency_picker.click()

                # '//li[@data-i="0" and contains(@data-label,"{where}")]'


    def filter_destination(self, where):
        """Custom method that filters destination by values provided as an arguments."""
        
        try:
            destination_form = self.driver.find_element(
                by=By.XPATH,
                value='//input[@id="ss" and @aria-label="Type your destination"]',
            )
            destination_form.clear()
            destination_form.send_keys(where)
            
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located (
                (By.XPATH,'//ul[@aria-label="List of suggested destinations "]')            
            ))

            confirm_choice = self.driver.find_element(
                by=By.XPATH,
                value=f'//li[@data-i="0" and contains(@data-label,"{where}")]'
            )
            confirm_choice.click()

        except ElementNotVisibleException as e:
            print(e)


    def pick_stay_date(self, check_in, check_out):
        """Custom methon that pick dates for check in and checking out."""

        # Format dates coming as str from function call to dates.
        # For future use in other searches.
        check_in_date = datetime.fromisoformat(check_in)
        check_out_date = datetime.fromisoformat(check_out)
        check_in_checked = False
        check_out_checked = False


        if check_in_checked == False:
            while True:
                        
                next_page_elem = self.driver.find_element(
                    by=By.XPATH,
                    value='//div[@data-bui-ref="calendar-next"]'
                )

                date_element_checker = self.driver.find_elements(
                    by=By.XPATH,
                    value='//div[contains(@id,"bui-calendar-")]',
                )

                if check_in_date.strftime("%B %Y") not in [x.text for x in date_element_checker]:
                    next_page_elem.click()
                else:
                    # Finds table element that is responsible for picking a check in date and clicks it.
                    check_in_element = self.driver.find_element(
                        by=By.XPATH,
                        value=f'//td[@data-date="{check_in_date.date()}"]',
                    )
                    check_in_element.click()
                    check_in_checked = True
                    break
        
        if check_out_checked == False:
            while True:

                next_page_elem = self.driver.find_element(
                    by=By.XPATH,
                    value='//div[@data-bui-ref="calendar-next"]'
                )

                date_element_checker = self.driver.find_elements(
                    by=By.XPATH,
                    value='//div[contains(@id,"bui-calendar-")]',
                )

                if check_out_date.strftime("%B %Y") not in [x.text for x in date_element_checker]:
                    next_page_elem.click()
                else:
                    # Finds table element that is responsible for picking a check in date and clicks it.
                    check_out_element = self.driver.find_element(
                        by=By.XPATH,
                        value=f'//td[@data-date="{check_out_date.date()}"]',
                    )
                    check_out_element.click()
                    check_out_checked = True
                    break      
    
    def send_adult_info(self, adult):
        """Sends info about number of adults that will travel."""

        # Finds input element.
        input_element = self.driver.find_element(
            by=By.XPATH,
            value='//label[@id="xp__guests__toggle"]',
        )
        input_element.click()
        WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located (
                (By.XPATH,'//div[@id="xp__guests__inputs-container"]')            
        ))
                    
        # Picks Number of adults.
        while True:
            add_adults_button = self.driver.find_element(
                by=By.XPATH,
                value='//div[@class="sb-group__field sb-group__field-adults"]/div[1]/div[2]/button[@data-bui-ref="input-stepper-add-button"]'
            )
            subtract_adults_button = self.driver.find_element(
                by=By.XPATH,
                value='//div[@class="sb-group__field sb-group__field-adults"]/div[1]/div[2]/button[@data-bui-ref="input-stepper-subtract-button"]'
            )
            default_number_of_adults = self.driver.find_element(
                by=By.XPATH,
                value='//div[@class="sb-group__field sb-group__field-adults"]/div[1]/div[2]/span[@class="bui-stepper__display"]'
            )

            if int(default_number_of_adults.text) < adult:
                add_adults_button.click()
            elif int(default_number_of_adults.text) > adult:
                subtract_adults_button.click()
            else:
                break
    
    def send_children_info(self, childrens):
        """
        Sends info about number of children that are traveling.
        Children argument have to be a tuple of children's ages
        While number of values inside this tuple (len(tuple)) coreponds to number of children.
        
        """

        # Finds input element.
        input_element = self.driver.find_element(
            by=By.XPATH,
            value='//label[@id="xp__guests__toggle"]',
        )
        input_element.click()
        WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located (
                (By.XPATH,'//div[@id="xp__guests__inputs-container"]')            
        ))

        for index, child in enumerate(childrens):
            
            # Elements!
            add_child_element = self.driver.find_element(
                by=By.XPATH,
                value='//button[@aria-label="Increase number of Children"]'
            )
            add_child_element.click()

            # Wait till elements shows up.
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located (
                (By.XPATH,f'//select[@aria-label="Child {index + 1} age"]')            
            ))

            # Select value of child's age.
            age_selector = self.driver.find_element(
                by=By.XPATH,
                value=f'//select[@aria-label="Child {index + 1} age"]'
            )
            age_selector.click()
            pick_age_elem = self.driver.find_element(
                by=By.XPATH,
                value=f'//select[@aria-label="Child {index + 1} age"]/option[@value="{child}"]'
            )
            pick_age_elem.click()

    def pick_number_of_rooms(self, rooms_num):
        """
        Sends info about number of room that user wants to book.
        """

        # Finds input element.
        input_element = self.driver.find_element(
            by=By.XPATH,
            value='//label[@id="xp__guests__toggle"]',
        )
        input_element.click()
        WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located (
                (By.XPATH,'//div[@id="xp__guests__inputs-container"]')            
        ))


        # Find default number of rooms in HTML.
        default_rooms_num = self.driver.find_element(
            by=By.XPATH,
            value='//div[@class="sb-group__field sb-group__field-rooms"]/div[1]/div[2]/span[@class="bui-stepper__display"]'
        )

        if rooms_num > int(default_rooms_num.text):
            while True:

                add_rooms_button = self.driver.find_element(
                    by=By.XPATH,
                    value='//div[@class="sb-group__field sb-group__field-rooms"]/div[1]/div[2]/button[@aria-label="Increase number of Rooms"]'
                )
                add_rooms_button.click()

                if rooms_num == int(default_rooms_num.text):
                    break
                else:
                    continue
    
    def send_all_info(self):
        """
        Sends entire form with all inserted data to booking.com service to filter a booking options.
        """

        search_button = self.driver.find_element(
            by=By.XPATH,
            value="//button[@data-sb-id='main']",
        )
        search_button.click()
