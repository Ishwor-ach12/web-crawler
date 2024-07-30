import threading
from urllib.request import urlopen
from link_finder import LinkFinder
from domain import get_domain_name
from general import create_project_dir, create_data_files, file_to_set, set_to_file

class Spider(threading.Thread):

    # Class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    num_threads = 10

    def __init__(self, project_name, base_url, domain_name, num_threads=4):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.num_threads = num_threads
        self.boot()
        print(f"Initialized spider with project_name={project_name}, base_url={base_url}, domain_name={domain_name}")
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        print(f"Booted with {len(Spider.queue)} URLs in queue and {len(Spider.crawled)} URLs crawled.")

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(f'Queue {len(Spider.queue)} | Crawled {len(Spider.crawled)}')
            links = Spider.gather_links(page_url)
            Spider.add_links_to_queue(links)
            try:
                Spider.queue.remove(page_url)
            except KeyError:
                print(f'Error: {page_url} not found in queue.')
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
            return finder.page_links()
        except Exception as e:
            print(f'Error in gather_links: {e}')
            return set()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue or url in Spider.crawled or Spider.domain_name not in url:
                continue
            Spider.queue.add(url)
        
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def worker(thread_name):
        while True:
            if not Spider.queue:
                break
            page_url = Spider.queue.pop()
            Spider.crawl_page(thread_name, page_url)

    def threaded_crawl(self):
        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.worker, args=(f'Thread-{i+1}',))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        print("All threads have finished.")
