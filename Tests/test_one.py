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
            "newCommandTimeout": 4000,
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
    # time.sleep(3)


def test_tc2_browsing(driver: WebDriver):
    test_tc1_login(driver)
    
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).'
        'setMaxSearchSwipes(10).scrollIntoView(new UiSelector().text("$7.99"))',
    )

    allProducts = driver.find_elements(
        AppiumBy.XPATH, '//android.widget.TextView[@content-desc="test-Item title"]'
    )
    all_add_toCart_Btns = driver.find_elements(
        AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-ADD TO CART"]'
    )
    for product in range(len(allProducts)):
        if allProducts[product].text == "Sauce Labs Onesie":
            all_add_toCart_Btns[product].click()
        if allProducts[product].text == "Test.allTheThings() T-Shirt (Red)":
            all_add_toCart_Btns[product].click()


def test_tc3_product_detls(driver: WebDriver):
    test_tc1_login(driver)
    
    visted = set()
    flag = 0

    while True:
        allProducts = driver.find_elements(
            AppiumBy.XPATH, '//android.widget.TextView[@content-desc="test-Item title"]'
        )
        new_found = False
        for index in range(len(allProducts)):
            ExpectedProductName = allProducts[index].text

            if ExpectedProductName in visted:
                continue

            visted.add(ExpectedProductName)
            new_found = True
            allProducts[index].click()

            # product name on details page (first TextView under test-Description)
            ActualProductName = driver.find_element(
                AppiumBy.XPATH,
                '//android.view.ViewGroup[@content-desc="test-Description"]/android.widget.TextView[1]',
            ).text

            # assertion
            assert ExpectedProductName == ActualProductName
            assert driver.find_element(
                AppiumBy.XPATH,
                '//android.view.ViewGroup[@content-desc="test-Description"]/android.widget.TextView[1]',
            ).is_displayed()

            # go back to list and re-fetch products
            driver.back()

            allProducts = driver.find_elements(
                AppiumBy.XPATH,
                '//android.widget.TextView[@content-desc="test-Item title"]',
            )

        if not new_found:
            try:
                for _ in range(1):
                    if flag == 2:
                        return   # <-- stop test completely
                    driver.execute_script(
                        "mobile: scrollGesture",
                        {
                            "left": 0,
                            "top": 0,
                            "width": 1080,
                            "height": 1920,
                            "direction": "down",
                            "percent": 0.5,
                        },
                    )
                    flag += 1

            except:
                break


def test_tc4_hamburger_menu(driver: WebDriver):
    test_tc1_login(driver)
    
    menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    menu.click()

    closeMenu = driver.find_element(
        AppiumBy.XPATH,
        '//android.view.ViewGroup[@content-desc="test-Close"]/android.widget.ImageView',
    )
    closeMenu.click()

    menu.click()
    time.sleep(0.5)
    # Close the Menu by Swipping left
    driver.execute_script(
        "mobile: swipeGesture",
        {
            "left": 1000,
            "top": 1582,
            "width": 200,
            "height": 200,
            "direction": "left",
            "percent": 1,
        },
    )
    time.sleep(0.5)


def test_tc5_QR(driver: WebDriver):
    test_tc1_login(driver)
    
    menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    menu.click()

    qr_btn = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("QR CODE SCANNER")'
    )
    qr_btn.click()

    try:
        permission_popup = driver.find_element(
            AppiumBy.ID, "com.android.permissioncontroller:id/content_container"
        )
        if permission_popup.is_displayed():
            driver.find_element(
                AppiumBy.ID,
                "com.android.permissioncontroller:id/permission_allow_one_time_button",
            ).click()
    except:
        pass

    assert driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.ViewGroup").instance(18)',
    ).is_displayed()


def test_tc6_geolocation(driver: WebDriver):
    test_tc1_login(driver)

    menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    menu.click()

    geoLocation_Btn = driver.find_element(
        AppiumBy.XPATH, '//android.widget.TextView[@text="GEO LOCATION"]'
    )
    geoLocation_Btn.click()

    try:
        permission_popup = driver.find_element(
            AppiumBy.ID, "com.android.permissioncontroller:id/content_container"
        )
        if permission_popup.is_displayed():
            driver.find_element(
                AppiumBy.ID,
                "com.android.permissioncontroller:id/permission_allow_one_time_button",
            ).click()
    except:
        pass

    # lat = 48.858844
    # long = 2.294351
    # alt = 10
    # driver.set_location(latitude=lat, longitude=long, altitude=alt)

    latitudeLocator = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-latitude"))
    )
    longitudeLocator = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-longitude"))
    )

    assert latitudeLocator.is_displayed() and longitudeLocator.is_displayed()

    assert float(latitudeLocator.text) and float(longitudeLocator.text)


