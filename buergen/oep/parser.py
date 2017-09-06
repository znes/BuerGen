"""
"""

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
            request_and_response(self.taburl, 'get', 200)
            return True

        except AssertionError:
            print("Table does not exist yet.")

    def create_table(self, body):

        try:
            request_and_response(self.taburl, 'put', 201, body=body,
                                 token=self.token)

        except AssertionError:
            print("Oops, table could not be created.")

    def insert_into_table(self, body, index=None):

        call = "rows/" + str(index + 1) if index else "rows/new"

        try:

            request_and_response(self.taburl + call, 'put', 201,
                                 body=body, token=self.token)
            print("Successfully inserted data at index {}.".format(index))

        except AssertionError:
            print("Oops, could not insert data at index {}.".format(index))

    def delete_table(self):

        try:
            request_and_response(self.taburl, 'del', 200, token=self.token)
            print("Table deleted.")

        except AssertionError:
            print("Oops, could not delete table.")
