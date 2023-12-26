import pytest
from selenium import webdriver
from webdriver_manager . chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import random

class Test_DemoClass:
    # prefix => test_ (fonk. adının önüne yazmak zorundayız.)
    def setup_method(self): #Her test başlangıcında çalışacak method
        self.driver = webdriver . Chrome ()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()

    def tearDown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize("username, password", [("user_user", "secret_sauce"),("locked_out_user", "sssecret_sauce"),("locked_out_user", "secret_sauce")])
    def test_invailed_login(self, username, password):
        self.driver.get("https://www.saucedemo.com/")

        WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.ID, "user-name")))
        usernameInput = self.driver.find_element(By.ID, "user-name")
        usernameInput.send_keys(username)

        WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.ID, "password")))
        passwordInput = self.driver.find_element(By.ID, "password")
        passwordInput.send_keys(password)

        loginButton = self.driver.find_element(By.ID, "login-button")
        WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.ID, "login-button")))
        loginButton.click()

        errorMessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errorMessage.text == "Epic sadface: Sorry, this user has been locked out."


    def test_blank_fields(self):
        self.driver.get("https://www.saucedemo.com/")
        WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.ID, "login-button")))
        loginButton = self.driver.find_element(By.ID, "login-button")
        loginButton.click()
        errorMessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errorMessage.text == "Epic sadface: Username is required"

    
    def test_blank_password(self):

        self.driver.get("https://www.saucedemo.com/")

        usernameInput = self.driver.find_element(By.ID, "user-name")
        usernameInput.send_keys("standard_user")
        loginButton = self.driver.find_element(By.ID, "login-button")
        loginButton.click()
        errorMessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errorMessage.text == "Epic sadface: Password is required"

    def test_successful_login(self):

        self.driver.get("https://www.saucedemo.com/")

        usernameInput = self.driver.find_element(By.ID, "user-name")
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID, "password")
        passwordInput.send_keys("secret_sauce")
        loginButton = self.driver.find_element(By.ID, "login-button")
        loginButton.click()
        headerLogo = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//*[@id='header_container']/div[1]/div[2]/div")))
        assert headerLogo.text == "Swag Labs"

        current_url = self.driver.current_url
        if current_url == "https://www.saucedemo.com/inventory.html":
            print("Kullanıcı başarıyla yönlendirildi.")
        else:
            print("Yönlendirme başarısız oldu.")
        
        listOfProduct = self.driver.find_elements(By.CLASS_NAME, "inventory_item_label")
        assert len(listOfProduct) == 6
        
        addToCart = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH , "//*[@id='add-to-cart-test.allthethings()-t-shirt-(red)']")))

        self.driver.execute_script("window.scrollTo(0,500)")
        addToCart.click()
        remove = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH , "//*[@id='remove-test.allthethings()-t-shirt-(red)']")))

        assert remove.text == "Remove"
        
    def test_Go_To_Basket(self):
        self.test_successful_login()
        self.driver.execute_script("window.scrollTo(0,0)")
        sleep(5)
        basket = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.ID, "shopping_cart_container")))
        basket.click()
        current_url = self.driver.current_url
        assert current_url == "https://www.saucedemo.com/cart.html"
        sleep(3)

    def test_go_to_basket_and_remove(self):
        self.test_Go_To_Basket()

        remove = self.driver.find_element(By.ID, "remove-test.allthethings()-t-shirt-(red)")
        remove.click()
        sleep(5)
        product_counter = WebDriverWait(self.driver, 5).until(ec.invisibility_of_element((By.CSS_SELECTOR, "#shopping_cart_container span")))
        if(product_counter):
            print("Ürün kaldırma işlemi başarılı.")
        else:
            print("Ürün Sepetten Kaldırılamadı!")
        sleep(5)

    def test_checkout(self):
        self.test_Go_To_Basket()

        checkout = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.ID, "checkout")))
        checkout.click()
        current_url = self.driver.current_url
        assert current_url == "https://www.saucedemo.com/checkout-step-one.html"

    def test_successful_order(self):
        self.test_checkout()

        first_name = self.driver.find_element(By.ID, "first-name")
        first_name.send_keys("Tuğçe")

        last_name = self.driver.find_element(By.ID, "last-name")
        last_name.send_keys("Taşkın")

        postal_code = self.driver.find_element(By.ID, "postal-code")
        postal_code.send_keys("34180")

        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()

        current_url = self.driver.current_url
        assert current_url == "https://www.saucedemo.com/checkout-step-two.html"

        finish = self.driver.find_element(By.ID, "finish")
        finish.click()

        current_url = self.driver.current_url
        assert current_url == "https://www.saucedemo.com/checkout-complete.html"

        success_order_message = self.driver.find_element(By.CSS_SELECTOR, "#checkout_complete_container h2")
        assert success_order_message.text == "Thank you for your order!"


    def test_checkout_blank(self):
        self.test_checkout()

        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()

        error_message = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//*[@id='checkout_info_container']/div/form/div[1]/div[4]/h3")))
        assert error_message.text == "Error: First Name is required"

    def test_random_product(self):
        self.driver.get("https://www.saucedemo.com/")

        usernameInput = self.driver.find_element(By.ID, "user-name")
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID, "password")
        passwordInput.send_keys("secret_sauce")
        loginButton = self.driver.find_element(By.ID, "login-button")
        loginButton.click()

        listOfProduct = self.driver.find_elements(By.CLASS_NAME, "inventory_item_label")
        assert len(listOfProduct) == 6

        random_index = random.randint(0, len(listOfProduct) - 1)
        selected_product = listOfProduct[random_index]
        self.driver.execute_script("arguments[0].scrollIntoView();", selected_product)
        sleep(5)

        addToCartButton = selected_product.find_element(By.CSS_SELECTOR, ".inventory_item_description.pricebar button")
        addToCartButton.click()
        sleep(5)


        
