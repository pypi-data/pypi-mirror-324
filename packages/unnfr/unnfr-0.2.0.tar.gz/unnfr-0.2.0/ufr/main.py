import xmltodict, os, sys, datetime, requests
from urllib.parse import urlparse
def getFeedinfo(feed):
    
    if os.path.isfile(feed):
        with open(feed, 'r', encoding='utf-8') as f:
            feed = f.read()

    parsed = xmltodict.parse(xml_input=feed)
    rss = parsed['rss']
    feedInfo = {
        "Name": rss['channel']['title'],
        "URL": rss['channel']['link'],
        "Description": rss['channel']['description'],
        "Language": rss['channel'].get('language', 'C'),
        "Items": []
    }
    for i in rss['channel'].get('item', []):
        pubDate = datetime.datetime.now().isoformat()
        guid = "https://example.com"
        if 'pubDate' in i:
            pubDate = i['pubDate']
        if 'guid' in i:
            guid = i['guid']
        feedInfo['Items'].append({
            "Title": i['title'],
            "URL": i['link'],
            "Desc": i['description'],
            "GUID": guid,
            "pubDate": pubDate
        })
            

    return feedInfo
def getPost(feedInfo, title):
    if not isinstance(feedInfo, dict):
        return False
    for i in feedInfo['Items']:
        if i['Title'] != title:
            continue
        else:
            return i
    return False
def _addURL(url):
    with open(f"{os.path.expanduser('~')}/.ufr-list", 'a') as ufrlist:
        ufrlist.write(f"{url}\n")

def _fetchallFeeds():
    target_dir = os.path.join(os.path.expanduser('~'), '.local', 'ufr')
    os.makedirs(target_dir, exist_ok=True)
    
    feed_list_path = f"{os.path.expanduser('~')}/.ufr-list"
    if not os.path.isfile(feed_list_path):
        print("Please add a feed to your feedlist, using <<ufr add [URL]>>")
        return False
    
    with open(feed_list_path, 'r') as ufrlist:
        lines = ufrlist.readlines()
        for line in lines:
            url = line.strip()  
            if not url:
                continue  
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error fetching {url}: {response.status_code}")
                continue
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                print(f"URL does not contain a valid filename: {url}")
                continue
            target_path = os.path.join(target_dir, filename)
            with open(target_path, 'w', encoding='utf-8') as feed:
                feed.write(response.text)
            print(f"Saved feed from {url} to {target_path}")
def read(feedFile):
    try:
        if not os.path.isfile(feedFile):
            raise FileNotFoundError("Could not find the RSS Feed")
        feed = getFeedinfo(feedFile)
        print(feed['Name'])
        print(feed['URL'])
        print(feed['Description'])
        print(f"Language: {feed['Language']}")
        print("===================================")
        for i in feed['Items']:
            print(i['Title'])
            print(i['URL'])
            print(i['Desc'])
            print(f'{i['pubDate']} - {i['GUID']}')
            print("--------------------------")    
    except Exception as e:
        raise e
def _chunkView():
    feeds = os.listdir(os.path.join(os.path.expanduser('~'), '.local', 'ufr'))
    if not feeds:
        return False
    for feed in feeds:
        read(os.path.join(os.path.expanduser('~'), '.local', 'ufr', feed))
    return True
def _help():
    print("uFM - unnamed Feed Reader")
    print("Available Commands:")
    print(" read <feedfile>    -   Read a RSS File")
    print(" add  <url>         -   Add an RSS Feed to your feedlist")
    print(" update             -   Update your feedlist")
    print(" chunk              -   View every feed in your feedlist")
    print(" help               -   Show this text")
    sys.exit(0)

def _main():
    args = sys.argv[1:]
    if not args:
        _help()
    command = args[0]
    match command:
        case 'read':
            if len(args) < 2:
                _help()
            read(args[1])
        case 'help':
            _help()
        case 'add':
            if len(args) < 2:
                _help()
            _addURL(sys.argv[2])
        case 'update':
            _fetchallFeeds()    
        case 'chunk':
            resp = _chunkView() 
            if resp == False:
                print("Your feedlist is empty")
        case _:
            _help()
    sys.exit(0)

if __name__ == "__main__":
    _main()

