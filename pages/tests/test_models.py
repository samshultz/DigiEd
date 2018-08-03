import datetime

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from mixer.backend.django import mixer
from pages.models import DiscountSection

pytestmark = pytest.mark.django_db


class TestDiscountSectionModel(TestCase):
    def setUp(self):
        self.future_date = timezone.now() + datetime.timedelta(days=3)
        self.now = timezone.now()
        self.image = SimpleUploadedFile(name='test_image.jpg', content=open(
            r"C:\Users\Samshultz\Pictures\never-regret.jpg", 'rb').read(), content_type='image/jpeg')

    def test_str_representation(self):

        disc = mixer.blend("pages.DiscountSection",
                           image=self.image, percent_discount=45, 
                           start_date=self.now, end_date=self.future_date)
        self.assertEqual(str(disc), disc.title)

    def test_title_length(self):
        disc = mixer.blend("pages.DiscountSection",
                           image=self.image, percent_discount=45, 
                           start_date=self.now, end_date=self.future_date)
        self.assertLessEqual(len(disc.title), 100,
                             msg="Title should be 100 <= 100")

    def test_min_value_for_disc(self):
        try:
            disc = mixer.blend("pages.DiscountSection",
                           image=self.image, percent_discount=-45, 
                           start_date=self.now, end_date=self.future_date)

            self.fail("Discount can't be negative")
        except ValidationError:
            pass

    def test_max_value_for_disc(self):
        try:
            disc = mixer.blend("pages.DiscountSection",
                           image=self.image, percent_discount=450, 
                           start_date=self.now, end_date=self.future_date)

            self.fail("Discount can't greater than 100%")
        except ValidationError:
            pass

    def test_start_date_less_than_end_date(self):
        future_date = timezone.now() + datetime.timedelta(days=3)
        now = timezone.now()

        try:
            disc = mixer.blend("pages.DiscountSection",
                               image=self.image, percent_discount=12,
                               start_date=future_date, end_date=now)

            self.fail("start date can't be greater than end date")
        except ValidationError:
            pass
