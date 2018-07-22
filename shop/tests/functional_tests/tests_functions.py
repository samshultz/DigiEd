import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import get_object_or_404

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shop.models import Category, Book
from ..test_data import create_book_instance


class BookTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        create_book_instance()
        category = Category.objects.create(
            name="Web development",
            slug="web-development"
        )
        create_book_instance(title="Django Testing",
                             price=0, category=category,
                             image="/books/2018/07/19/lrg.jpg")
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
            ".new-collections-grid1 .item_price")[1].text, '₦2,000.00')
        add_cart_btn = self.browser.find_elements_by_css_selector(
            ".new-collections-grid1 .simpleCart_shelfItem")

        # He observes that the free books have a DOWNLOAD button beneath them
        if add_cart_btn[1].find_element_by_class_name("item_price").text == "Free":
            self.assertEqual(add_cart_btn[0].find_element_by_class_name(
                "item_add").text, "DOWNLOAD")
        # and books on sale have an ADD TO CART button beneath them
        if add_cart_btn[1].find_element_by_class_name("item_price").text == "\u20a62,000.00":
            self.assertEqual(add_cart_btn[1].find_element_by_class_name(
                "item_add").text, "ADD TO CART")

    def test_that_categories_are_listed_on_the_list_page(self):
        pass
        # when john came to the product items page he saw a list of categories
        # that books belonged to, to help him filter through all the books
        # in the site.
        self.browser.get(self.live_server_url + '/shop/')
        self.assertIn('<ul class="cate">', self.browser.page_source)

        # He saw a category called "Web design"
        self.browser.execute_script("window.scrollTo(0, 500);")
        categories = self.browser.find_element_by_css_selector(".categories .cate")
        try:
            categories.find_element_by_link_text("Web design")
        except NoSuchElementException as e:
            self.fail(e)
        # and clicked on it and the list of books
        categories.find_element_by_link_text("Web design").click()
        self.browser.execute_script("window.scrollTo(0, 500);")
        time.sleep(5)
        # on the page was filtered to show only those books related to "Web design"
        category = get_object_or_404(Category, slug="web-development")
        book = Book.objects.filter(category=category).first()

        self.assertNotIn(book.name, self.browser.page_source)
        # self.assertIn('WEB DESIGN', self.browser.page_source)

    def test_detail_page(self):
        # When John was in the book list page, he saw a book that
        # caught his attention and wanted to know more about the book
        # so he clicked on the book's image and was taken to the book's
        # detail page
        self.browser.get(self.live_server_url + '/shop/')
        self.browser.execute_script("window.scrollTo(0, 700);")
        time.sleep(3)
        self.browser.find_element_by_css_selector(
            ".new-collections-grid1 .product-image").click()

        # He knows this because he can see the books title and author
        # on the browser's title, and the image of the book is also
        # largely displayed on the page
        self.assertIn("Django Testing", self.browser.title)
        self.browser.execute_script("window.scrollTo(0, 700);")
        time.sleep(3)
        self.assertIn('<div class="flexslider">', self.browser.page_source)

        # while on the detail page, he also sees the book's name,
        # Author, and a short description of the book after he clicked
        # on the information
        self.assertEqual(self.browser.find_element_by_css_selector(
            ".detail h3").text, "Django Testing")
        self.assertIn('<div class="description">', self.browser.page_source)

        # he saw the price of the book and an
        # add to cart button on the page as well
        self.assertEqual(self.browser.find_element_by_css_selector(
            ".detail .item_price").text, "Free")
        self.assertEqual(self.browser.find_element_by_css_selector(
            ".detail .item_add").text, "ADD TO CART")
        # when he scrolled to the bottom of the page, he saw a list of similar
        # books with a title of "SIMILAR BOOKS"

        # the list of categories he saw before on the product list page
        # was also here

