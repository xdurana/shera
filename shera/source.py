from abc import ABCMeta, abstractmethod

class Source():

    __metaclass__ = ABCMeta

    @classmethod
    def setup_pool():
        return Source()

    @abstractmethod
    def send_reports(self, reports):
        """Send generated reports"""

    @abstractmethod
    def get_partner_data(self, contract_id):
        """Get partner data from source"""
