from selenium import webdriver
from webdriver_manager . chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

class Test_SauceDemo:
    def test_invailed_login():
        driver = webdriver . Chrome ()
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        usernameInput = driver.find_element(By.ID, "user-name")
        passwordInput = driver.find_element(By.ID, "password")
        loginButton = driver.find_element(By.ID, "login-button")
        

        usernameInput.send_keys("locked_out_user")
        passwordInput.send_keys("secret_sauce")
        sleep(5)
        loginButton.click()
        sleep(3)
        errorMessage = driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        testResult = errorMessage.text == "Epic sadface: Sorry, this user has been locked out."
        print(f"Test Result : {testResult}")
        sleep(3)

    def test_blank_fields():
        driver = webdriver . Chrome ()
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        loginButton = driver.find_element(By.ID, "login-button")
        loginButton.click()
        sleep(3)
        errorMessage = driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        testResult = errorMessage.text == "Epic sadface: Username is required"
        sleep(3)
        print(f"Test Result : {testResult}")
        sleep(3)

testClass = Test_SauceDemo
testClass.test_blank_fields()      