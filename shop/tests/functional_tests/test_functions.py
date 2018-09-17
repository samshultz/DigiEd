import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import get_object_or_404
from mixer.backend.django import mixer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shop.models import Category
from ..test_data import create_book_instance


class TestBookCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        create_book_instance()
        category = mixer.blend(Category)
        
        create_book_instance(title="Django Testing",
                             price=0, category=category,
                             image="/books/2018/07/19/lrg.jpg")
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_contains_relevant_sections_and_items(self):
        # Sherlock comes to dlean.tk, he knows this is the right website
        # because he sees the name of the site in the browser title and
        # the logo
        self.browser.get(self.live_server_url)
        time.sleep(15)
        self.assertEqual(self.browser.title, "Digital Learning")
        logo = self.browser.find_element_by_css_selector(".logo-nav-left h1 a").text
        self.assertIn("DLearn", logo)
        # At the top of the page he sees three links one with
        # a title of dlearn.tk,
        email = self.browser.find_element_by_link_text("@dlearn.tk").text
        self.assertIn(email, self.browser.page_source)
        
        # the other with a title of login,
        header = self.browser.find_element_by_css_selector(".header-grid-left")
        login = header.find_element_by_link_text("Login").text
        self.assertIn(login, self.browser.page_source)
        # and the last with a title of Register
        register = header.find_element_by_link_text("Register").text
        self.assertIn(register, self.browser.page_source)
        # very close to the logo he sees a navigation with two items
        # Home and All books
        navbar = self.browser.find_element_by_css_selector("ul.navbar-nav")
        home = navbar.find_elements_by_tag_name("li")[0]
        book = navbar.find_elements_by_tag_name("li")[1]

        home_link = home.find_element_by_tag_name("a").text.title()
        book_link = book.find_element_by_tag_name("a").text.title()

        self.assertIn(home_link, self.browser.page_source)
        self.assertIn(book_link, self.browser.page_source)
        # very close to that he also sees a cart
        
        # He scrolls down and sees a section with the heading "New Collections"
        self.browser.execute_script("window.scrollTo(0, 1000);")
        new = self.browser.find_element_by_css_selector(".new-collections")
        heading = new.find_element_by_tag_name("h3").text
        self.assertIn(heading, self.browser.page_source)
        # after which there is a list of books with their titles and price
        book_lists = self.browser.find_elements_by_css_selector("div.new-collections-grid")
        self.assertGreater(len(book_lists), 2)
        book_list = book_lists[0]
        book = book_list.find_element_by_css_selector(".new-collections-grid1")
        self.assertIn(book.find_element_by_css_selector("h4 a").text.title(), self.browser.page_source)
        self.assertIn(book.find_element_by_css_selector("span.item_price").text, self.browser.page_source)
        # print(len(book))
        # when he scrolls down again he sees a form with a placeholder of
        # "Enter your email address"
        self.browser.execute_script("window.scrollTo(0, 1500);")
        newsletter = self.browser.find_element_by_id("id_email_field").get_attribute("value")
        self.assertEqual(newsletter, "Enter your email address")

        # there is also a button by the side of the form asking you to subscribe
        self.assertEqual(self.browser.find_element_by_id("id_submit").get_attribute("value"), "Subscribe")

    def test_that_user_can_see_list_of_books_and_prices(self):
        # John comes to dlearn.tk  and is taken to the homepage
        self.browser.get(self.live_server_url)
        # he sees a link with the text "All Books" and clicks it
        self.browser.find_element_by_link_text("ALL BOOKS").click()
        # he is then taken to a page with a list of books and their prices
        book_lists = self.browser.find_element_by_css_selector(".products-right-grids-bottom")
        book = book_lists.find_element_by_css_selector(".new-collections-grid1")
        self.assertIn(book.find_element_by_css_selector("h4 a").text.title(), self.browser.page_source)
        self.assertIn(book.find_element_by_css_selector("span.item_price").text, self.browser.page_source)
        # he see that some books are free and others are paid
        self.browser.execute_script("window.scrollTo(0, 1500);")
        time.sleep(5)
        books = book_lists.find_element_by_css_selector(".products-right-grids-bottom-grid")
        books = books.find_elements_by_css_selector(".new-collections-grid1")
        self.assertNotEqual(books[0].find_element_by_css_selector("span.item_price").text, "Free")
        self.assertEqual(books[1].find_element_by_css_selector("span.item_price").text, "Free")
        # he also notices that the free books have a download button beneath
        # them while the paid books have an add to cart button beneath them
        # he also sees a list of categories on the side of the page
        # on scrolling down the page he finds that there is a list of new books
        # on the side and also he sees a pagination widget
        # he clicks on the clicks on the image of of a book and is taken to
        # the details page of the book
        # He knows this because he can see the title of the book
        # on the page's title, he also sees the image and title of the book
        # on the page with price (free or paid) and download link or add to cart button
        # He also sees some stars on the page for rating the book
        # He scrolls to the bottom of the page and sees a tab widget which
        # contains information on the book
        # at the very bottom of the page he sees a list of similar books
        # also on this page he sees a list of categories at the side of the page


    #     self.assertGreater(
    #         len(self.browser.find_elements_by_class_name(
    #             "new-collections-grid1")), 0
    #     )

    #     self.browser.execute_script("window.scrollTo(0, 500);")
    #     time.sleep(5)
    #     self.assertGreater(
    #         len(self.browser.find_elements_by_css_selector(
    #             ".new-collections-grid1 .item_price")), 0
    #     )

    #     # he sees that some books are FREE and some have price tags on them

    #     self.assertEqual(self.browser.find_elements_by_css_selector(
    #         ".new-collections-grid1 .item_price")[1].text, '₦2,000.00')
    #     add_cart_btn = self.browser.find_elements_by_css_selector(
    #         ".new-collections-grid1 .simpleCart_shelfItem")

    #     # He observes that the free books have a DOWNLOAD button beneath them
    #     if add_cart_btn[1].find_element_by_class_name("item_price").text == "Free":
    #         self.assertEqual(add_cart_btn[0].find_element_by_class_name(
    #             "item_add").text, "DOWNLOAD")
    #     # and books on sale have an ADD TO CART button beneath them
    #     if add_cart_btn[1].find_element_by_class_name("item_price").text == "\u20a62,000.00":
    #         self.assertEqual(add_cart_btn[1].find_element_by_class_name(
    #             "item_add").text, "ADD TO CART")

    # def test_that_categories_are_listed_on_the_list_page(self):
    #     pass
    #     # when john came to the product items page he saw a list of categories
    #     # that books belonged to, to help him filter through all the books
    #     # in the site.
    #     self.browser.get(self.live_server_url + '/shop/')
    #     self.assertIn('<ul class="cate">', self.browser.page_source)

    #     # He saw a category called "Web design"
    #     self.browser.execute_script("window.scrollTo(0, 500);")
    #     categories = self.browser.find_element_by_css_selector(".categories .cate")
    #     try:
    #         categories.find_element_by_link_text("Web design")
    #     except NoSuchElementException as e:
    #         self.fail(e)
    #     # and clicked on it and the list of books
    #     categories.find_element_by_link_text("Web design").click()
    #     self.browser.execute_script("window.scrollTo(0, 500);")
    #     time.sleep(5)
    #     # on the page was filtered to show only those books related to "Web design"
    #     category = get_object_or_404(Category, slug="web-development")
    #     book = Book.objects.filter(category=category).first()

    #     self.assertNotIn(book.name, self.browser.page_source)
    #     # self.assertIn('WEB DESIGN', self.browser.page_source)

    # def test_detail_page(self):
    #     # When John was in the book list page, he saw a book that
    #     # caught his attention and wanted to know more about the book
    #     # so he clicked on the book's image and was taken to the book's
    #     # detail page
    #     self.browser.get(self.live_server_url + '/shop/')
    #     self.browser.execute_script("window.scrollTo(0, 700);")
    #     time.sleep(3)
    #     self.browser.find_element_by_css_selector(
    #         ".new-collections-grid1 .product-image").click()

    #     # He knows this because he can see the books title and author
    #     # on the browser's title, and the image of the book is also
    #     # largely displayed on the page
    #     self.assertIn("Django Testing", self.browser.title)
    #     self.browser.execute_script("window.scrollTo(0, 700);")
    #     time.sleep(3)
    #     self.assertIn('<div class="flexslider">', self.browser.page_source)

    #     # while on the detail page, he also sees the book's name,
    #     # Author, and a short description of the book after he clicked
    #     # on the information
    #     self.assertEqual(self.browser.find_element_by_css_selector(
    #         ".detail h3").text, "Django Testing")
    #     self.assertIn('<div class="description">', self.browser.page_source)

    #     # he saw the price of the book and an
    #     # add to cart button on the page as well
    #     self.assertEqual(self.browser.find_element_by_css_selector(
    #         ".detail .item_price").text, "Free")
    #     self.assertEqual(self.browser.find_element_by_css_selector(
    #         ".detail .item_add").text, "ADD TO CART")
    #     # when he scrolled to the bottom of the page, he saw a list of similar
    #     # books with a title of "SIMILAR BOOKS"

    #     # the list of categories he saw before on the product list page
    #     # was also here

