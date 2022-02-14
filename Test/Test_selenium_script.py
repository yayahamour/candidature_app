from Test_selenium_func import Selenium_test,  driver 
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep 


url = 'http://candidature-app1.herokuapp.com/profil'


driver.get(url)

Selenium_test.clic_connexion("yayahamour@gmail.com","1234") 

Selenium_test.add_candidacy_test('Linkedin','eric@gmail.com') 

Selenium_test.delete_candidacy_test() 

Selenium_test.clic_offres()

Selenium_test.add_offer_test("Apple", "Eric")
Selenium_test.delete_offer_test() 


driver.quit()