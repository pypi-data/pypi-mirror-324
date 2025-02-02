import xmltodict, os, sys, datetime
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
def _read(feedFile):
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

def _help():
    print("uFM - unnamed Feed Reader")
    print("Available Commands:")
    print(" read <feedfile>    -   Read a RSS File")
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
            _read(args[1])
        case 'help':
            _help()
        case _:
            _help()
    sys.exit(0)

if __name__ == "__main__":
    _main()

