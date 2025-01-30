#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, argparse, json, datetime, xmltodict, uuid, logging
from Perdy.pretty import prettyPrintLn, Style

if os.path.dirname(sys.argv[0]) == '.':
	sys.path.append('..')

from Handlers.TopHat import TopHat, args

if __name__ == '__main__': 
	result = args.execute()
	if result:
		prettyPrintLn(result, ignore=True)



