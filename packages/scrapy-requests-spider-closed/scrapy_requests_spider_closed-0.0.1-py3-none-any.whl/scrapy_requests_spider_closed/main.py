import logging
import requests
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class RequestsSpiderClosed:
    def __init__(self, requests_parameters, reasons_trigger):
        self.requests_parameters = requests_parameters
        self.reasons_trigger = reasons_trigger

    @classmethod
    def from_crawler(cls, crawler):
        requests_parameters = crawler.settings.get('REQUESTS_SPIDER_CLOSED_REQUESTS_PARAMETERS', [])
        reasons_trigger = crawler.settings.get('REQUESTS_SPIDER_CLOSED_REASONS_TRIGGER', [])
        if not requests_parameters:
            logger.error('REQUESTS_SPIDER_CLOSED_REQUESTS_PARAMETERS is not set')
            raise NotConfigured
        if not reasons_trigger:
            logger.error('REQUESTS_SPIDER_CLOSED_REASONS_TRIGGER is not set')
            raise NotConfigured

        ext = cls(requests_parameters, reasons_trigger)

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    def spider_closed(self, reason):
        if reason not in self.reasons_trigger:
            logger.info(f'reason "{reason}" is NOT in reasons_trigger "{self.reasons_trigger}')
            return

        logger.info(f'reason: "{reason}" is in reasons_trigger "{self.reasons_trigger}"')

        for request_parameters in self.requests_parameters:
            response = requests.request(**request_parameters)
            logger.info(f'({response.status_code}) {response.url}')

            if not response.ok:
                logger.error(f'({response.status_code}) {response.url}, {response.text}')
