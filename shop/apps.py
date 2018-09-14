from django.apps import AppConfig
import elasticsearch_dsl.connections


class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        elasticsearch_dsl.connections.connections.create_connection(timeout=20)
        import shop.signals
