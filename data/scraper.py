#BEGIN CODE

import json
import requests
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning 
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

#STEP 2 Implement fetch_page():
def fetch_page(url):
   response = requests.get(url)
   return response.text

#STEP 3 Implement parse_page():
def parse_page(html):
   soup = BeautifulSoup(html, 'html.parser')
   title = soup.find('title').get_text()
   
   main_content = soup.find('article')
   if main_content:
      content = main_content.get_text()
   else:
      content = ""

   return {'title': title, 'content': content}

def get_docs_links(html, base_url):
   soup = BeautifulSoup(html, 'html.parser')
   links = []
   
   # Sections we want to scrape
   doc_sections = ['/tutorial/', '/advanced/', '/reference/', '/learn/']

   for a_tag in soup.find_all('a', href=True):
      href = a_tag['href']

      if href.startswith('/') and not href.startswith('//'):
         full_url = base_url.rstrip('/') + href
      elif href.startswith(base_url):
         full_url = href
      else:
         continue  # Skip external links
      
      # Only keep links that are in our doc sections
      if any(section in full_url for section in doc_sections):
         links.append(full_url)
   
   return list(set(links))

def get_urls_from_sitemap(sitemap_url):
   sitemap_xml = fetch_page(sitemap_url)
   soup = BeautifulSoup(sitemap_xml, 'html.parser')
   urls = [loc.get_text() for loc in soup.find_all('loc')]
   return urls

def scrape_all_docs(sitemap_url, output_file):
    # 1. Get all URLs from sitemap
   urls = get_urls_from_sitemap(sitemap_url)
    # 2. Create empty list for results
   results = []
    # 3. Loop through each URL:
    #    - fetch the page
    #    - parse it
    #    - append {url, title, content} to results
    #    - print progress
   for i, url in enumerate(urls):
      html = fetch_page(url)
      parsed = parse_page(html)
      results.append({
         'url' : url,
         'title' : parsed['title'],
         'content' : parsed['content']  
      })
   print(f"Scraped {i+1}/{len(urls)}: {url}")
    # 4. Save results list to JSON file
   with open(output_file, 'w', encoding='utf-8') as f:
      json.dump(results, f, ensure_ascii=False, indent=2)

# Test it
if __name__ == "__main__":
    with open("data/raw/fastapi_docs.json", "r", encoding="utf-8") as f:
        docs = json.load(f)
    
    print(f"Total docs: {len(docs)}")
    print(f"\nFirst doc title: {docs[0]['title']}")
    print(f"Content preview: {docs[0]['content'][:300]}")
