# -*- coding: utf-8 -*-
"""
Eugene Trutat partnership between Wikimedia France and the City archives of Toulouse
"""
__authors__ = 'User:Jean-Frédéric'

import csv


def isDefined(item):
    """Tests if the given item is defined, ie if it is not the NoneType nor an empty string
    """
    return item is not None and item is not ""


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), dialect=dialect, **kwargs)
    for row in csv_reader:
            # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
