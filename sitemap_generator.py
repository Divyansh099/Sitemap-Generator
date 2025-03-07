class SitemapGenerator:
    def __init__(self, url, output_dir):

        self.urls = []
        self.url = url
        self.output_dir = output_dir


    def add_url(self, url):
        self.urls.append(url)

    def generate_sitemap(self):
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap-image.v1">\n'
        for url in self.urls:
            sitemap += f'  <url>\n    <loc>{url}</loc>\n  </url>\n'
        sitemap += '</urlset>'
        return sitemap

    def save_sitemap(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate_sitemap())
