from common import *
from utils import *


def initialize_search():
    print("Initializing Search...")

    # Your initial setup
    brand_addons = ["Colgate", "Logitech"]
    category_addons = ["Trade show", "Health & Beauty", "Electronics"]
    keyword_phrases = []

    # Generating keyword phrases
    for brand_addon in brand_addons:
        keyword_phrases.append(urllib.parse.quote("Wholesale Supplier " + brand_addon))
        keyword_phrases.append(urllib.parse.quote(brand_addon + " Wholesale Supplier"))

    for category_addon in category_addons:
        keyword_phrases.append(urllib.parse.quote("Wholesale Supplier " + category_addon))
        keyword_phrases.append(urllib.parse.quote(category_addon + " Wholesale Supplier"))

    # return keyword_phrases
    return [urllib.parse.quote("Wholesale Suppliers USA")]


def search_keywords_pages(keyword_phrases):
    print("Searching Keyword Pages")
    base_url = 'https://www.google.com/search?q='

    data = {
        'URL': [],
        'Content': []
    }

    for phrase in keyword_phrases:
        url = base_url + phrase
        response = make_api_request(url)

        if response is not None:
            data['URL'].append(url)
            data['Content'].append(response.text)

    # Convert to DataFrame
    return pd.DataFrame(data)


def search_keyword_links(page_data):
    print("Searching for Keyword Links")
    page_contents = page_data['Content']
    links = {'URL': []}

    for content in page_contents:
        # find all urls on page
        urls = find_urls(content)
        links['URL'].extend(urls)

    return links


def collect_supplier_info(links_data):
    print("Collecting Supplier Info")
    supplier_urls = links_data['URL']

    supplier_info = [{"name": "",
                      "url": "",
                      "email": "",
                      "phone": 0}]
    for url in supplier_urls:
        content = make_api_request(url)

        if content is not None:
            name_pattern = r'Supplier Name: ([\w\s]+)'
            name_matches = re.findall(name_pattern, content.text)

            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_matches = re.findall(email_pattern, content.text)

            phone_pattern = r'\(?\b\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b'
            phone_matches = re.findall(phone_pattern, content.text)

            # Assuming each page contains one supplier's info
            supplier_info.append({
                "name": name_matches[0] if name_matches else "Unknown",
                "url": url,
                "email": email_matches[0] if email_matches else "Unknown",
                "phone": phone_matches[0] if phone_matches else "Unknown"
            })

    return pd.DataFrame(supplier_info[1:])


def extract_info(info):
    print("Extracting Supplier Info")

    # Extracting each field from the DataFrame
    name = info['name']
    url = info['url']
    email = info['email']
    phone = info['phone']

    extracted_info = pd.DataFrame({'Name': name, 'URL': url, 'Email': email, 'Phone': phone})

    # Path to save the CSV file
    path = os.getcwd() + '/res.csv'

    # Saving the DataFrame to a CSV file
    extracted_info.to_csv(path, index=False)

    return path


def start():
    keyword_phrases = initialize_search()
    page_data = search_keywords_pages(keyword_phrases)
    links_data = search_keyword_links(page_data)
    supplier_info = collect_supplier_info(links_data)
    output_file = extract_info(supplier_info)

    return output_file


if __name__ == '__main__':
    print("Starting collection process...")
    file_path = start()
    print(f"Collection complete! Exported to: {file_path}")
