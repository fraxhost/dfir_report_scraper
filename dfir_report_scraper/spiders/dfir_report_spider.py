import scrapy


class DfirReportSpiderSpider(scrapy.Spider):
    name = "dfir_report_spider"
    allowed_domains = ["thedfirreport.com"]
    start_urls = ["https://thedfirreport.com"]

    def parse(self, response):
        
        yield response
        
