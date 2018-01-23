import scrapy
import os

class ChemistrySpider(scrapy.Spider):
    name = "chemistry"

    def start_requests(self):
        urls = [
            'http://as.nyu.edu/chemistry/people/faculty.html',
            'http://as.nyu.edu/chemistry/people/clinical-faculty.html',
            'http://as.nyu.edu/chemistry/people/research-scientists.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        faculty_links = response.xpath("//a[text()='View Profile']/@href").extract()
        for link in faculty_links:
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse_people)

    def parse_people(self, response):
        full_name = response.xpath("//div[contains(@class, 'faculty__header')]/h1/text()").extract_first()

        filename = "../nyu/{}/{}".format(
            self.name,
            full_name.replace(' ', '')
        )
        
        with open(filename, 'w') as f:
            text = ''.join(response.xpath('//div[contains(@class, "bio") and contains(@class, "global")]//text()').extract())
            f.write(text)
