from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):
    
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.base_domain = parse.urlparse(base_url).netloc
        self.links = set()
        self.social_media_links = set()
        self.social_media_domains = {
            'facebook.com', 'twitter.com', 'instagram.com',
            'linkedin.com', 'youtube.com', 'pinterest.com',
            'tiktok.com', 'reddit.com', 'snapchat.com'
        }

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    if self._is_same_domain(url):
                        self.links.add(url)
                    elif self._is_social_media(url):
                        self.social_media_links.add(url)

    def _is_same_domain(self, url):
        domain = parse.urlparse(url).netloc
        return domain == self.base_domain

    def _is_social_media(self, url):
        domain = parse.urlparse(url).netloc
        return any(social_domain in domain for social_domain in self.social_media_domains)

    def page_links(self):
        return self.links

    def social_media(self):
        return self.social_media_links

    def error(self, message):
        pass
