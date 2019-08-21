def request(url):
    import keys
    import requests
    api_key = keys.get_key()
    headers = {'X-API-Key': api_key}
    r = requests.get(url=url, headers=headers)
    return r.content

def bill_search(query):
    url = f"https://api.propublica.org/congress/v1/bills/search.json?query={query}"
    return request(url)