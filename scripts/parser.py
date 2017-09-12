""" Parse data to the OEP

Usage:
  parser.py [options] DEFN DATA
  parser.py -h | --help

Examples:

  python parser.py -s 'schemaname' -t 'tablename' --token 11549d0315c95cd2e011569b338e19efmm4 path/to/table_definition.json path/to/table_data.csv

Arguments:

  DEFN                 Path to a JSON-file containing the table definition.
  DATA                 Path to a CSV-file containing table data.

Options:

  -h --help                  Show this screen and exit.
  -s --schema=SCHEMA         Name of the OEP schema. [default: model_draft]
  -t --table=TABLE           Name of the OEP table. [default: buergen_test]
  -l, --loglevel=LOGLEVEL    Set the loglevel. Should be one of DEBUG, INFO,
                             WARNING, ERROR or CRITICAL. [default: INFO]
     --token=TOKEN           Authentication token provided by the OEP.
     --sep=SEP               Delimiter used in CSV-files. [default: ,]

"""

# arguments = {
#    "DATA" : "/home/martin/buergen/buergen_repository/buergen/data/Widerstand_Protestinhalt_Netzausbau.csv",
#    "DEFN" : "/home/martin/buergen/buergen_repository/buergen/data/Widerstand_Protestinhalt_Netzausbau.json",
#    "--schema" : "model_draft",
#    "--table" : "buergen_test",
#    "--token" : "",
#    "SEP" : ","}

import json
import logging
import pandas as pd
from docopt import docopt
from buergen.oep.parser import OepParser
from buergen.helper import yes_or_no
from django.contrib.gis.geos import GEOSGeometry


APIURL = "http://oep.iks.cs.ovgu.de/api/v0/"

def read_table_definition(**arguments):
    with open(arguments['DEFN'], 'r') as f:
        defn = json.load(f)
    return defn


def read_data(**arguments):
    def read_geom(i):
        return str(GEOSGeometry(i, srid=25832))
    df = pd.read_csv(arguments['DATA'], dtype=str, converters={'geom': read_geom})
    return df


def main(**arguments):

    logging.info("Reading table definition.")
    defn = read_table_definition(**arguments)

    logging.info("Reading table data.")
    data = read_data(**arguments)

    p = OepParser(apiurl=APIURL,
                  schema=arguments['--schema'],
                  table=arguments['--table'],
                  token=arguments['--token'])

    logging.info("Creating table.")
    if p.check_table_exists():

        logging.warning("Unfortunately table {} does already exist.".format(
            arguments['--table']))

        msg = "Do you want to delete it?"

        if yes_or_no(msg):
            p.delete_table()
        else:
            quit()

    p.create_table(body=defn)

    logging.info("Start inserting data.")
    data.columns = data.columns.str.lower()
    records = data.to_dict(orient='records')
    p.insert_into_table(body={'query': records})


if __name__ == '__main__':
    arguments = docopt(__doc__, version='parser.py v0.1')
    logging.basicConfig(level='DEBUG')
    logging.info('Starting parser.py!')
    main(**arguments)
    logging.info('Done!!!')
