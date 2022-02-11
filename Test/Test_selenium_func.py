from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep 


driver = webdriver.Firefox(executable_path='./Driver/geckodriver')

class Selenium_test:
    
    def login_test(user, password) :
        # Insert user and password in the login form 
        driver.find_element_by_id('email').send_keys(user)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_name('submit').click()
        
        # Assert h1 field is correct in this page
        # Try + assert ou l'un ou l'autre uniquement ? 
        try:
            h1 = driver.find_element_by_tag_name('h1')
            assert h1.text == "CANDIDATURES"
        except AttributeError:
            print('ERROR ----- h1 not found')
        # Assert Flash login success 
        flash_login = driver.find_element_by_class_name('alert')
        assert 'Vous êtes connecté en tant que :' in flash_login.text 
        print('------------------test login user Done----------------------')
        
        
