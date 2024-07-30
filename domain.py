from urllib.parse import urlparse

# Get domain name (e.g., example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except IndexError:
        return ''

# Get sub-domain name (e.g., name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return ''
