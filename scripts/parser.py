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
     --token=TOKEN           Authentication token provided by the OEP.
     --sep=SEP               Delimiter used in CSV-files. [default: ,]

"""

#arguments = {
#    "DATA" : "/home/martin/buergen/buergen_repository/buergen/data/Widerstand_Protestinhalt_Netzausbau.csv",
#    "DEFN" : "/home/martin/buergen/buergen_repository/buergen/data/Widerstand_Protestinhalt_Netzausbau.json",
#    "--schema" : "model_draft",
#    "--table" : "buergen_test",
#    "--token" : "",
#    "SEP" : ","}

import json
import pandas as pd
from time import sleep
from sys import stdout
from docopt import docopt
from buergen.oep.parser import OepParser
from buergen.oep.io import request_and_response
from buergen.helper import yes_or_no


APIURL = "http://oep.iks.cs.ovgu.de/api/v0/"

def read_table_definition(**arguments):
    with open(arguments['DEFN'], 'r') as f:
        defn = json.load(f)
    return defn

def read_data(**arguments):
    df = pd.read_csv(arguments['DATA'], dtype=str)
    return df


def main(**arguments):

    print("[+] Reading table definition.")
    defn = read_table_definition(**arguments)

    print("[+] Reading table data.")
    data = read_data(**arguments)

    p = OepParser(apiurl=APIURL,
                  schema=arguments['--schema'],
                  table=arguments['--table'],
                  token=arguments['--token'])

    print("[+] Creating table.")
    if p.check_table_exists():

        msg = "[-] Unfortunately this table does already exist.\n" \
            "[?] Do you want to delete it?"

        if yes_or_no(msg):
            p.delete_table()
        else:
            quit()

    p.create_table(body=defn)

    print("[+] Start inserting data.")
    for ix, s in data.iterrows():
        s.index = s.index.str.lower()
        body = {"query": s.to_dict()}
        p.insert_into_table(body=body, index=ix)
        sleep(20)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='parser.py v0.1')
    print('Startng parser.py!')
    main(**arguments)
    print('Done!!!')
