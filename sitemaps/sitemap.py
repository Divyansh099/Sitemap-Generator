import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import xml.dom.minidom
from datetime import datetime

class SitemapGenerator:
    def __init__(self, base_url, output_dir="sitemaps"):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def is_valid_url(self, url):
        """Check if URL belongs to the same domain and hasn't been visited yet."""
        parsed_url = urlparse(url)
        return (parsed_url.netloc == self.base_domain or not parsed_url.netloc) and url not in self.visited_urls

    def extract_links(self, url):
        """Extract all links from a webpage."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                absolute_url = urljoin(url, href)
                
                # Filter out anchors, mailto, javascript, etc.
                if absolute_url.startswith('http') and self.is_valid_url(absolute_url):
                    links.append(absolute_url)
            
            return links
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return []

    def crawl_website(self, max_pages=100):
        """Crawl the website starting from base_url up to max_pages."""
        urls_to_visit = [self.base_url]
        page_count = 0
        
        while urls_to_visit and page_count < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
                
            print(f"Crawling: {current_url}")
            self.visited_urls.add(current_url)
            page_count += 1
            
            # Extract links from the current page
            new_links = self.extract_links(current_url)
            
            # Add new links to the queue
            for link in new_links:
                if link not in self.visited_urls and link not in urls_to_visit:
                    urls_to_visit.append(link)
        
        print(f"Crawling complete. Visited {len(self.visited_urls)} pages.")
        return self.visited_urls

    def generate_xml_sitemap(self, filename="sitemap.xml"):
        """Generate an XML sitemap from the visited URLs."""
        if not self.visited_urls:
            print("No URLs to include in sitemap. Run crawl_website() first.")
            return
        
        # Create XML document
        doc = xml.dom.minidom.getDOMImplementation().createDocument(
            None, "urlset", None
        )
        root = doc.documentElement
        root.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        # Add description at the beginning of the XML file
        description = doc.createComment("This is an XML sitemap for the website.")
        doc.insertBefore(description, root)
        
        # Current date in W3C format
        today = datetime.today().strftime('%Y-%m-%d')
        
        # Add URLs to sitemap
        for url in sorted(self.visited_urls):
            url_element = doc.createElement("url")
            
            # Add location
            loc = doc.createElement("loc")
            loc_text = doc.createTextNode(url)
            loc.appendChild(loc_text)
            url_element.appendChild(loc)
            
            # Add last modified date (using today)
            lastmod = doc.createElement("lastmod")
            lastmod_text = doc.createTextNode(today)
            lastmod.appendChild(lastmod_text)
            url_element.appendChild(lastmod)
            
            # Add priority (default to 0.5)
            priority = doc.createElement("priority")
            priority_text = doc.createTextNode("0.5")
            priority.appendChild(priority_text)
            url_element.appendChild(priority)
            
            # Add to root element
            root.appendChild(url_element)
        
        # Write to file
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))
        
        print(f"Sitemap created at {filepath}")
        return filepath

# MODIFY THIS SECTION WITH YOUR WEBSITE URL
def main():
    # Hard-coded URL - REPLACE THIS WITH YOUR WEBSITE URL
    url = "https://3mmaven.com/"  # <-- REPLACE WITH YOUR WEBSITE URL HERE
    
    # Settings
    output_dir = "sitemaps"  # Directory where sitemap will be saved
    max_pages = 100         # Maximum number of pages to crawl
    
    # Run the sitemap generator
    generator = SitemapGenerator(url, output_dir)
    generator.crawl_website(max_pages=max_pages)
    generator.generate_xml_sitemap()

if __name__ == "__main__":
    main()