from scrapy.cmdline import execute
if __name__ == '__main__':
    # execute(['scrapy', 'crawl', 'reference'])
    execute(['scrapy', 'crawl', 'citedBy'])
    # execute(['scrapy', 'crawl', 'related'])

    #execute('scrapy crawlall'.split())
