# -*- coding: utf-8 -*-
"""
Eugene Trutat partnership between Wikimedia France and the City archives of Toulouse
"""
__authors__ = 'User:Jean-Frédéric'


import re
from HelperFunctions import *
from StringFunctions import *
monthList = {u'janvier': 1, u"février": 2, u'mars': 3, u'avril': 4, u'mai': 5, u'juin': 6, u'juillet': 7, u'août': 8, u'septembre': 9, u'octobre': 10, u'novembre': 11, u'décembre': 12}


def lookForDate(analyse, creationYear):
    """
    Searches a given string for a date pattern, using regular expressions.
    Returns the date (either using the ISO YYY-MM-DD format or the {{Other date}} template) and the year.
    """
    fullDatePattern = re.compile("(?P<day>\d+?) (?P<month>[\w]+?) (?P<year>\d\d\d\d)", re.UNICODE)
    monthDatePattern = re.compile("(?P<month>[\w]+?) (?P<year>\d\d\d\d)", re.UNICODE)
    circaYearPattern = re.compile("Vers(\s*?)(?P<year>\d\d\d\d)", re.UNICODE)
    circaDatePattern = re.compile("Vers (?P<month>\w*?) (?P<year>\d\d\d\d)", re.UNICODE)
    betweenDatePattern = re.compile("Entre (?P<year1>\d\d\d\d) et (?P<year2>\d\d\d\d)", re.UNICODE)
    orDatePattern = re.compile("(?P<year1>\d\d\d\d) ou (?P<year2>\d\d\d\d)", re.UNICODE)
    #Pattern = re.compile("", re.UNICODE)

    fullDateR = re.search(fullDatePattern, analyse)
    monthDateR = re.search(monthDatePattern, analyse)
    circaYearR = re.search(circaYearPattern, analyse)
    circaDateR = re.search(circaDatePattern, analyse)
    betweenDateR = re.search(betweenDatePattern, analyse)
    orDateR = re.search(orDatePattern, analyse)

    if fullDateR:
        month = fullDateR.group('month').lower()
        if month in monthList.keys():
            year = fullDateR.group('year')
            date = u'%s-%s-%s' % (year, '%02d' % monthList[month], '%02d' % int(fullDateR.group('day')))
            dateCategory = u"%s in " % fullDateR.group('year')
            return (date, year)

    if monthDateR:
        month = monthDateR.group('month').lower()
        if month in monthList.keys():
            year = monthDateR.group('year')
            date = u'%s-%s' % (year, '%02d' % monthList[month])
            dateCategory = u"%s in " % monthDateR.group('year')
            return (date, year)

    if circaDateR:
        month = circaDateR.group('month').lower()
        if month in monthList.keys():
            year = circaDateR.group('year')
            date = u'{{Other date|circa|%s-%s}}' % (year, '%02d' % monthList[month])
            dateCategory = u"%s in " % circaDateR.group('year')
            return (date, year)

    if circaYearR:
        circaYear = circaYearR.group('year')
        date = u'{{Other date|circa|%s}}' % (circaYear)
        return (date, creationYear)

    if betweenDateR:
        date = u'{{Other date|between|%s|%s}}' % (betweenDateR.group('year1'), betweenDateR.group('year2'))
        return (date, creationYear)

    if orDateR:
        date = u'{{Other date|or|%s|%s}}' % (orDateR.group('year1'), orDateR.group('year2'))
        return (date, creationYear)

    return (creationYear, creationYear)


def parseFormat(format):
    """
    Parse, using a regular expression, the given string looking for a format, and splitting between width and height.
    """
    if isDefined(format):
        formatR = re.search(r"(?P<width>[\d,.]+?)\s*x\s*(?P<height>[\d,]+?)\s*$", format)
        width = formatR.group('width').replace(',', '.')
        height = formatR.group('height').replace(',', '.')
        return (width, height)
    else:
        return ('', '')


def parseSupport(support):
    values = {
      'VERRE': 'glass'}
    return values[support]


def parseTechnique(technique):
    values = {
      u'Photographie': u'photograph',
      u'Photographie stéréo': u'stereophotography'}
    return values[technique]


def identifyName(name):
    values = {
      u'SANS': 0,
      u'TRUTAT, Eugène': 1,
      u'ROUZAUD, H.': 2,
      u'LACGER, Jules': 3,
      u'LACGER': 3,
      u'PAGES, L.': 4,
      u'TRANTOUL': 5}
    if name in values.keys():
        return values[name]
    elif name is None or name is "":
        print "ERROR : None"
    else:
        parseName(name)
        print "TODO"
    return ""


def parsePersnameField(persnameField):
    if isDefined(persnameField):
        depictedList = []
        persnamesList = persnameField.split(';')
        for persname in persnamesList[:-1]:
            depictedList.append(parseName(persname))
    return depictedList


def parseName(name):
    nameR = re.search(r"(?P<nom>.+?),\s*(?P<prenom>.+?)$", name)
    if nameR:
        nom = nameR.group('nom')
        prenom = nameR.group('prenom')
        return  "%s %s" % (capitalizeFirst(prenom), capitalizeFirst(nom.capitalize()))

    return None


def getCommonsAuthor(authorID):
    values = {
      0: u"{{Unknown}}",
      1: u"{{Creator:Eugène Trutat}}",
      2: u"H Rouzaud",
      3: u"Jules Lacger",
      4: u"L Pages",
      5: u"Trantoul"}
    if authorID in values.keys():
        return values[authorID]


def identifyAnalyse(analyse):
    values = {
      u'NEGATIF N&B': 1,
      u'Positif N&B': 2}
    if analyse in values.keys():
        print values[analyse]
    elif analyse is None or name is "":
        print "None"
    else:
        print "ERROR"
    return ""
