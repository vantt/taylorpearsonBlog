import sys
import os
import re
import zlib
import binascii
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from sitegraph.items import SiteGraphItem


class GraphspiderSpider(CrawlSpider):
    name = "graphspider"

    allowed_domains = ["taylorpearson.me"]
    start_urls = ["https://taylorpearson.me/definition/"]
    keep_urls = [
        r"^https:\/\/taylorpearson\.me\/[^\/]+\/$",
    ]

    ignore_urls = [
        r"^https:\/\/taylorpearson\.me\/eojbook",
        r"^https:\/\/taylorpearson\.me\/archive",
        r"^https:\/\/taylorpearson\.me\/contact",
        r"^https:\/\/taylorpearson\.me\/services/",
        r"^https:\/\/taylorpearson\.me\/coaching-consulting",
        r"^https:\/\/taylorpearson\.me\/cmo/",
        r"^https:\/\/taylorpearson\.me\/speaking-events/",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"/",),
                deny=(
                    r"/eojbook",
                    r"/archive",
                    r"/contact",
                    r"/services",
                    r"/coaching-consulting",
                    r"/speaking-events",
                    r"/cmo",
                ),
                deny_extensions=(
                    'jpg', 'jpeg', 'png', 'gif'
                )
            ),
            callback="parse_item", follow=True
        ),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        page_url = response.url.strip()

        if self.is_keep_url(page_url):
            item = SiteGraphItem()
            item["url"] = page_url
            item["id"] = zlib.crc32(bytes(page_url, 'utf-8')) & 0xffffffff
            item["title"] = hxs.xpath("//header/h1/text()").extract()[0].strip()
            links = {}

            for anchor in hxs.xpath("//a[@href]"):
                href = anchor.xpath("@href").extract()[0].strip()
                if not href.lower().startswith("javascript"):
                    if self.is_keep_url(href):
                        link_url = urljoin(page_url, href)
                        link_id = zlib.crc32(bytes(link_url, 'utf-8')) & 0xffffffff
                        links[link_id] = link_url
                        print('keep', href)

            item["links"] = links

            return item

    def is_keep_url(self, url):
        return any(re.search(regex, url) for regex in self.keep_urls)
        #
        # if is_keep:
        #     return True
        #
        # return not any(re.search(regex, url) for regex in self.ignore_urls)

