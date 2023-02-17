from gnews import GNews

scraper = GNews()

top_news = scraper.get_news_by_location(country='IN')

print(top_news)