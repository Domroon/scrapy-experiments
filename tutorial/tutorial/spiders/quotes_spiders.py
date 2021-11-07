import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


class QuotesSpider2(scrapy.Spider):
    name = "quotes2"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('.quote'):
            yield {
                'text' : quote.css('span.text::text').get(),
                'author' : quote.css('.author::text').get(),
                'tags' : quote.css('.tags .tag::text').getall(),
            }


class QuotesSpider3(scrapy.Spider):
    name = "quotes3"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('.quote'):
            yield {
                'text' : quote.css('.text::text').get(),
                'author' : quote.css('.author::text').get(),
                'tags' : quote.css('.tags .tag::text').getall(),
            }

        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class QuotesSpider4(scrapy.Spider):
    name = "quotes4"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('.quote'):
            yield {
                'text' : quote.css('.text::text').get(),
                'author' : quote.css('.author::text').get(),
                'tags' : quote.css('.tags .tag::text').getall(),
            }

        for a in response.css('.next a'):
            yield response.follow(a, callback=self.parse)


class QuotesSpider5(scrapy.Spider):
    name = "quotes5"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)