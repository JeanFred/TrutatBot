# -*- coding: utf-8 -*-
"""
Eugene Trutat partnership between Wikimedia France and the City archives of Toulouse
"""
__authors__ = 'User:Jean-Frédéric'

import xml.dom.minidom
import codecs
import re
import sys
import argparse
import time
from parsers import *
from GeonamesHandling import *
from HelperFunctions import *
from StringFunctions import *
sys.path.append("/media/easel/PythonTuile/pywikipedia")
import upload


def processMetadataFile(metadataFile, geonamesFile):
    global GeonamesHandlingClass
    GeonamesHandlingClass = GeonamesHandling()
    GeonamesHandlingClass.parseMetadataFileGeonames(geonamesFile)
    out = codecs.open('sortie.csv', 'w', 'utf-8')
    out2 = codecs.open('geonames.txt', 'w', 'utf-8')
    doc = xml.dom.minidom.parse(metadataFile)

    dateFoundList = []
    localRoot = u"FRAC31555_51Fi"
    characterBlackList = [u'[', u']', u': ']
    commonsFileDescriptions = {}
    commonsFileNames = {}
    localFileNames = {}
    geonames = {}
    #headerLine=u'{'.join(['Cote','Titre','Auteur','Date','Analyse','Format',"Technique","Support","Origine","Sujet","geoname","persname","corpname",'\n'])
    #out.write(headerLine)
    for images in doc.childNodes:
        if images.localName == u'AllDocsFigurés':
            for image in images.childNodes:
                if image.localName == u'DocsFigurés':
                    id = handleNode(image, u'Cote')
                    title = handleNode(image, u'Titre')
                    analyse = handleNode(image, u'Analyse')
                    creationYear = handleNode(image, u'Réalisé_en')
                    author = handleNode(image, u'Auteur')
                    typeDoc = handleNode(image, u'Type_Doc')
                    support = handleNode(image, u'Support')
                    technique = handleNode(image, u'Technique')
                    format = handleNode(image, u'Format')
                    observations = handleNode(image, u'Observations')
                    origine = handleNode(image, u'Origine')
                    subject = handleNode(image, u'subject')
                    geoname = handleNode(image, u'geoname')
                    persname = handleNode(image, u'persname')
                    corpname = handleNode(image, u'corpname')
                    #csvLine=u'{'.join([id,title,author,creationYear,typeDoc,format,technique,support,origine,subject,geoname,persname,corpname,'\n'])
                    #out.write(csvLine)
                    (commonsTpl, year) = createCommonsDescription(id, title, author, creationYear, typeDoc, format, technique, support, analyse, observations, origine, subject, geoname, persname, corpname)
                    commonsFileDescriptions[id] = commonsTpl
                    if(isDefined(year)):
                        commonsFileNames[id] = u"%s (%s) - %s - Fonds Trutat.jpg" % (removeBadCharacters(title, characterBlackList), year, id)
                    else:
                        commonsFileNames[id] = u"%s - %s - Fonds Trutat.jpg" % (removeBadCharacters(title, characterBlackList), id)
                    localFileNames[id] = localRoot + str(id[4:]).rjust(3, '0') + u".jpg"

    return commonsFileDescriptions, commonsFileNames, localFileNames


def createCommonsDescription(id, title, author, creationYear, typeDoc, format, technique, support, analyse, observations, origine, subject, geoname, persname, corpname):
    #print "\n---------------"
    #print id
    categoriesList = []
    commonsGallery = u"{{Institution:Archives municipales de Toulouse}}"
    commonsAuthor = getCommonsAuthor(identifyName(author))
    commonsDimensions = u"{{Size|cm|%s|%s}}" % parseFormat(format)
    commonsTechnique = parseTechnique(technique)
    commonsMedium = u"{{Technique|%s|%s}}" % (commonsTechnique, parseSupport(support))
    creditLine = u"""{{ProvenanceEvent|time=1971|type=gift|newowner=Association des Toulousains de Toulouse|oldowner=Jean Trutat}}
    {{ProvenanceEvent|time=2006-12-14|type=deposited|newowner=Archives municipales de Toulouse|oldowner=Association des Toulousains de Toulouse}}"""

    commonsDescription = u"{{fr|%s}}" % analyse

    if(identifyName(author) is 1):
        commonsLicense = u"{{PD-old-100}}"
    else:
        commonsLicense = u"{{PD-old-70}}"

    if isDefined(observations):
        commonsNotes = u"{{fr|%s}}" % observations
    else:
        commonsNotes = ""

    if isDefined(persname):
        depictedPersonList = parsePersnameField(persname)
        commonsDescription = commonsDescription + "\n{{Depicted person|" + "|".join(depictedPersonList) + "}}"
        for person in depictedPersonList:
            categoriesList.append("[[Category:%s]]" % person)

    (commonsDate, year) = lookForDate(analyse, creationYear)

    (geocat, city) = GeonamesHandlingClass.parseGeoNameField(geoname)
    if isDefined(geocat):
        categoriesList = categoriesList + geocat
    if city is 1:
        place = "Toulouse"
    else:
        place = "France"

    if isDefined(year):
        categoriesList.append(u"[[Category:%s in %s]]" % (year, place))

    if(commonsTechnique is u"stereophotography"):
        categoriesList.append("[[Category:Stereo cards of %s]]" % place)
    if(identifyName(author) is 1):
        categoriesList.append(u"[[Category:Photographs by Eugène Trutat]]")

    sortkey = u"51Fi" + str(id[4:]).rjust(3, '0')
    categoriesList.append(u"[[Category:Fonds Trutat - Archives municipales de Toulouse|%s]]" % sortkey)
    categoriesList.append(u"[[Category:Fonds Trutat - Archives municipales de Toulouse to check|%s]]" % sortkey)
    categories = u'\n'.join(categoriesList)

    def addCatToDictionary(x):
        catR = re.search(r"^\[\[Category:(?P<cat>.+?)(\|.*)?\]\]$", x)
        if catR:
            cat = catR.group('cat')
            if cat in categoriesTable.keys():
                categoriesTable[cat] += 1
            else:
                categoriesTable[cat] = 1
        else:
            print "====Problem"

    map(addCatToDictionary, categoriesList)

    commonsTpl = u"""
{{Artwork
|artist         = %s
|title          = {{fr|%s}}
|description    = %s
|date           = %s
|medium         = %s
|dimensions     = %s
|gallery        = %s
|location       =
|references     =
|object history = %s
|credit line    =
|notes          = %s
|ID             = {{Archives municipales de Toulouse - FET link|%s}}
|source         = {{Fonds Eugène Trutat - Archives municipales de Toulouse}}
|permission     = %s
|other_versions =
|other_fields   =
}}

%s
""" % (commonsAuthor, title, commonsDescription, commonsDate, commonsMedium, commonsDimensions, commonsGallery, creditLine, commonsNotes, id, commonsLicense, categories)

    return (commonsTpl, year)


