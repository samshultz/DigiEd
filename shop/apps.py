from django.apps import AppConfig
import elasticsearch_dsl.connections
from django.conf import settings

class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        elasticsearch_dsl.connections.connections.create_connection(hosts=[settings.FOUNDELASTICSEARCH_URL], 
                                                                    http_auth=settings.HTTP_AUTH, 
                                                                    timeout=20)
        # elasticsearch_dsl.connections.connections.create_connection(timeout=20)
        import shop.signals
