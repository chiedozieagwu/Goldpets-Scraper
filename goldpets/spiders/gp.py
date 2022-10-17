from statistics import quantiles
import scrapy
import os
import json
from scrapy.loader import itemloaders
from goldpets.items import GoldpetsItem

class GpSpider(scrapy.Spider):
    name = 'gp'
    start_urls = []
    urls = ['https://goldpet.pt/3-cao','https://goldpet.pt/4-gato','https://goldpet.pt/7-roedor','https://goldpet.pt/6-ave','https://goldpet.pt/5-peixe','https://goldpet.pt/281-reptil']
    for url in urls:
        start_urls.append(url)

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'

    def parse(self, response):
        products = response.css('h2.h3.product-title>a::attr(href)').extract()
        for product in products:
            product_link = product
            yield scrapy.Request(product_link, callback=self.parse_products)

        next_page = response.css('a.next.js-search-link::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_products(self, response):
        item = GoldpetsItem()
        item['Title'] =  response.css('h1.h1.product-title::text').get()
        item['Descrição'] = response.css('div.product-description>p::text').extract()
        item['Marca'] = response.css('img.img.img-thumbnail.manufacturer-logo::attr(alt)').get()
        if item['Marca'] is None:
            item['Marca'] = 'No brand'
        item['Idade'] = response.xpath('//dt[text()="Idade"]/following-sibling::dd/text()').get()
        item['Porte'] = response.xpath('//dt[text()="Porte"]/following-sibling::dd/text()').get()
        item['Características'] = response.xpath('//dt[text()="Características"]/following-sibling::dd/text()').get()
        item['Gama'] = response.xpath('//dt[text()="Gama"]/following-sibling::dd/text()').get()
        item['Alimento'] = response.xpath('//dt[text()="Alimento"]/following-sibling::dd/text()').get()
        item['product_url'] = response.url 
        item['Quantidade'] = ''
        item['image_urls'] = ''
        item['Price'] = ''
        item['images'] = ''
        item['ean13'] = ''

        breadcrumbs = list(filter(None, map(str.strip, response.css('li[itemprop=itemListElement]>a>span::text').extract())))
        try:
            item['category'] = breadcrumbs[0]
        except:
            item['category'] = ''
        
        try:
            item['sub_category1'] = breadcrumbs[1]
        except:
            item['sub_category1'] = ''
        
        try:
            item['sub_category2'] = breadcrumbs[2]
        except:
            item['sub_category2'] = ''

        try:
            item['sub_category3'] = breadcrumbs[3]
        except:
            item['sub_category3'] = ''

        try:
            item['sub_category4'] = breadcrumbs[4]
        except:
            item['sub_category4'] = ''

        product_img = response.css('img.js-qv-product-cover::attr(src)').getall()
        img_urls = product_img[0]
        ext = img_urls.split('?')[0].rsplit('.', 1)[-1]
        filename = item['Title'] + '_1.' + ext

        item['Photo_0'] = filename
        item['Photo_Path_0'] = os.path.join('product images', 'images', item['Marca'], filename)

        for i in range(3):
            item[f'Photo_{i + 1}'] = ''
            item[f'Photo_Path_{i + 1}'] = ''

        for i, image in enumerate(product_img[1:]):
            ext = image.split('?')[0].rsplit('.', 1)[-1]
            filename = item['Title'] + f'_{i + 1}.{ext}'
            

            item[f'Photo_{i + 1}'] = filename
            item[f'Photo_Path_{i + 1}'] = os.path.join('product images', 'images', item['Marca'], filename)

        token = response.css('div.product-actions form#add-to-cart-or-refresh input::attr(value)').get()
        product_id = response.css('input#product_page_product_id::attr(value)').get()
        customization_id = response.css('input#product_customization_id::attr(value)').get()
        groups = response.css('li.input-container.float-xs-left label input.input-radio::attr(value)').getall()
        for group in groups:
            ajax_url = f'https://goldpet.pt/index.php?controller=product&token={token}&id_product={product_id}&id_customization={customization_id}&group%5B8%5D={group}&qty=1'
            payload = {"controller" : item['Title']
                ,"token" : token
                ,"id_product" : product_id
                ,"id_customization" : customization_id
                ,"group%5B8%5D" : group
                ,"qty" : '1'
                }
            yield scrapy.FormRequest(ajax_url,callback=self.parse_variants, method="POST", body=json.dumps(payload), meta={'item': item})

    def parse_variants(self,response):
        item = response.meta.get('item', {})
        var_item = item.copy()
        var_item['Price'] = response.css('div.product-prices span::text').get().replace('\xa0€','')
        var_item['image_urls'] =  response.css('img.js-qv-product-cover::attr(src)').extract()
        var_item['ean13'] = response.xpath('//dt[text()="ean13"]/following-sibling::dd/text()').get()
        other,quantity = response.css('meta[itemprop=url]::attr(content)').get().rsplit('-',1)
        var_item['Quantidade'] = quantity
        yield var_item