import os
import re
 
def replace_url_in_html_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    url_file_path = os.path.join(script_dir, 'url.txt')
    
    with open(url_file_path, 'r', encoding='utf-8') as file:
        desired_url = file.read().strip()
 
    pattern = re.compile(r'onerror=window.location=".*?"')
 
    for filename in os.listdir(script_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(script_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
 
            new_content = pattern.sub(f'onerror=window.location="{desired_url}"', content)
 
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
 
            print(f"Updated URL in file: {filename}")
 
replace_url_in_html_files()