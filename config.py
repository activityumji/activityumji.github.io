from pathlib import Path

DB_PATH = "db/db.csv"

WECHAT_ACCOUNTS = [
    "JIers",
    "JIcareer",
    "JI觅源",
    "JI青团",
    "JIAdvisingCenter",
    "密院科协",
    "密院气象",
]

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"

# if True, use local cache in /src/
# otherwise, set wechat article cover url to qlogo.cn
USE_CACHED_ARTICLE_COVERS = True
# shame on Tencent, destroyer of the open web

COVER_PATH = Path("docs/src/")

INDEX_PATH = Path("docs/index.html")
TODAY_PATH = Path("docs/today.html")
GALLERY_PATH = Path("docs/gallery.html")
CATALOGS_PATH = Path("docs/activities/")
