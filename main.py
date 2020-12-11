#!/usr/bin/env python
import argparse
import logging
import os
from logging.config import dictConfig

import requests

import config
from utils import flatten

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

"""
Skeleton for Squirro Delivery Hiring Coding Challenge
October 2020
"""


dictConfig(config.LOGGING)
log = logging.getLogger(__name__)


class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    """

    base_url = "https://api.nytimes.com/svc/search/v2/"
    api_key = None

    def __init__(self, api_key: str):
        self.api_key = api_key

    def connect(self, inc_column=None, max_inc_value=None):
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def _read_n_articles(self, query: str, page_num: int) -> dict:
        params = {"q": query, "page": page_num, "api-key": self.api_key}

        response = requests.get(
            f"{self.base_url}articlesearch.json?{urlencode(params)}"
        )

        return response.json()

    def getDataBatch(self, query: str, batch_size: int) -> dict:
        """
        Generator - Get data from source on batches.

        :returns One list for each batch. Each of those is a list of
                 dictionaries with the defined rows.
        """

        for page_num in range(0, batch_size):
            results = self._read_n_articles(query, page_num)

            if results["status"] != "OK":
                raise Exception("Request failed!")

            log.info(f"Collected {len(results['response']['docs'])} articles")

            flattened_results = []

            for result in results["response"]["docs"]:
                flattened_article = flatten(result)
                flattened_results.append(
                    {
                        key: flattened_article[key]
                        for key in flattened_article.keys() & self.getSchema()
                    }
                )

            yield flattened_results

    def getSchema(self) -> set:
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """

        schema = {
            "abstract",
            "web_url",
            "lead_paragraph",
            "headline.main",
            "pub_date",
            "document_type",
            "news_desk",
            "section_name",
            "subsection_name",
            "byline.original",
            "type_of_material",
            "word_count",
            "_id",
        }

        return schema


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process NY Times data.")
    # Explicit is better than implicit.
    parser.add_argument(
        "--query", type=str, help="Search query", default="Silicon Valley"
    )
    parser.add_argument(
        "--pages", type=int, help="How many pages to get", default=10
    )
    args = parser.parse_args()

    source = NYTimesSource(api_key=os.getenv("API_KEY"))

    for idx, batch in enumerate(
        source.getDataBatch(query=args.query, batch_size=args.pages)
    ):
        print(f"{idx} Batch of {len(batch)} items")
        for item in batch:
            print(f"  - {item['_id']} - {item['headline.main']}")
