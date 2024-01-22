from common import *


def make_api_request(url):
    # Load the cache
    cache = load_cache()

    # Check if the response is already cached
    if url in cache:
        print(f"Retrieving cached data for {url}")
        return cache[url]

    params = {
        'api_key': key,
        'url': url
    }

    response = requests.get(api_base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {url}: {response.status_code}")
        return None

    cache[url] = response
    save_cache(cache)

    print(f"Request successful for {url}: {response.status_code}")
    return response


def find_urls(content):
    # Load the cache
    cache = load_cache()

    cache_key = f"openai-{content}"  # Unique key for this content

    if cache_key in cache:
        print("Using cached OpenAI response.")
        return cache[cache_key]

    print("Finding Page URLs")
    # Regular expression pattern for finding URLs
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'

    found_urls = re.findall(url_pattern, content)

    message = """
                Here is a comma separated list of URLs. Identify which URLs are likely to be Wholesale websites or similar. Ignore 
                common website headers like Google or w3, and focus only on domain names related to wholesale or 
                similar. ONLY respond with a comma separated list of only the url part, exclude any "\n" you might see.
                If you recognize that many links might have the same base url but with different paths then exclude all 
                only have 1 instance of each base url and no parameters. Remember to include the full url for the eligible 
                ones so like "https://" etc.

                URLs:
                {}
                """

    batch_size = 50

    filtered_urls = []

    for i in range(0, len(found_urls), batch_size):
        batch_urls = found_urls[i:i + batch_size]
        urls_string = ",".join(batch_urls)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": message.format(urls_string)}
            ],
            temperature=0.2
        )

        filtered_urls.extend(response.choices[0].message.content.split(","))
        break

    cache[cache_key] = filtered_urls
    save_cache(cache)

    return list(set(filtered_urls))
