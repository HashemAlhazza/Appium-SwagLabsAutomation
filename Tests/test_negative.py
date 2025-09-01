import pytest
import time
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder


@pytest.fixture(scope="function")
def driver():
    configurations = UiAutomator2Options().load_capabilities(
        {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": "Pixel 3a API 35",
            "app": r"S:\Appium Projects\SwagLabs\Android.SauceLabs.Mobile.Sample.app.2.7.1.apk",
            "appWaitActivity": "*",
            # "chromedriverExecutable" : r"C:\Users\Hashe\Desktop\chromedriver.exe"
            "newCommandTimeout": 1200,
        }
    )

    driver = webdriver.Remote("http://127.0.0.1:4723", options=configurations)
    driver.implicitly_wait(15)
    # Disable idle wait to speed up execution

    yield driver
    driver.quit()


def test_tc1_login(driver: WebDriver):
    user_name_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Username")
    user_name_field.send_keys("standard_user")
    password_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Password")
    password_field.send_keys("secret_sauce")
    login_btn = driver.find_element(
        AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='test-LOGIN']"
    )
    login_btn.click()


def test_unregisterd_user(driver: WebDriver):
    user_name_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Username")
    user_name_field.send_keys("blabla")
    password_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Password")
    password_field.send_keys("blabla123")
    login_btn = driver.find_element(
        AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='test-LOGIN']"
    )
    login_btn.click()

    try:
        errorMessage = driver.find_element(
            AppiumBy.ACCESSIBILITY_ID, "test-Error message"
        )
        assert errorMessage.is_displayed()
    except Exception:
        assert False


def test_locked_out_user(driver: WebDriver):
    user_name_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Username")
    user_name_field.send_keys("locked_out_user")
    password_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Password")
    password_field.send_keys("secret_sauce")
    login_btn = driver.find_element(
        AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='test-LOGIN']"
    )
    login_btn.click()

    try:
        errorMessage = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Sorry, this user has been locked out.")',
        )
        assert errorMessage.is_displayed()
    except Exception:
        assert False


def test_tc3_checkout_info(driver: WebDriver):
    test_tc1_login(driver)

    addProduct = driver.find_element(
        AppiumBy.XPATH,
        '(//android.view.ViewGroup[@content-desc="test-ADD TO CART"])[1]',
    )
    addProduct.click()

    cart_btn = driver.find_element(
        AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Cart"]'
    )
    cart_btn.click()

    checkout_btn = driver.find_element(
        AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-CHECKOUT"]'
    )
    checkout_btn.click()

    firstName = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-First Name")
    lastName = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Last Name")
    postalCodedriver = driver.find_element(
        AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code"
    )

    lastName.send_keys("Ahmed")
    postalCodedriver.send_keys("816")

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE").click()

    errorMessage = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.widget.TextView[contains(@text, "is required")]',
            )
        )
    )
    assert "First Name is required" in errorMessage.text

    lastName.clear()
    firstName.send_keys("Rana")

    errorMessage = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.widget.TextView[contains(@text, "is required")]',
            )
        )
    )
    
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE").click()
    assert "Last Name is required" in errorMessage.text

    postalCodedriver.clear()
    lastName.send_keys("Ahmed")

    errorMessage = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.widget.TextView[contains(@text, "is required")]',
            )
        )
    )
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE").click()
    assert "Postal Code is required" in errorMessage.text
