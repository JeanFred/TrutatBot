# -*- coding: utf-8 -*-
"""
Eugene Trutat partnership between Wikimedia France and the City archives of Toulouse
"""
__authors__ = 'User:Jean-Frédéric'

import codecs
import re
from HelperFunctions import *
from StringFunctions import *


class GeonamesHandling():

    def __init__(self):
        self.geonamesType = {}
        self.lameGeoTable = {
    u"SAINT-VOLUSIEN (église)": u"[[Category:Église Saint-Volusien (Foix)]]",
    u"GARONNE (fleuve)": u"[[Category:Garonne]]",
    u"SAINT-JUST-DE-VALCABRERE (basilique)": u"[[Category:Basilique Saint-Just de Valcabrère]]",
    u"SAINT-BERTRAND-DE-COMMINGES (église)": u"[[Category:Cathédrale Notre-Dame de Saint-Bertrand-de-Comminges]]",
    u"ASSEZAT (hôtel particulier d')": u"[[Category:Hôtel d'Assézat]]",
    u"SAINT-ETIENNE (cathédrale)": u"[[Category:Cathédrale Saint-Étienne de Toulouse]]",
    u"SAINT-SERNIN (basilique)": u"[[Category:Basilique Saint-Sernin (Toulouse)]]",
    u"CAPITOLE (hôtel de ville)": u"[[Category:Capitole de Toulouse]]",
    u"CORDELIERS (église des)": u"[[Category:Église des Cordeliers de Toulouse]]",
    u"ARIEGE (rivière)": u"[[Category:Ariège River]]",
    #u"AUGUSTINS (cloître des)": u"[[Category:]]",
    u"PALAIS NIEL (Quartier général)": u"[[Category:Palais Niel]]",
    u"CITE DE CARCASSONNE": u"[[Category:Historic fortified city of Carcassonne]]",
    u"MATABIAU (gare)": u"[[Category:Gare de Toulouse-Matabiau]]",
    #u"": u"[[Category:]]",
    u"MONTASTRUC-LA-CONSEILLERE (ville)": u"[[Category:Montastruc-la-Conseillère]]",
    u"SAINT-ETIENNE (fontaine)": u"[[Category:Fontaine de la place Saint-Étienne]]",
    u"PONT-NEUF (pont)": u"[[Category:Pont-Neuf de Toulouse]]",
    u"CARMES (église des)": u"[[Category:Église Notre-Dame de la Dalbade]]",
    u"CARMES (marché des)": u"[[Category:Markets in Toulouse]]",
    u"JAURES (allées Jean)": u"[[Category:Allées Jean Jaurès (Toulouse)]]",
    u"CORNUSSON (hameau)": u"[[Category:Caylus]]"}

    def parseMetadataFileGeonames(self, geonamesFile):
        fileHandler = codecs.open(geonamesFile, 'r', 'utf-8')
        csvReader = unicode_csv_reader(fileHandler, delimiter='|', quotechar='"')
        geonamesType = {}
        for row in csvReader:
            geonamesType[row[0]] = row[1]
        self.geonamesType = geonamesType

    def parseGeoNameField(self, geonameField):
        #TODO:Use the more powerful "assert" to ensure geonameField is defined.
        """
        Specific method which parses the "Geoname" field and returns the city and a list of categories.
        It first splits the field into a list. The it iterates twice over the geonames list.
        During the first pass, it determinates the city and the "deepness level" of the location metadata.
        """
        city = None
        level = 5
        categoryList = []
        if isDefined(geonameField):
            geonamesList = geonameField.split(';')
            for geoname in geonamesList[:-1]:
                #print geoname
                (cityFound, levelFound) = self.processGeonameFirstPass(geoname)

                if isDefined(cityFound):
                    city = cityFound
                if isDefined(levelFound) and levelFound < level:
                    level = levelFound

            #print "Level : %s - City : %s"%(level,city)
            for geoname in geonamesList[:-1]:
                #print "Processing in 2nd pass %s"%geoname
                if(geoname in self.lameGeoTable.keys()):
                    category = self.lameGeoTable[geoname]
                else:
                    category = self.processGeonameSecondPass(geoname, city, level)

                if isDefined(category):
                    categoryList.append(category)
        return (categoryList, city)

    def processGeonameFirstPass(self, geoname):
        """

        """
        city = None
        if isDefined(geoname):
            geonameType = self.identifyGeonameType(geoname)
            if geonameType > 0 and geonameType < 10:  # Bâtiment & co
                return (None, 1)
            elif geonameType > 10 and geonameType < 20:  # streets & co
                return (None, 2)
            elif geonameType is 30:
                if geoname == "TOULOUSE (ville)":
                    return (1, 3)
                else:
                    #print "A city that is not Toulouse : %s"%geoname
                    return (2, 3)
            else:
                #print "Should not happen in processGeonameFirstPass : %s"%geoname
                return (None, None)

    def processGeonameSecondPass(self, geoname, city, level):
        if isDefined(geoname):
            geonameType = self.identifyGeonameType(geoname)
            #print "Type : %s"%geonameType
            if geonameType >= 0 and geonameType < 10 and level >= 1:  # Bâtiment & co
                # print "2nd pass - (non)generate category for edifice"
                return makeCategoryFromPlace(geoname, city)
                return None

            elif geonameType > 10 and geonameType < 20 and level >= 2:  # streets & co
                if(city is 1):  # 1 is Toulouse
                    #print "2nd pass - generate category for place"
                    return makeCategoryFromPlace(geoname, city)

            elif geonameType is 30 and level >= 3:  # COMMUNE
                if geoname == "TOULOUSE (ville)":
                    return "[[Category:Toulouse]]"
                    #print "At city level in Toulouse ? Should not happen"
                else:
                    #print "2nd pass - generate category for city"
                    return makeCategoryFromCity(geoname)
            elif geonameType is 0:
                print "Geoname not recognised : " + geoname
            else:
                plop = 1
                #print "Left out : " + geoname
        return None

    def identifyGeonameType(self, geoname):
        """
        Identifies the type of the given geoname.
        It first inferes the type from the metadata file, then identifies using regular expressions.
        """
        if geoname in self.geonamesType.keys():
            geonameType = self.geonamesType[geoname]
            if re.search("Lieux", geonameType):
                if re.search("RUE$", geonameType):
                    return 11
                elif re.search("AVENUE$", geonameType):
                    return 12
                elif re.search("ALLEE$", geonameType):
                    return 13
                elif re.search("ALLEES$", geonameType):
                    return 14
                elif re.search("PLACE$", geonameType):
                    return 15
                elif re.search("SQUARE$", geonameType):
                    return 16
                elif re.search("QUAI$", geonameType):
                    return 17
                elif re.search("BOULEVARD$", geonameType):
                    return 18
                elif re.search("QUARTIER", geonameType):
                    return 18
                elif re.search("PORT$", geonameType):
                    return 19  # Classified as Edifice, but Street for our purposes

                elif re.search("COMMUNE$", geonameType):
                    return 30
                elif re.search("HAMEAU$", geonameType):
                    return -1
                else:
                    # print geoname
                    return 40

            elif re.search("Edifice", geonameType):
                if re.search("STATUE$", geonameType):
                    return -1
                if re.search("PARTICULIER$", geonameType):
                    return -1
            #elif re.search("PONT$", geonameType):
                #return 3
            #elif re.search("STATUE$", geonameType):
                #return 9
            #elif re.search("$", geonameType):
                #return 5
            #elif re.search("$", geonameType):
                #return 6
            #elif re.search("$", geonameType):
                #return 7
            else:
                #print "Edifice drop out %s"%geoname
                return 9
        else:
            print "Cannot match geoname %s" % geoname
            return -1


def makeCategoryFromPlace(place, city):
    """

    """
    placeR = re.search(r"(?P<place1>.+?) \((?P<place2>.+?)\)$", place)
    if placeR:
        place1 = placeR.group('place1')
        place2 = placeR.group('place2')
        if re.search(u"'$", place2):
            category = "%s%s" % (place2, place1.capitalize())
        else:
            category = "%s %s" % (place2, place1.capitalize())
    else:
        category = place.capitalize()
    category = capitalizePlace(category)
    if city is 1:
        cityName = "Toulouse"
    return "[[Category:%s (%s)]]" % (capitalizeFirst(category), cityName)


def makeCategoryFromCity(place):
    placeR = re.search(r"(?P<place1>.+?) \((?P<place2>.+?)\)$", place)
    if placeR:
        place1 = placeR.group('place1')
        place2 = placeR.group('place2')
        category = place1.capitalize()

    category = capitalizePlace(category)
    return "[[Category:%s]]" % capitalizeFirst(category)
