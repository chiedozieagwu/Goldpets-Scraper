from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from slugify import slugify

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        Marca = item['Marca']
        for i in range(10):
            filename = item['Title'] + f'_{i + 1}'
            return f'{Marca}/{filename}.jpg'