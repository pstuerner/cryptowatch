from uuid import uuid4
import feedparser
import newspaper
from time import mktime
from backend.db.chroma import ChromaDB


class RSSWatcher:
    def __init__(self) -> None:
        pass
        self.feeds = self._get_feeds_list()
        self.chroma = ChromaDB()

    def _get_feeds_list(self):
        return [
            "https://cointelegraph.com/rss",
            "https://cointelegraph.com/rss/tag/altcoin",
            "https://cointelegraph.com/rss/tag/bitcoin",
            "https://cointelegraph.com/rss/tag/ethereum",
            "https://cointelegraph.com/rss/tag/regulation",
            "https://cointelegraph.com/rss/category/weekly-overview"
        ]
    
    def fetch_rss_feeds(self):
        existing = list(set([x["url"] for x in self.chroma.client.get(include=["metadatas"])["metadatas"]]))
        articles = []
        for feed_url in self.feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                if entry.id in existing:
                    continue
                
                content = self.fetch_article_content(entry.id)
                articles.append(
                    {
                        "title": entry.title,
                        "url": entry.id,
                        "published": int(mktime(entry.published_parsed)),
                        "content": content,
                    }
                )
                print("Added", entry.id)

        return articles
    
    def fetch_article_content(self, article_url):
        article = newspaper.Article(article_url)
        try:
            article.download()
            article.parse()

            return article.text
        except Exception as e:
            return None
    
    def to_chroma(self, articles):
        for article in articles:
            self.chroma.insert(article)
        
        return True
    
    def run(self):
        articles = self.fetch_rss_feeds()
        insert = self.to_chroma(articles)

        return True
