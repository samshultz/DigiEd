from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book
from shop.es_docs import ESBook

@receiver(post_save, sender=Book)
def index_data(sender, instance, created, **kwargs):
    
    if instance.image:
            image = instance.image.url
    else:
        image = instance.image_url
    
    if instance.book_file:
        download_link = instance.book_file.url
    else:
        download_link = instance.book_url

    esp = ESBook(meta={'id': instance.pk},
                 title=instance.name,
                 image=image,
                 url=instance.get_absolute_url(),
                 price=instance.price,
                 publisher=instance.publisher,
                 author=instance.author,
                 download_link=download_link

                )
        
    esp.save(index='books')

@receiver(post_delete, sender=Book)
def remove_book_from_index(sender, instance, **kwargs):
    ESBook().get(id=instance.pk, index='books').delete()
