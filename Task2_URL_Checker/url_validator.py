import csv
from urllib.parse import urlparse

def fix_common_issues(url):
    """Correct only verified URL syntax issues"""
    corrections = [
        ('http//', 'http://'),
        ('https//', 'https://')
    ]
    for wrong, right in corrections:
        url = url.replace(wrong, right)
    return url.strip()

def validate_urls(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8-sig') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['original_url', 'fixed_url', 'is_valid'])
        
        for i, row in enumerate(reader):
            if not row:  # Indentation fixed
                continue
                
            original = row[0].strip()
            if i == 0 and original.lower() == 'urls':
                continue
                
            fixed = fix_common_issues(original)  # Fixed typo (was fix.common_issues)
            parsed = urlparse(fixed)
            is_valid = bool(parsed.scheme and parsed.netloc)
            writer.writerow([original, fixed, is_valid])

if __name__ == '__main__':
    validate_urls("Task 2 - Intern.csv", "cleaned_urls.csv")