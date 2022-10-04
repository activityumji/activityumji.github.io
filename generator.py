import csv
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
from config import *


def utc_iso_datetime() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"  # HACK


class Generator:
    def __init__(self):
        self.jinja = Environment(
            loader=PackageLoader("generator"), autoescape=select_autoescape()
        )
        self.template = self.jinja.get_template("common.html")
        self.articles = []  # list of articles as dicts
        db_file = open(DB_PATH)
        reader = csv.reader(db_file)
        for row in reader:
            article = dict(
                zip(["aid", "timestamp", "date", "title", "acct", "cover", "url"], row)
            )
            if USE_CACHED_ARTICLE_COVERS:
                article["cover"] = f"/src/{article['aid']}.jpg"
            self.articles.append(article)
        db_file.close()

    def generate_index(self):
        """Generate index page"""
        now = datetime.now()
        html = self.template.render(
            {
                "index": True,
                "title": "UM-SJTU JI Activity",
                "path": "/index.html",
                "image": "/src/Cover1.jpg",
                "updated_date": str(now)[:10],
                "updated_datetime": str(now)[:19],
                "updated_isodatetime": utc_iso_datetime(),
                "posts": [
                    {
                        "path": f"/activities/{acct}.html",
                        "title": acct,
                        "cover": f"/src/{acct}.jpg",
                        "date": str(now)[:10],
                        "datetime": str(now)[:19],
                        "iso_datetime": utc_iso_datetime(),
                    }
                    for acct in WECHAT_ACCOUNTS
                ],
            }
        )
        f = open(INDEX_PATH, "w")
        f.write(html)
        f.close()

    def generate_catalog(self, acct=None, today_only=False):
        """Generate article catalog

        acct -- Name of wechat account to generate catalog for.
                Generate for all accounts (gallery) if None.
        today_only -- filter articles posted today
        """
        if acct and today_only:
            raise NotImplementedError

        now = datetime.now()
        today = str(now)[:10]
        articles = self.articles
        if acct:
            title = acct
            path = f"/activities/{acct}.html"
            image = f"/src/{acct}.jpg"
            articles = filter(lambda art: art["acct"] == acct, articles)
            save_to = CATALOGS_PATH / f"{acct}.html"
        elif today_only:
            title = "今日活动"
            path = f"/today.html"
            image = f"/src/Cover.jpg"
            articles = filter(lambda art: art["date"] == today, articles)
            save_to = TODAY_PATH
        else:
            title = "近期活动汇总"
            path = f"/gallery.html"
            image = f"/src/Cover.jpg"
            save_to = GALLERY_PATH

        html = self.template.render(
            {
                "index": False,
                "title": title,
                "path": path,
                "image": image,
                "updated_date": today,
                "updated_datetime": str(now)[:19],
                "updated_isodatetime": utc_iso_datetime(),
                "articles": articles,
            }
        )
        f = open(save_to, "w")
        f.write(html)
        f.close()


if __name__ == "__main__":
    generator = Generator()
    generator.generate_index()
    generator.generate_catalog()
    generator.generate_catalog(today_only=True)
    for acct in WECHAT_ACCOUNTS:
        generator.generate_catalog(acct=acct)