def handleNode(node, tagName):
    """Returns the contents of a tag based on his given name inside of a given node.
    """
    element = node.getElementsByTagName(tagName)
    if element.length > 0:
        if element.item(0).hasChildNodes():
            return element.item(0).childNodes.item(0).data.rstrip()
    return ""


def massProcess(commonsFileDescriptions, commonsFileNames, localFileNames, upload=False, printInfo=False):
    for num in range(124, 200):
        idToFetch = "51Fi" + str(num)
        if(printInfo):
            printInformation(localFileNames[idToFetch], commonsFileNames[idToFetch], commonsFileDescriptions[idToFetch])
        if(upload):
            uploadToCommons(localFileNames[idToFetch], commonsFileNames[idToFetch], commonsFileDescriptions[idToFetch])
        time.sleep(2)


def main(idToFetch, upload=False, printInfo=False):
    metadataFile = "metadata.XML"
    geonamesFile = "geonames.csv"
    dateFinder = 0
    lameLookUpTables()
    commonsFileDescriptions, commonsFileNames, localFileNames = processMetadataFile(metadataFile, geonamesFile)

    categoriesList = sorted(categoriesTable, key=categoriesTable.get)
    categoriesList.reverse()

    #with codecs.open('categoriesInferred.tex', encoding='utf-8', mode='w') as f:
        #f.write(" \item "+"\n \item ".join(map(lambda x: "\\commonsCatLink{%s} : %s"%(x,categoriesTable[x]),categoriesList)))

    #print reduce(lambda x, y: x+y,categoriesTable.values())

    if(idToFetch is "0"):
        massProcess(commonsFileDescriptions, commonsFileNames, localFileNames, upload, printInfo)
    else:
        if(printInfo):
            printInformation(localFileNames[idToFetch], commonsFileNames[idToFetch], commonsFileDescriptions[idToFetch])
        if(upload):
            uploadToCommons(localFileNames[idToFetch], commonsFileNames[idToFetch], commonsFileDescriptions[idToFetch])


def printInformation(localFileName, commonsFileName, commonsDescription):
    print localFileName
    print commonsFileName
    print commonsDescription


def uploadToCommons(localFileName, commonsFileName, commonsDescription):
    """
    Upload the file with the given name under a given file name and with a given description.
    """
    imagesFolder = "images/"
    imageFullPath = imagesFolder + localFileName
    print "Importing %s to Commons as %s" % (imageFullPath, commonsFileName)
    print commonsDescription
    bot = upload.UploadRobot(
      url=imageFullPath,
      description=commonsDescription,
      useFilename=commonsFileName,
      keepFilename=False,
      verifyDescription=False)
    bot.run()


def lameLookUpTables():
    plop = 11

    global lameGeoTable
    global cityTable
    cityTable = {1: "Toulouse", 2: "France"}

if __name__ == "__main__":
    global dateFinder
    global categoriesTable
    categoriesTable = {}
    dateFinder = 0
    parser = argparse.ArgumentParser(description='Processing Trutat metadata and uploading pictures.')
    parser.add_argument('id', help='the id of the image to display')
    parser.add_argument('--upload', action='store_true', help='whether to upload the picture or not')
    parser.add_argument('--print', dest="printInfo", action='store_true', help='whether to print the info or not')
    args = parser.parse_args()
    main(args.id, args.upload, args.printInfo)
    #massUpload()
