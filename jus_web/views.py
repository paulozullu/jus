# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from django.shortcuts import render


def search_process(request):
    """
    Get and send the data.
    """
    process_number = request.POST.get('process_number', '').strip()
    court = request.POST.get('court', '').strip()

    params = {
        'meta':
            {
                'process_number': process_number,
                'court': court
            },
        'spider_name': 'processes',
        'start_requests': True,
    }
    response = requests.post('http://localhost:9080/crawl.json', json=params)
    data = json.loads(response.text)

    context = {
        'process': data['items'][0]
    }

    return render(request, 'process_result.html', context)

