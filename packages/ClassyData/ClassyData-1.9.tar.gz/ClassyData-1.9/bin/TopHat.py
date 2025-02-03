#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, argparse, json, datetime, xmltodict, uuid, logging
from Perdy.pretty import prettyPrintLn, Style

from jsonweb.encode import dumper
from jsonweb.decode import loader

if os.path.dirname(sys.argv[0]) == '.':
	sys.path.append('..')

from Classes import *
from Handlers.TopHat import TopHat, args

if __name__ == '__main__': 
	result = args.execute()
	if result:
		if isinstance(result, Base):
			result = json.loads(dumper(result))
		prettyPrintLn(result, ignore=True)



