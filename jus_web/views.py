# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crochet import setup
from django.shortcuts import render
from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from common.connect import get_db
from jus_crawler.jus_crawler.spiders.processes import ProcessesSpider

setup()  # Avoid ReactorNotRestartable exception


def search_process(request):
    """
    Get and send the data.
    """
    db = get_db()

    process_number = request.POST.get('process_number', '').strip()
    court = request.POST.get('court', '').strip()

    start_crawl(process_number, court)

    process = db.processes.find_one({
        'process_number': process_number
    })

    context = {
        'process': process,
        'court': court
    }

    return render(request, 'process.html', context)


def start_crawl(process_number, court):
    """
    Starts the crawler.

        Args:
            process_number (str): Process number to be found.
            court (str): Court of the process.
    """
    runner = CrawlerRunner()
    dispatcher.connect(reactor.stop, signal=signals.spider_closed)
    process_info = runner.crawl(ProcessesSpider,
                                process_number=process_number,
                                court=court)
    process_info.addBoth(lambda _: reactor.stop())
