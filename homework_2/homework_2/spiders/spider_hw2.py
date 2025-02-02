import scrapy
from scrapy.spiders import SitemapSpider
import re
from ..items import BookItem

def parse_price(price_str):
    # Если строка равна 'null', возвращаем None
    if price_str == None:
        return None
    
    # Удаляем все символы, кроме цифр
    cleaned_str = ''.join(filter(str.isdigit, price_str))
    
    # Если строка пустая, возвращаем None
    if not cleaned_str:
        return None
    
    # Возвращаем число
    return cleaned_str

def strip_fun(string):
    if string != None:
        return string.strip()

def change_type(string, type):
    if string != None:
        return type(string)

class ProductsSpider(SitemapSpider):
    name = 'spider_hw2'
    allowed_domains = ['chitai-gorod.ru']
    sitemap_urls = ['https://www.chitai-gorod.ru/sitemap/products1.xml']

    def parse(self, response):
        # Извлекаем необходимые данные с каждой страницы товара
        title = response.xpath('//h1/text()').get()

        author = response.xpath('//a[@class="product-info-authors__author"]/text()').get() or \
            response.xpath('//a[@class="product-info-authors__author product-info-authors__author--unavailable"]/text()').get()

        description = response.xpath('//article[@class="detail-description__text"]/text()').get()

        raw_price = response.xpath('//text()[contains(., "₽")]').get()
        price_amount = parse_price(raw_price)

        rating_value = response.xpath('//span[@class="product-review-range__count"]/text()').get()

        rating_count_raw = response.xpath('//text()[contains(., "оценок")]').get()
        rating_count = parse_price(rating_count_raw)

        publication_year = response.xpath('//span[@itemprop="datePublished"]/text()').get()

        isbn = response.xpath('//span[@itemprop="isbn"]/text()').get()

        pages_cnt = response.xpath('//span[@itemprop="numberOfPages"]/text()').get()

        publisher = response.xpath('//a[@itemprop="publisher"]/text()').get()

        book_cover = response.xpath('//img[@class="product-info-gallery__poster"]/@src').get()
        if title != '' and publication_year != '' and isbn != None and isbn != '' and pages_cnt != '' and response.url != '':
            yield {
                'title': strip_fun(title),
                'author': strip_fun(author),
                'description': strip_fun(description),
                'price_amount': change_type(strip_fun(price_amount), int),
                'price_currency': '₽',
                'rating_value': change_type(strip_fun(rating_value), float),
                'rating_count': change_type(strip_fun(rating_count), int),
                'publication_year': change_type(strip_fun(publication_year), int),
                'isbn':strip_fun(isbn),
                'pages_cnt':change_type(strip_fun(pages_cnt), int),
                'publisher': strip_fun(publisher),
                'book_cover': strip_fun(book_cover),
                'source_url':  strip_fun(response.url),

            }



 

    #C:\Users\tebel\OneDrive\Desktop\crowling\hw2\PythonApplication2\homework_2\homework_2
    # scrapy crawl spider_hw2 -o spider_hw2.jsonlines
