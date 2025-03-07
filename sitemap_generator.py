import os


class SitemapGenerator:
    def __init__(self, url, output_dir):
        self.base_url = url
        self.output_dir = output_dir
        self.urls = [url]
        self.visited_urls = set()


    def add_url(self, url):
        self.urls.append(url)

    def generate_sitemap(self):
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in self.urls:
            sitemap += f'  <url>\n    <loc>{url}</loc>\n  </url>\n'
        sitemap += '</urlset>'
        return sitemap

    def save_sitemap(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate_sitemap())

    def crawl_website(self, max_pages=100):
        """Crawl website starting from base URL"""
        from bs4 import BeautifulSoup 
        import requests 
        
        queue = [self.base_url]
        while queue and len(self.visited_urls) < max_pages:
            url = queue.pop(0)
            if url in self.visited_urls:
                continue
                
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                self.add_url(url)
                self.visited_urls.add(url)
                
                for link in soup.find_all('a', href=True):
                    absolute_url = requests.compat.urljoin(url, link['href'])
                    if absolute_url.startswith(self.base_url) and absolute_url not in self.visited_urls:
                        queue.append(absolute_url)
            except Exception as e:
                print(f"Error crawling {url}: {str(e)}")

    def generate_xml_sitemap(self):
        """Generate XML file and return its path"""
        filename = os.path.join(self.output_dir, 'sitemap.xml')
        self.save_sitemap(filename)
        return filename
