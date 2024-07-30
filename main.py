# from domain import get_domain_name
# from spider import Spider

# PROJECT_NAME = 'my_project'
# HOMEPAGE = 'https://www.bbc.com'
# DOMAIN_NAME = get_domain_name(HOMEPAGE)

# Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, num_threads=4)

from spider import Spider

if __name__ == '__main__':
    PROJECT_NAME = input("Enter project name: ")
    HOMEPAGE = input("Enter homepage url you want to crawl (example: https://www.w3schools.com/)\n")  # Use a website with many links to test
    DOMAIN_NAME = input("Enter domain name example(w3schools.com)\n")
    spider = Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, num_threads=10)
    print("Starting crawl...")
    spider.threaded_crawl()
    print("Crawling finished.")

