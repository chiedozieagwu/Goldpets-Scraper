import scrapy
from scrapy.loader import ItemLoader
from collections import OrderedDict

class GoldpetsItem(scrapy.Item):
    Title =  scrapy.Field()
    Descrição = scrapy.Field()
    Price =  scrapy.Field()
    Marca = scrapy.Field()
    Quantidade = scrapy.Field()
    Idade = scrapy.Field()
    Porte = scrapy.Field()
    Características = scrapy.Field()
    Gama = scrapy.Field()
    Alimento = scrapy.Field()
    ean13 = scrapy.Field()
    category = scrapy.Field()
    sub_category1 = scrapy.Field()
    sub_category2 = scrapy.Field()
    sub_category3 = scrapy.Field()    
    sub_category4 = scrapy.Field()
    product_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    Photo_0 = scrapy.Field()
    Photo_1 = scrapy.Field()
    Photo_2 = scrapy.Field()
    Photo_3 = scrapy.Field()
    Photo_Path_0 = scrapy.Field()
    Photo_Path_1 = scrapy.Field()
    Photo_Path_2 = scrapy.Field()
    Photo_Path_3 = scrapy.Field()
    
