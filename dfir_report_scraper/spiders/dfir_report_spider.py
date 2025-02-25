import scrapy


class DfirReportSpiderSpider(scrapy.Spider):
    name = "dfir_report_spider"
    allowed_domains = ["thedfirreport.com"]
    start_urls = ["https://thedfirreport.com"]

    def parse(self, response):

        titles = response.css("h2.entry-title a::text").getall()

        for title in titles:
            yield {"title": title}

        next_page = response.css("div.nav-links a.next.page-numbers::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
