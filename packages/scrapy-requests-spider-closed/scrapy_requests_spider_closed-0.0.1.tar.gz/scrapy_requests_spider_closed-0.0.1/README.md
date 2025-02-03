# scrapy-requests-spider-closed

scrapy-requests-spider-closed is an extension to make requests when the spider is closed.

Use cases: 
- You must make a request to an API when the spider is closed.
- You make a request to an API when the scraping is finished, your API will create a report with the data scraped.
- Etc.

## Installation
Install scrapy-requests-spider-closed using pip:
```bash
pip install git+https://github.com/XavierZambrano/scrapy-requests-spider-closed.git
```


## Configuration
1. Add the `REQUESTS_SPIDER_CLOSED_REASONS_TRIGGER` in your `settings.py` file.
```python
REQUESTS_SPIDER_CLOSED_REASONS_TRIGGER = ['finished', 'cancelled', 'shutdown']
```
The `REQUESTS_SPIDER_CLOSED_REASONS_TRIGGER` is a list of reasons that will trigger the requests. [reasons](https://docs.scrapy.org/en/latest/topics/signals.html?highlight=finish%20reason#spider-closed).

2. Add the `REQUESTS_SPIDER_CLOSED_REQUESTS_PARAMETERS` in your `settings.py` file.
```python
REQUESTS_SPIDER_CLOSED_REQUESTS_PARAMETERS = [
    {
        'method': 'POST',
        'url': 'https://myapi-xxx.com/endpoint',
    }
]
```
You can use any parameter that the [requests](https://requests.readthedocs.io/en/latest/api/) library accepts.

3. Enable `SpiderClosedRequests` by adding it to the `EXTENSIONS` in your `settings.py` file.
```python
EXTENSIONS = {
   "scrapy_requests_spider_closed.RequestsSpiderClosed": 0,
}
```
