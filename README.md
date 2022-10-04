# So you are the Chosen One to maintain activityumji.github.io

## Dependencies

- Python 3 (tested on 3.10.7, Arch Linux)
- [Requests](https://requests.readthedocs.io/)
- [Selenium](https://pypi.org/project/selenium/)
- [Jinja](https://jinja.palletsprojects.com/)

## Setup

Clone repo and `cd` into it.

Download [`chromedriver`](https://chromedriver.chromium.org/downloads)
into this directory. Edit executable path in `config.py` if necessary.

## Update site

Two steps:

1. `python spider.py`
2. `python generator.py`

In step one you will need to scan a QR code to log into mp.weixin.qq.com.
Select an Official Account (公众号), not a Mini Program (小程序).

You need to hurry because there is a timeout.

The original author of `spider.py` warned against the use of VPNs.

Article metadata will be written into `db/db.csv` in reverse chronological
order.

Cover images of articles will be saved into `docs/src/`.

## Troubleshooting

### `spider.py` says 『获取 token 失败』

Try again, but scan QR code as fast as you can.

If this still doesn't work, edit this line:

```python
time.sleep(10)
```

Or move somewhere with better internet.

### `spider.py` is stuck for five minutes

Interrupt, then re-run.

If in a hurry, go to `config.py` and comment out wechat accounts you
already downloaded updates from. Remember to uncomment later.

### Encoding problem

You are not using UTF-8. Use UTF-8. This is not a suggestion; this is
a threat.

## TODO

- [ ] Improve login process
- [ ] Complete automation
- [ ] Detect cover image format
- [ ] Fix CSS
