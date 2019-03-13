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
                    'CUPS': rows[0],
                    'address': rows[1],
                    'city': rows[2],
                    'province': rows[3],
                    'language': rows[4]
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

    def get_partner_data(self, cups):
        return self.contracts[cups]
