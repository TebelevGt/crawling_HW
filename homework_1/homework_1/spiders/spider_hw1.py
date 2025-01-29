from gc import callbacks
import scrapy
from ..items import PointItem, OrganizationItem


class SpiderHw1Spider(scrapy.Spider):
    name = "spider_hw1"
    allowed_domains = ["merchantpoint.ru"]
    start_urls = ["https://merchantpoint.ru/brands"]

    def parse(self, response):
        """Main scrapping function, collecting data about organizations"""

        # Getting all organization on page
        hrefs = response.xpath("//table//a/@href").getall()

        # Scrapping info about each org on page
        for href in hrefs:
            yield scrapy.Request(url=response.urljoin(href),callback = self.parse_org)

        # Getting next page and invoking parse function until pages end
        next_page_href = response.xpath("//a[text()='Вперед →']/@href").get()
        yield scrapy.Request(url=response.urljoin(next_page_href))

    def parse_org(self, response):
        """Collecting info about organization and it's merchant points"""

        # Org data
        org_name = response.xpath("//h1/text()").get()
        org_description = response.xpath("//div[@class='form-group mb-2']//p[2]/text()").get()
        source_url = response.url

        # Merchant points data in table
        rows = response.xpath("//table[@class='table table-striped']/tbody/tr")
        data = []
        
        # Parsing table
        for row in rows:
            mcc = row.xpath('./td[1]/text()').get()
            tsp = row.xpath('./td[2]/a/text()').get()
            address = row.xpath('./td[3]/text()').get().strip()
            point_item = PointItem(mcc=mcc, merchant_name=tsp, address=address)
            data.append(point_item)

        # Organizing data points
        organization_item = OrganizationItem(
            org_name=org_name,
            org_description=org_description,
            source_url=source_url,
            points=data
        )

        yield organization_item


    #C:\Users\tebel\OneDrive\Desktop\crowling\hw1\PythonApplication1\homework_1\homework_1
    # scrapy crawl spider_hw1 -L INFO -O res.jsonlines
