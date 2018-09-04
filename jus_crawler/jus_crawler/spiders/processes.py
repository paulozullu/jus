# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

from jus_crawler.jus_crawler.items import ProcessItem


class ProcessesSpider(scrapy.Spider):
    name = 'processes'

    custom_settings = {
        'ITEM_PIPELINES': {
            'jus_crawler.jus_crawler.pipelines.JusCrawlerPipeline': 300
        }
    }

    def start_requests(self):
        self.start_urls = [
            'https://esaj.tjsp.jus.br/cpopg/open.do',
            'https://www.tjms.jus.br/cpopg5/open.do'
        ]
        process_number = getattr(self, 'process_number', None)
        court = getattr(self, 'court', None)

        if court == 'tjsp':
            url = self.start_urls[0]
        elif court == 'tjms':
            url = self.start_urls[1]

        request = scrapy.Request(url=url, callback=self.parse)
        request.meta['process_number'] = process_number
        request.meta['court'] = court

        yield request

    def parse(self, response):
        process_number = response.meta["process_number"]

        request = scrapy.FormRequest.from_response(
            response,
            formdata={'dadosConsulta.valorConsulta': process_number},
            callback=self.get_process_info
        )
        request.meta['process_number'] = process_number
        request.meta['court'] = response.meta['court']

        yield request

    def get_process_info(self, response):
        """
        Get process data.
        """
        sel = Selector(response)

        area_xpath = '//span[contains(text(), "%s")]/following-sibling' \
                     '::text()'
        area = getSingleElement(area_xpath, "Área", sel)

        classe_xpath = '//label[contains(text(), "%s")]/parent::td/' \
                       'following-sibling::td/table/tr/td/span/span/text()'
        classe = getSingleElement(classe_xpath, "Classe:", sel)

        common_xpath = '//label[contains(text(), "%s")]/parent::td/' \
                       'following-sibling::td/span/text()'
        assunto = getSingleElement(common_xpath, "Assunto:", sel)

        distribuicao = getSingleElement(common_xpath, "Distribuição:",
                                        sel).split(' ')[0]
        juiz = getSingleElement(common_xpath, "Juiz:", sel)

        valor_acao = getSingleElement(common_xpath, "Valor da ação:",
                                      sel).replace(' ', '')

        partes_do_processo = getProcessParts(sel)

        movimentacoes = getHistory(sel)

        item = ProcessItem()
        item['process_number'] = response.meta["process_number"]
        item['court'] = response.meta['court']
        item['area'] = area
        item['class_'] = classe
        item['subject'] = assunto
        item['distribution_date'] = distribuicao
        item['judge'] = juiz
        item['value'] = valor_acao
        item['parts'] = partes_do_processo
        item['changes'] = movimentacoes

        # open_in_browser(response)

        return item


def getSingleElement(xpath, param, sel):
    """
    Get text from
        Args:
             xpath (str): Text representing the xpath.
             param(str): Text to be found in the label.
             sel(Selector): Object that will be  browsed.

        Returns:
            str: Text that matches the search.
    """
    local_xpath = xpath % (param)
    result = sel.xpath(local_xpath.decode('utf8')). \
        extract_first().strip()

    return result


def getProcessParts(sel):
    """
    Get participants of the process.

        Args:
            sel (Selector): Object that will be  browsed.

        Returns:
            (list): A list of dict with the data.
    """
    result_list = list()
    applicant_xpath = '//table[@id="tableTodasPartes"]/tr[@class="fundoClaro"]'
    applicant_list = sel.xpath(applicant_xpath)

    for td in applicant_list.xpath('.'):
        title = td.xpath('./td[1]/span/text()').extract_first().strip()
        applicant = td.xpath('./td[2]/text()').extract_first().strip()
        applicant_parts = td.xpath('./td[2]/span')

        applicant_list = list()
        for span in applicant_parts:
            part_type = span.xpath('./text()').extract_first().encode('ascii', 'ignore')
            part_name = span.xpath('./following-sibling::text()').extract_first()
            part_str = (part_type + ' ' + part_name.strip())

            applicant_list.append(part_str)

        result_list.append({
            'applicant': title + ' ' + applicant,
            'applicant_parts': applicant_list
        })

    return result_list


def getHistory(sel):
    """
       Get participants of the process.

           Args:
               sel (Selector): Object that will be  browsed.

            Returns:
                (list): A list of dict with the data.
    """
    result_list = list()
    dates_path = '//tbody[@id="tabelaTodasMovimentacoes"]/tr/td[position() = 1]/text()'
    dates_list = sel.xpath(dates_path).extract()
    changes_path = '//tbody[@id="tabelaTodasMovimentacoes"]/tr/td[position() = 3]'
    changes_list = sel.xpath(changes_path)

    for date_, change in zip(dates_list, changes_list):
        title = change.xpath('./text()').extract_first().strip()
        abstract = change.xpath('./span/text()').extract_first().strip()

        move = title + abstract if abstract else title

        result_list.append({
            'data': date_.strip(),
            'move': move
        })

    return result_list

