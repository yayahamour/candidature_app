from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep 


driver = webdriver.Firefox(executable_path='./Driver/geckodriver')

class Selenium_test:
    
    def clic_connexion(user,password):
        driver.find_element_by_link_text('Connexion').click()
        sleep(1)
        # Insert user and password in the login form 
        driver.find_element_by_id('email').send_keys(user)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_name('submit').click()

        # Assert h1 field is correct in this page
        try:
            h1 = driver.find_element_by_tag_name('h1')
            assert h1.text == "CANDIDATURES"
            print('Connexion success')
        except AttributeError:
            print('ERROR ----- h1 not found')
        # Assert Flash login success 
        flash_login = driver.find_element_by_class_name('alert')
        assert 'Vous êtes connecté en tant que :' in flash_login.text 
        print('------------------test login user Done----------------------')
        
        

    def add_candidacy_test(plateform_name, contact_test):
        # To click to the button add candidacy
        driver.find_element_by_link_text('Ajouter candidature').click()
        
        # Insert the candidacy in the form 
        driver.find_element_by_id('plateforme').send_keys(plateform_name) 
        driver.find_element_by_id('entreprise').send_keys('Ikea') 
        driver.find_element_by_id('lieu').send_keys("Lille") 

        # Click on the button add candidacy
        driver.find_element_by_name('submit').click()

        # Assert flash element added success 
        try:
                
            flash_succes = driver.find_element_by_class_name('alert').text
            assert 'Nouvelle Candidature ajouté' in flash_succes 
            # Assert element is on dashboard's following place => Front test
            td_entreprise_xpath = "//tbody/tr[2]/td[1]"
            td_entreprise = driver.find_element(By.XPATH, td_entreprise_xpath)
            assert td_entreprise.text in plateform_name
            print('------------------test add candidacy Done with success----------------------')

        except:
            print(' -------ERROR!  Add candidacy test error : Plateform name not at the good place --------ERROR!')


    def delete_candidacy_test() :
        # Click on the third button delete item 
        delete_xpath = '//tbody/tr/td[12]/a[2]'
        try:
            driver.find_element(By.XPATH, delete_xpath).click()
            flash_succes = driver.find_element_by_class_name('alert').text
            assert "Candidature supprimée avec succès" in flash_succes
            print('------------------delete candidacy done----------------------')

        except:
            print('Cannot found the delete button --------ERROR!')

        # need order dashboard by last added to assert 'word' not in [xpath row[1]] 
        # Or need candidacy id on admin dashboard to assert deleted
        # Or need to use Candidacy.query.filter_by(name=["element to check"]) methods ?

        
    def clic_offres():
        driver.find_element_by_link_text('Offres').click()
        try:
            h1 = driver.find_element_by_tag_name('h1')
            assert h1.text == "OFFRES D'ALTERNANCE"
            print('------------------Offres page reached with success---------------------')
        except AttributeError:
            print('ERROR : Title not found --------ERROR! ')
        
        
    def add_offer_test(entreprise_name, contact_test):
        # To click to the button add candidacy
        driver.find_element_by_link_text('Ajouter offre').click()
        
        # Insert the candidacy in the form 
        driver.find_element_by_id('entreprise').send_keys(entreprise_name) 
        driver.find_element_by_id('lieu').send_keys('Ikea') 
        driver.find_element_by_id('contact_full_name').send_keys(contact_test) 

        # Click on the button add candidacy
        driver.find_element_by_name('submit').click()

        # Assert flash element added success 
        try:
                
            flash_succes = driver.find_element_by_class_name('alert').text
            assert "Nouvelle offre d'emploi ajoutée" in flash_succes 
            td_entreprise_xpath = "//tbody/tr[2]/td[2]"
            td_entreprise = driver.find_element(By.XPATH, td_entreprise_xpath)
            assert td_entreprise.text == entreprise_name
            print('------------------test add offer Done----------------------')
        except:
            print('Error add offer test : Plateform name not found-------ERROR! ')



    def delete_offer_test() :
        # Click on the third button delete item 
        
        try:
            delete_xpath = '//tbody/tr[2]/td[10]/a[3]'
            driver.find_element(By.XPATH, delete_xpath).click()
            flash_succes = driver.find_element_by_class_name('alert').text
            assert "Offre d'emploi supprimée avec succès" in flash_succes
            print('------------------test offer deleted with succées ---------')
        except:
            print('Cannot found the delete button   --------ERROR!')

        # need order dashboard by last added to assert 'word' not in [xpath row[1]] 
        # Or need candidacy id on admin dashboard to assert deleted
        # Or need to use Candidacy.query.filter_by(name=["element to check"]) methods ?

        print('------------------delete candidacy n°3 done----------------------')
   