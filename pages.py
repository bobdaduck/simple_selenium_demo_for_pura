from selenium import webdriver
from selenium.webdriver.common.by import By
from .browser import Driver
import time

class Home:

    def __init__(self, driver):
        self.driver = driver
        self.smart_device_pre_order_btn = (By.XPATH, "//*[@id=\"product_form_1591193796717\"]/button")
        self.popup = (By.XPATH, "//*[@id=\"shopify-section-popup\"]/aside/div/button")
        self.url = "https://trypura.com"

    def get_smart_device_pre_order_btn(self):  # methods instead of properties keep code from automatically executing
        return self.driver.find_element(*self.smart_device_pre_order_btn)

    def wait_for_popup(self):
        time.sleep(10) # chromedriver always starts with fresh cache so this popup will always happen
        self.driver.find_element(*self.popup).click()

    def is_at(self):
        try:
            current_url = self.driver.current_url
            if self.url == current_url:
                return True
            else:
                return False
        except:
            return False

    def goto(self):
        self.driver.get(self.url)
        self.wait_for_popup()



class Cart:

    def __init__(self, driver):
        self.suggestions_list = (By.CLASS_NAME, "Cart__UpsellList")
        self.remove_item = (By.CLASS_NAME, "CartItem__Remove")
        self.close_btn = (By.XPATH, '//*[@id="sidebar-cart"]/div/button')
        self.items_in_cart = (By.CLASS_NAME, "Cart__ItemList") #use findElements rather than findElement, then get CartItem__Title Heading for each for comparison
        self.cart_checkout_btn = (By.ID, "cart-drawer-checkout-button")
        self.cart_total = (By.XPATH, "//*[@id=\"cart-drawer-checkout-button\"]/span[3]")
        self.driver = driver

    def suggestions_contain(self, item_name):
        if not self.is_loaded():
            self.goto_and_wait_for_cart()
        suggestions_list = self.driver.find_element(*self.suggestions_list)
        innertext = suggestions_list.get_attribute('innerHTML')
        if item_name in innertext: 
            return True
        else:
            return False

    def clear(self):
        if not self.is_loaded():
            self.goto_and_wait_for_cart()
        #cart_items = self.driver.find_element(*self.items_in_cart)
        remove_links = self.driver.find_elements(By.CLASS_NAME, "CartItem__Remove")
        for item in remove_links:
            try:
                item.click()
            except:
                pass

    def find_item_in_suggestions(self, item_name):
        suggestions_list = self.driver.find_element(* self.suggestions_list)
        cartItems = suggestions_list.driver.find_elements(By.CLASS_NAME, "CartItem") 
        for cartItem in cartItems:
            innertext = cartItem.get_attribute('innerHTML')
            if item_name in innertext:
                return cartItem


    def get_total(self):
        time.sleep(5)
        return float(self.driver.find_element(*self.cart_total).text.split("$")[1])

    def checkout(self):
        self.driver.find_element(*self.cart_checkout_btn).click()
    
    def is_empty(self):
        time.sleep(10)
        if ("Your cart is empty" in self.driver.page_source):
            return True
        else:
            return False

    def close(self):
        self.driver.find_element(*self.close_btn).click()

    def is_loaded(self):
        try:
            self.driver.find_element(*self.cart_checkout_btn)
            self.driver.find_element(By.CLASS_NAME, "Drawer__Title")
            self.driver.find_element(*self.suggestions_list)
        except:
            return False

    def goto_and_wait_for_cart(self):
        try:
            self.driver.find_element(*self.cart_top_btn).click()
            time.sleep(6)
        except: #if cart is already open this button won't be clickable
            time.sleep(6) # There's more elegant ways to do this.

class Fragrance:

    def __init__(self, driver):
        self.driver = driver
        self.subscribe_toggle = (By.XPATH, "//*[@id=\"recurring\"]")
        self.one_time_purchase_toggle = (By.XPATH, "//*[@id=\"one_time\"]")
        self.add_to_cart_btn = (By.CLASS_NAME, "ProductForm__AddToCart ")
        self.url = "https://www.trypura.com/collections/fragrances/products/violet-yarrow"

    def subscribe(self):  # methods instead of properties keep code from automatically executing
        if not self.is_at():
            self.goto()
        add_to_cart_btn = self.driver.find_element(*self.add_to_cart_btn)
        # self.driver.find_element(*self.subscribe_toggle).click() # needs handling for when already toggled, but its fine without for this test case
        self.driver.execute_script("arguments[0].scrollIntoView();", add_to_cart_btn)
        add_to_cart_btn.click()
        time.sleep(5)

    def add_as_one_time_purchase(self):
        if not self.is_at():
            self.goto()
        add_to_cart_btn = self.driver.find_element(*self.add_to_cart_btn)
        one_time_purchase_toggle = self.driver.find_element(*self.one_time_purchase_toggle)
        self.driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(5)
        self.driver.execute_script("arguments[0].scrollIntoView();", one_time_purchase_toggle)
        time.sleep(5)
        one_time_purchase_toggle.click()
        self.driver.execute_script("arguments[0].scrollIntoView();", add_to_cart_btn)
        add_to_cart_btn.click()
        time.sleep(5)

    def is_at(self):
        try:
            current_url = self.driver.current_url
            if self.url == current_url:
                return True
            else:
                return False
        except:
            return False

    def goto(self):
        self.driver.get(self.url)
        time.sleep(5)


class Checkout:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.trypura.com/collections/fragrances/products/violet-yarrow"
        self.cart_total = (By.XPATH, "//*[@id=\"order-summary\"]/div/div[3]/table/tfoot/tr/td/span[2]")
        self.coupon_code_field = (By.ID, "checkout_reduction_code")
        self.apply_coupon_btn = (By.XPATH, "//*[@id=\"order-summary\"]/div/div[2]/form[2]/div/div/div/button")
        self.back_to_cart_btn = (By.XPATH, "/html/body/div[1]/div/div/main/div[1]/form/div[2]/a/span")
        #self.back_to_cart_btn = (By.XPATH, "//*[@id=\"edit_checkout_429553653\"]/div[3]/a")
                                              
    def get_smart_device_pre_order_btn(self):  # methods instead of properties keep code from automatically executing
        return self.driver.find_element(*self.smart_device_pre_order_btn)

    def get_total(self):

        return float(self.driver.find_element(*self.cart_total).text.split("$")[1])

    def apply_code(self, code):
        self.driver.find_element(*self.coupon_code_field).send_keys(code)
        self.driver.find_element(*self.apply_coupon_btn).click()
    
    def go_back(self):
        back_btn = self.driver.find_element(*self.back_to_cart_btn)
        self.driver.execute_script("arguments[0].scrollIntoView();", back_btn)
        back_btn.click()
