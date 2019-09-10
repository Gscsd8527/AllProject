from scrapy.cmdline import execute
if __name__ == '__main__':
    # execute(['scrapy', 'crawl', 'authorsId'])
    # execute(['scrapy', 'crawl', 'authorsCj'])
    execute('scrapy crawlall'.split())

