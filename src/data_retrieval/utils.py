import const as cs

def get_url_content(url, errorMsg = ''):
    print(url)

    try:
        r = cs.req.get(url)
    except Exception as e:
        print(f"Exception! when getting {errorMsg}: {e}")
        exit(1)
    return cs.json.loads(r.content)

