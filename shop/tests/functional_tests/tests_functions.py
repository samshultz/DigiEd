import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shop.models import Category
from ..test_data import create_book_instance


class BookTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        create_book_instance()
        category = Category.objects.create(
            name="Web design",
            slug="web-design2"
        )
        create_book_instance(title="Django Testing",
                             price=0, category=category)
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_that_user_can_see_list_of_books_and_prices(self):
        # John comes to DIGIED.COM  and sees a list of books and their prices
        self.browser.get(self.live_server_url + '/shop/')

        self.assertGreater(
            len(self.browser.find_elements_by_class_name(
                "new-collections-grid1")), 0
        )

        self.browser.execute_script("window.scrollTo(0, 500);")
        time.sleep(5)
        self.assertGreater(
            len(self.browser.find_elements_by_css_selector(
                ".new-collections-grid1 .item_price")), 0
        )

        # he sees that some books are FREE and some have price tags on them

        self.assertEqual(self.browser.find_elements_by_css_selector(
            ".new-collections-grid1 .item_price")[0].text, '₦2,000.00')
        add_cart_btn = self.browser.find_elements_by_css_selector(
            ".new-collections-grid1 .simpleCart_shelfItem")

        # He observes that the free books have a DOWNLOAD button beneath them
        if add_cart_btn[1].find_element_by_class_name("item_price").text == "Free":
            self.assertEqual(add_cart_btn[1].find_element_by_class_name(
                "item_add").text, "DOWNLOAD")
        # and books on sale have an ADD TO CART button beneath them
        if add_cart_btn[0].find_element_by_class_name("item_price").text == "\u20a62,000.00":
            self.assertEqual(add_cart_btn[0].find_element_by_class_name(
                "item_add").text, "ADD TO CART")

    def test_that_categories_are_listed_on_the_list_page(self):
        pass
        # when john came to the product items page he saw a list of categories
        # that books belonged to, to help him filter through all the books
        # in the site.
        self.browser.get(self.live_server_url + '/shop/')
        self.assertIn('<ul class="cate">', self.browser.page_source)
        
        # He clicked on a category called "Web design" and the list of books
        categories = self.browser.find_element_by_css_selector(".categories .cate")
        try:
            categories.find_element_by_link_text("Web design")
        except NoSuchElementException as e:
            self.fail(e)
        
        # on the page was filtered to show only those books related to
        # "Web design"
        
        self.fail("Incomplete test")