def draw_line(driver: WebDriver, start_x, start_y, end_x, end_y, duration=2000):
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")
    actions = ActionBuilder(driver, mouse=finger)

    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.move_to_location(end_x, end_y)
    actions.pointer_action.pause(duration / 1000)
    actions.pointer_action.pointer_up()

    actions.perform()


def test_tc7_drawing(driver: WebDriver):
    test_tc1_login(driver)
    
    menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    menu.click()

    drawing_btn = driver.find_element(
        AppiumBy.XPATH, '//android.widget.TextView[@text="DRAWING"]'
    ).click()

    # Draw a square
    draw_line(driver, 200, 800, 600, 800)  # top edge
    draw_line(driver, 600, 800, 600, 1200)  # right edge
    draw_line(driver, 600, 1200, 200, 1200)  # bottom edge
    draw_line(driver, 200, 1200, 200, 800)  # left edge

    save_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-SAVE")
    save_btn.click()

    try:
        permission_popup = driver.find_element(
            AppiumBy.ID, "com.android.permissioncontroller:id/content_container"
        )
        if permission_popup.is_displayed():
            driver.find_element(
                AppiumBy.ID,
                "com.android.permissioncontroller:id/permission_allow_button",
            ).click()
    except:
        pass

    driver.execute_script(
        "mobile: startActivity",
        {
            "wait": True,
            "stop": True,
            "action": "android.intent.action.MAIN",
            "component": "com.google.android.apps.photos/com.google.android.apps.photos.home.HomeActivity",
            "categories": ["android.intent.category.LAUNCHER"],
            "flags": "0x10200000",
        },
    )
    assert WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                "//android.widget.ImageView[matches(@content-desc, 'Photo taken on .*')]",
            )
        )
    ).is_displayed()
    driver.back()


def test_tc8_about(driver: WebDriver):
    test_tc1_login(driver)
    
    menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    menu.click()
    about_btn = driver.find_element(
        AppiumBy.XPATH, '//android.widget.TextView[@text="ABOUT"]'
    )
    about_btn.click()

    time.sleep(2)

    current_package = driver.current_package

    assert 'chrome' in current_package.lower()


def test_tc9_logout(driver: WebDriver):
    test_tc1_login(driver)
    
    menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    menu.click()
    logout_btn = driver.find_element(
        AppiumBy.XPATH, '//android.widget.TextView[@text="LOGOUT"]'
    )
    logout_btn.click()

    try:
        assert WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ACCESSIBILITY_ID, "test-Username"
            )
        )
    ).is_displayed()
    except:
        pass


