import csv
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_single_url(url):
    """Check status of one URL"""
    try:
        if not urlparse(url).scheme:
            url = 'https://' + url
            
        response = requests.get(
            url,
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0'},
            allow_redirects=True
        )
        return (url, response.status_code)
    except Exception as e:
        return (url, f"Error: {str(e)}")

def check_urls_parallel(input_file, output_file, max_workers=10):
    """Process URLs in parallel"""
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        # Read only valid URLs from the cleaned file
        urls = [row[1] for row in csv.reader(f) 
               if row and row[2] == 'True']  # Skip header and invalid URLs
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_single_url, url): url for url in urls}
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['url', 'status'])
            
            for future in as_completed(futures):
                url, status = future.result()
                writer.writerow([url, status])
                print(f"({status}) {url[:60]}...")  # Progress tracking

if __name__ == "__main__":
    check_urls_parallel("cleaned_urls.csv", "url_status_results.csv")