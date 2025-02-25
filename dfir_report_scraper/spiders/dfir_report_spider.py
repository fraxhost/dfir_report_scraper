import scrapy
from dfir_report_scraper.items import DfirReportItem


class DfirReportSpiderSpider(scrapy.Spider):
    name = "dfir_report_spider"
    allowed_domains = ["thedfirreport.com"]
    start_urls = ["https://thedfirreport.com"]

    def parse(self, response):

        report_urls = response.css("h2.entry-title a::attr(href)").getall()

        for report_url in report_urls:
            yield response.follow(report_url, callback=self.parse_report_page)

        next_page = response.css("div.nav-links a.next.page-numbers::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_report_page(self, response):
        report_item = DfirReportItem()

        report_item["title"] = response.css(".entry-title::text").get()
        report_item["url"] = response.css(".posted-on a::attr(href)").get()
        report_item["publish_date"] = response.css(
            ".entry-date.published::attr(datetime)"
        ).get()
        report_item["description"] = response.css(
            "article p::text, article p a::text"
        ).getall()

        yield report_item
