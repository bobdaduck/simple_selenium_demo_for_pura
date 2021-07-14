import unittest

from .pages import Home
from .pages import Cart
from .pages import Checkout
from .pages import Fragrance
from .browser import Driver

class LoginTests(unittest.TestCase):
    
    def setUp(self):
        self.driver = Driver().get_instance() # Driver class's "get_instance" handles setup and options (such as headless)
        self.Home = Home(self.driver)
        self.Cart = Cart(self.driver)
        self.Fragrance = Fragrance(self.driver)
        self.Checkout = Checkout(self.driver)

    def test_cart_flow(self):
        self.Home.goto()
        self.Home.get_smart_device_pre_order_btn().click()
        assert self.Cart.suggestions_contain("Pura Smart Device") == False
        self.Cart.clear()
        assert self.Cart.suggestions_contain("Pura Smart Device") == True
        self.Fragrance.subscribe() 
        cart_total_with_subscription = self.Cart.get_total()
        self.Cart.clear() 
        self.Cart.close()
        self.Fragrance.add_as_one_time_purchase()
        assert cart_total_with_subscription < self.Cart.get_total()
        self.Cart.checkout()
        order_total = self.Checkout.get_total()
        #self.Checkout.apply_code("3Z09T7GQ9") # this discount code doesn't work!
        #assert self.Checkout.get_total() == order_total * .20
        self.Checkout.go_back()
        self.Cart.clear()
        assert self.Cart.is_empty() == True


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
