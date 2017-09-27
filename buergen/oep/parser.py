""" Simple and easy-to-read interface for the OEP api
"""
import logging
from .io import request_and_response


class OepParser(object):
    """ Interface for the OEP api.

    The interface holds easy-to-understand methods for calling the OEP api.

    Parameters
    ----------
    schema : str
        Schema name.
    table : str
        Table name.
    token : str
        Authentictaion token provided by the OEP.
    apiurl : str
        Url of OEP api.
    taburl : str
        Url to OEP api with table specification.


    Notes
    -----

    Link to api-docs:
    http://oep-data-interface.readthedocs.io/en/latest/api/how_to.html
    """

    def __init__(self, *args, **kwargs):

        self.schema = kwargs.get('schema')
        self.table = kwargs.get('table')
        self.token = kwargs.get('token')
        self.apiurl = kwargs.get('apiurl')
        self.taburl = self.apiurl + 'schema' + '/' + self.schema +\
            '/' + 'tables' + '/' + self.table + '/'

    def check_table_exists(self):
        """ Verify table exists.

        Returns
        -------
            boolean

        """

        res = request_and_response('GET', self.taburl, None)
        return True if res.status_code == 200 else False

    def create_table(self, body):
        """ Create empty table in OEP.

        Attributes
        ----------

        body: dict
            Dict of specific format. See notes for this class.

        Returns
        -------
            None

        """

        logging.info("Create table.")
        request_and_response('PUT', self.taburl, status_code=201, body=body,
                             token=self.token)

    def insert_into_table(self, body):
        """ Bulk insert new data into the table.

        Attributes
        ----------

        body: dict
            Dict of specific format. See notes for this class.

        Returns
        -------
            None

        """

        call = "rows/new"

        logging.info("Insert data.")
        request_and_response('POST', self.taburl + call, status_code=201,
                             body=body, token=self.token)

    def delete_table(self):
        """ Delete table.

        Returns
        -------
            None

        """

        logging.info("Delete table.")
        request_and_response('DELETE', self.taburl, status_code=200,
                             token=self.token)
