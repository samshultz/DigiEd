from elasticsearch_dsl import DocType, Mapping
from elasticsearch_dsl import Long
from elasticsearch_dsl import Text


class ESBook(DocType):

    title = Text(required=True)
    author = Text(required=True)
    image = Text(required=True)
    price = Long(required=True)
    url = Text(required=True)
    download_link = Text()
    publisher = Text()

    
    class Meta:
        mapping = Mapping("books")

    class Index:
        doc_type = 'books'
