from gnews import GNews

scraper = GNews()

top_news = scraper.get_news_by_topic('WORLD')

print(top_news)