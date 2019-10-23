import csv
from source import Source


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


class CSVSource(Source):
    def __init__(self, data):
        with open(data, mode='r') as infile:
            reader = unicode_csv_reader(infile, delimiter=';')
            self._contracts = {
                rows[0]: {
                    'field_%s' % str(k+1): v for k, v in enumerate(rows)
                } for rows in reader
            }

    @property
    def contracts(self):
        return self._contracts

    @staticmethod
    def setup_pool(data):
        return CSVSource(data)

    def send_reports(self, reports):
        pass

    def get_partner_data(self, contract_id):
        return self.contracts[contract_id]
