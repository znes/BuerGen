"""
"""
import logging
from .io import request_and_response


class OepParser(object):
    """ Call the OEP """

    def __init__(self, *args, **kwargs):

        self.schema = kwargs.get('schema')
        self.table = kwargs.get('table')
        self.token = kwargs.get('token')
        self.apiurl = kwargs.get('apiurl')
        self.taburl = self.apiurl + 'schema' + '/' + self.schema +\
            '/' + 'tables' + '/' + self.table + '/'

    def check_table_exists(self):

        try:
            request_and_response('GET', self.taburl, 200)
            return True

        except AssertionError:
            logging.exception("Table does not exist yet.")

    def create_table(self, body):

        try:
            request_and_response('PUT', self.taburl, 201, body=body,
                                 token=self.token)

        except AssertionError:
            logging.exception("Oops, table could not be created.")

    def insert_into_table(self, body, index=None):

        # TODO other http request on new
        call = "rows/" + str(index) if index else "rows/new"

        try:

            request_and_response('PUT', self.taburl + call, 201,
                                 body=body, token=self.token)
            logging.info("Successfully inserted data at index {}.".format(index))

        except AssertionError:
            logging.exception("Oops, could not insert data at index {}.".format(index))

    def delete_table(self):

        try:
            request_and_response('DELETE', self.taburl, 200, token=self.token)
            logging.info("Table deleted.")

        except AssertionError:
            logging.exception("Oops, could not delete table.")
