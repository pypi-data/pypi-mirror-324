import xmltodict, os, sys, datetime, requests, inscriptis, pydoc
from urllib.parse import urlparse
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

version = "0.2.4"

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

def _fetchallFeeds():
    target_dir = os.path.join(os.path.expanduser('~'), '.local', 'share', 'ufr', 'rss')
    os.makedirs(target_dir, exist_ok=True)
    
    feed_list_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'ufr', 'Feeds')
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
            print(f"Saved feed from {url}")
def _addURL(url):
    with open(f"{os.path.join(os.path.expanduser('~'), '.local', 'share', 'ufr', 'Feeds')}", 'a') as ufrlist:
        ufrlist.write(f"{url}\n")
def read(feedFile, page=True):
    try:
        if not os.path.isfile(feedFile):
            raise FileNotFoundError("Could not find the RSS Feed")
        feed = getFeedinfo(feedFile)
        result = f"{feed['Name']}\n{feed['URL']}\n{feed['Description']}\nLanguage: {feed['Language']}\n===================================\n"
        for i in feed['Items']:
            result += f"{i['Title']}\n{i['URL']}\n---\n{inscriptis.get_text(i['Desc'])}\n---\n{i['pubDate']} - {i['GUID']}\n-------------------------------\n"
        if not page:
            print(result)
        else:   
            pydoc.pager(result)
    except Exception as e:
        raise e
def _chunkView(page=True):
    feeds = os.listdir(os.path.join(os.path.expanduser('~'), '.local', 'share', 'ufr', 'rss'))
    if not feeds:
        return False
    for feed in feeds:
        read(os.path.join(os.path.expanduser('~'), '.local', 'share', 'ufr', 'rss', feed), page)
    return True
def _help():
    print(f"uFR - unnamed Feed Reader - Version {version}            ")
    print(f" Available Commands:                                     ")
    print(f"  read <feedfile>       -   Read a RSS File                 ")
    print(f"  add  <url>            -   Add an RSS Feed to your feedlist")
    print(f"  update                -   Update your feedlist            ")
    print(f"  chunk                 -   View every feed in your feedlist")
    print(f"  help                  -   Show this text                  ")
    print(f" Flags:                                                  ")
    print(f"  <read/chunk> --nopage -   Disable Paging                 ")
    sys.exit(0)

def _main():
    try:
        os.makedirs(os.path.join(os.path.expanduser('~'), '.local', 'share', 'ufr'), exist_ok=True)
        args = sys.argv[1:]
        if not args:
            print("  Please view <<ufr help>> for a list of commands")
            sys.exit(1)
        command = args[0]
        match command:
            case 'read':
                if len(args) < 2:
                    print("  Usage: <<ufr read [feed file]>>")
                    sys.exit(1)          
                page = True
                if "--nopage" in sys.argv:
                    page = False
                read(args[1], page)
            case 'help':
                _help()
            case 'add':
                if len(args) < 2:
                    print("  Usage: <<ufr add [URL]>>")
                    sys.exit(1)          
                _addURL(sys.argv[2])
            case 'update':
                _fetchallFeeds()    
            case 'chunk':
                page = True
                if "--nopage" in sys.argv:
                    page = False
                resp = _chunkView(page) 
                if resp == False:
                    print("Your feedlist is empty")
                    sys.exit(1)          
            case _:
                print("Unknown command, please view <<ufr help>>")  
                sys.exit(1)          
        sys.exit(0)
    except Exception as e:
        print(f'Fatal: {e}')

if __name__ == "__main__":
    _main()

