from django.apps import AppConfig
import elasticsearch_dsl.connections


class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        elasticsearch_dsl.connections.connections.create_connection(hosts=['https://ef45e787737c2385b89f93820c9bfea6.us-east-1.aws.found.io'], http_auth="elastic:veOFdNEXM0ugmxJsgauaKrH1", timeout=20)
        import shop.signals