def test_tc10_addItems(driver: WebDriver):
    test_tc1_login(driver)
    
    bolt_shirt = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        "new UiScrollable(new UiSelector().scrollable(true))."
        'setMaxSearchSwipes(10).scrollIntoView(new UiSelector().text("Sauce Labs Bolt T-Shirt"))',
    )

    bolt_shirt.find_element(
        By.XPATH, './/android.view.ViewGroup[@content-desc="test-ADD TO CART"]'
    ).click()

    driver.execute_script(
        "mobile: scrollGesture",
        {
            "left": 0,
            "top": 0,
            "width": 1080,
            "height": 1920,
            "direction": "down",
            "percent": 0.4,
        },
    )

    driver.find_element(
        AppiumBy.XPATH,
        '(//android.view.ViewGroup[@content-desc="test-ADD TO CART"])[1]',
    ).click()

    cart_btn = driver.find_element(
        AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Cart"]'
    )
    cart_btn.click()

    elements = driver.find_elements(
        AppiumBy.XPATH,
        '//android.view.ViewGroup[@content-desc="test-Description"]/android.widget.TextView[1]',
    )

    texts = [el.text for el in elements]

    assert "Sauce Labs Bolt T-Shirt" in texts
    assert "Sauce Labs Onesie" in texts
    
    
    driver.execute_script(
        "mobile: scrollGesture",
        {
            "left": 0,
            "top": 0,
            "width": 1080,
            "height": 1920,
            "direction": "down",
            "percent": 0.5,
        },
    )

    checkout_btn = driver.find_element(
        AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-CHECKOUT"]'
    )
    checkout_btn.click()

    firstName = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-First Name")
    lastName = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Last Name")
    postalCode = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code")
    continue_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE")

    firstName.send_keys("Rana")
    lastName.send_keys("Ahmed")
    postalCode.send_keys("816")
    continue_btn.click()
    
    # Get all product prices
    productPrices = driver.find_elements(
        AppiumBy.XPATH,
        '//android.view.ViewGroup[@content-desc="test-Price"]/android.widget.TextView',
    )

    subtotal = 0
    for price in productPrices:
        subtotal += float((price.text).replace("$", "").strip())

    driver.execute_script(
        "mobile: scrollGesture",
        {
            "left": 0,
            "top": 0,
            "width": 1080,
            "height": 1920,
            "direction": "down",
            "percent": 0.5,
        },
    )

    tax_element = driver.find_element(
        AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Tax:")]'
    )
    tax_value = float(tax_element.text.replace("Tax: $", "").strip())

    total_element = driver.find_element(
        AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Total:")]'
    )
    total_value = float(total_element.text.replace("Total: $", "").strip())

    # Assertion
    assert round(subtotal + tax_value, 2) == round(total_value, 2)

    finish_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-FINISH")
    finish_btn.click()

    try:
        thankUMessage = driver.find_element(
            AppiumBy.XPATH, '//android.widget.TextView[@text="THANK YOU FOR YOU ORDER"]'
        )
        assert thankUMessage.is_displayed()
        assert "THANK YOU" in thankUMessage.text
    except Exception as e:
        assert False, f"Thank you message not found: {e}"

    backHome_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-BACK HOME")
    backHome_btn.click()



def test_tc11_filter_low_to_high(driver: WebDriver):
    test_tc1_login(driver)
    
    allPrices = []
    filter_btn = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(5)',
    )
    filter_btn.click()
    lowToHigh_btn = driver.find_element(
        AppiumBy.XPATH, '//android.widget.TextView[@text="Price (low to high)"]'
    )
    lowToHigh_btn.click()
    time.sleep(2)

    while True:
        productPriceElements = driver.find_elements(
            AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "$")]'
        )

        for elem in productPriceElements:
            price = float(elem.text.replace("$", "").strip())
            if price not in allPrices:
                allPrices.append(price)

        try:
            driver.implicitly_wait(0)
            last_element = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located(
                    (
                        AppiumBy.XPATH,
                        '//android.widget.ScrollView[@content-desc="test-PRODUCTS"]/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ImageView',
                    )
                )
            )
            if last_element.is_displayed():
                break
        except:
            driver.execute_script(
                "mobile: scrollGesture",
                {
                    "left": 0,
                    "top": 0,
                    "width": 1080,
                    "height": 1920,
                    "direction": "down",
                    "percent": 0.3,
                },
            )

    for i in range(len(allPrices) - 1):
        assert allPrices[i] <= allPrices[i + 1]


def test_tc12_filter_high_to_low(driver: WebDriver):
    test_tc1_login(driver)
    
    time.sleep(2)

    allPrices = []
    
    filter_btn = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(5)',
    )
    filter_btn.click()
    highToLow_btn = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Price (high to low)"]')
        )
    )
    highToLow_btn.click()
    time.sleep(2)

    while True:
        productPriceElements = driver.find_elements(
            AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "$")]'
        )

        for elem in productPriceElements:
            price = float(elem.text.replace("$", "").strip())
            if price not in allPrices:
                allPrices.append(price)

        try:
            driver.implicitly_wait(0)
            last_element = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located(
                    (
                        AppiumBy.XPATH,
                        '//android.widget.ScrollView[@content-desc="test-PRODUCTS"]/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ImageView',
                    )
                )
            )
            if last_element.is_displayed():
                break
        except:
            driver.execute_script(
                "mobile: scrollGesture",
                {
                    "left": 0,
                    "top": 0,
                    "width": 1080,
                    "height": 1920,
                    "direction": "down",
                    "percent": 0.3,
                },
            )

    for i in range(len(allPrices) - 1):
        assert allPrices[i] >= allPrices[i + 1]
