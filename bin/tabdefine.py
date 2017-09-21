#!/usr/bin/env python
""" Create table definition in JSON-format from CSV-file.

Usage:
  tabdefine.py [options] DATA
  tabdefine.py -h | --help

Examples:

  tabdefine.py path/to/table_data.csv

Arguments:

  DATA                 Path to a CSV-file containing table data.

Options:

  -h --help                  Show this screen and exit.
  -l --loglevel=LOGLEVEL     Set the loglevel. Should be one of DEBUG, INFO,
                             WARNING, ERROR or CRITICAL. [default: INFO]
     --geomtype=GEOMTYPE     Set geometry type. [default: multipolygon]

"""

import json
import pandas as pd
from docopt import docopt
from django.contrib.gis.geos import GEOSGeometry
from decimal import Decimal
import logging
import re
import os


class PGTYPE():
    """ """

    def __init__(self, name):

        if not re.match("^[a-zA-Z_]*$", name):
            raise ValueError("{} does not conform to format.".format(name))

        self.name = name.lower()

    def asdict(self):
        return {"name": self.name,
                "data_type": self.data_type}


class BOOLEAN(PGTYPE):

    def __init__(self, name):
        self.data_type = 'boolean'
        super().__init__(name)

    @classmethod
    def isvalid(cls, value):
        assert value in ['Ja', 'ja', '1', 'Nein', 'nein', '0']


class INTEGER(PGTYPE):

    def __init__(self, name):
        self.data_type = 'integer'
        super().__init__(name)

    @classmethod
    def isvalid(cls, value):
        int(value)
        assert not value.startswith('0')
        assert int(value) == float(value)


class FLOAT(PGTYPE):

    def __init__(self, name):
        self.data_type = 'double precision'
        super().__init__(name)

    @classmethod
    def isvalid(cls, value):

        int(value)
        assert not value.startswith('0')
        assert not float(value) == int(value)
        assert float(value) == Decimal(value)


class DECIMAL(PGTYPE):

    def __init__(self, name):
        self.data_type = 'numeric'
        super().__init__(name)

    @classmethod
    def isvalid(cls, value):

        Decimal(value)
        assert not value.startwith('0')
        assert not Decimal(value) == float(value)
        assert not Decimal(value) == int(value)


class GEOMETRY(PGTYPE):

    global arguments

    def __init__(self, name):
        self.data_type = 'geometry(%s)' % arguments['--geomtype']
        super().__init__(name)

    @classmethod
    def isvalid(cls, value):
        GEOSGeometry(value)


class VARCHAR(PGTYPE):

    def __init__(self, name):
        self.data_type = 'varchar'
        super().__init__(name)

    @classmethod
    def isvalid(cls, value):

        assert isinstance(value, str)
        assert len(value) < 50
        assert value not in ['Ja', 'ja', '1', 'Nein', 'nein', '0']

    def asdict(self):
        return {"name": self.name,
                "data_type": self.data_type,
                "character_maximum_length": 50}


class TEXT(PGTYPE):

    def __init__(self, name):
        self.data_type = 'text'
        super().__init__(name)

    @classmethod
    def isvalid(cls, value):

        assert isinstance(value, str)
        assert len(value) >= 50


TYPES = [BOOLEAN, INTEGER, FLOAT, DECIMAL, GEOMETRY, VARCHAR, TEXT]


def main(**arguments):

    # read file
    fname = arguments['DATA']
    basename = os.path.basename(fname).split('.')[0]
    df = pd.read_csv(fname, dtype=str)

    columns = []
    for name in df:
        for T in TYPES:
            try:
                df[name].apply(T.isvalid)
                columns.append(T(name).asdict())
            except:
                pass

    # add idcolumn
    idcolumn = {"name": "id", "data_type": "serial", "is_nullable": "NO"}
    columns.append(idcolumn)

    # create statement
    query = {
        "query":
            {
                "columns": columns,
                "constraints":
                    [{
                        "constraint_type": "PRIMARY KEY",
                        "constraint_parameter": "id"
                    }]
            }
        }

    with open(basename + '.json', 'w') as outfile:
        json.dump(query, outfile, indent=4, sort_keys=True)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='parser.py v0.1')
    logging.basicConfig(level=arguments['--loglevel'])
    logging.info('Starting tabdefine!')
    main(**arguments)
    logging.info('Done!!!')
