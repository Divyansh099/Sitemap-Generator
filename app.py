from flask import Flask, jsonify, request, send_file
import os
from sitemap_generator import SitemapGenerator  # Reverted import statement
import re

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Sitemap Generator</title>
        </head>
        <body>
            <h1>Sitemap Generator</h1>
            <form method="POST" action="/generate">
                <label for="url">Enter the URL to crawl:</label>
                <input type="text" id="url" name="url" required>
                <button type="submit">Generate Sitemap</button>
            </form>
        </body>
    </html>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form.get('url')

    if not url:
        return "No URL provided", 400

    # Validate URL format
    if not re.match(r'^(http|https)://', url):
        return "Invalid URL format", 400
    
    try:
        # Create output directory if it doesn't exist
        output_dir = "sitemaps"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate the sitemap
        generator = SitemapGenerator(url, output_dir)
        generator.crawl_website(max_pages=100)
        sitemap_path = generator.generate_xml_sitemap()
        
        # Send the sitemap file as a download
        return send_file(sitemap_path, as_attachment=True)
    except Exception as e:
        return f"Error generating sitemap: {str(e)}", 500

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Page not found"), 404

if __name__ == "__main__":
    app.run(debug=True)
