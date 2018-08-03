from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class DiscountSection(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="discount/section")
    percent_discount = models.IntegerField("Discount (%)",
                                           validators=[
                                               MinValueValidator(
                                                   0, "Discount must not be less than 0 percent"),
                                               MaxValueValidator(100, "Discount must not exceed 100 percent")])

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.clean()
        # Call the real save() method
        super(DiscountSection, self).save(*args, **kwargs)

    def clean(self):
        if self.percent_discount < 0 or self.percent_discount > 100:
            raise ValidationError("discount must be between 0 and 100% inclusive")
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be less than end date")
            
    class Meta:
        ordering = '-end_date',
