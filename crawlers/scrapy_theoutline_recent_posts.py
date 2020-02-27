import scrapy
import json
import csv
from scrapy.selector import Selector

class OutlineRecentSpider(scrapy.Spider):
    name = "recent"

    def __init__(self):
        self.filename = 'recent-outline.csv'
        self.unsorted_page_posts = []
        self.logged_out = False

    def start_requests(self):
        base_url = 'https://theoutline.com/api/topic/recent?page='
        # opening the file with w+ mode truncates the file
        f = open(self.filename, "w+")
        f.close()
        
        for page_num in range(20):
            parse_url = base_url + str(page_num)
            yield scrapy.Request(url=parse_url, callback=self.parse, meta={'page_num': page_num})

    def make_post_dict(self, raw_post):
        title = Selector(text=raw_post).css('.workhorse__title::text').get()
        date = Selector(text=raw_post).css('.workhorse__date::text').get()
        return {"title": title, "date": date}

    def parse(self, response):
        # titles = response.css('.workhorse__title::text').getall()
        json_response = json.loads(response.body_as_unicode())
        page_num = response.meta['page_num']
        html_response = json_response['html']
        all_posts_raw = Selector(text=html_response).css('.workhorse__post').getall()
        all_posts_list_of_dict = map(self.make_post_dict, all_posts_raw)
        page_dict = {
            "page_num": page_num,
            "posts": all_posts_list_of_dict
        }
        self.unsorted_page_posts.append(page_dict)

    def closed(self, reason):
        self.log('closed')
        sorted_page_posts_dict = sorted(self.unsorted_page_posts, key=lambda k: k['page_num'])
        # sorted_page_posts = map(lambda x: x['titles'], sorted_page_posts_dict)
        
        with open(self.filename, 'a') as f:
            writer = csv.writer(f)
            for page in sorted_page_posts_dict:
                for post in page['posts']:
                    writer.writerow([post['date'], post['title']])
                
            

