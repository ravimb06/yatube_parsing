import scrapy


class GroupSpider(scrapy.Spider):
    name = 'group'
    start_urls = ['http://51.250.32.185/']

    def parse(self, response):
        all_groups = response.css('[href^="/group/"]')
        for group_link in all_groups:
            yield response.follow(group_link, callback=self.parse_group)
        next_page = response.css('li.page-item a::attr(href)').getall()[-1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    

    def parse_group(self, response):
        yield {
            'group_name': response.css('div.card-body h2::text').get().strip(),
            'description': response.css('p.group_descr::text').get().strip(),
            'posts_count': int(response.css('li.list-group-item div::text').get().strip()[-1])
        }
