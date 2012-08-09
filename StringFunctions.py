# -*- coding: utf-8 -*-
"""
Eugene Trutat partnership between Wikimedia France and the City archives of Toulouse
"""
__authors__ = 'User:Jean-Frédéric'


def removeBadCharacters(string, blackList):
    """Removes from a given string all the characters from a given list.
    """
    for character in blackList:
        string = string.replace(character, u'')
    return string


def startsWithOneFromList(word, list):
    """Predicate which tests if at least one element of a given list begins with a given word.
    """
    for item in list:
        if word.startswith(item):
            return True
    return False


def capitalizeFirst(word):
    """Return a given word with its first letter capitalized.
    """
    return word[0].upper() + word[1:]


def capitalizePlace(place):
    """Return the given string capitalised based on rules.
    It first splits the string based on a hardcoded separator list and capitalises each substring.
    """
    separatorList = ['\'', '-', ' ']
    for separator in separatorList:
        place = capitalizePlacePartial(place, separator)
    return place


def capitalizePlacePartial(place, separator):
    """Capitalise a single word.
    """
    capitalizeBlackList = [u"de", u"du", u"l'", u"d'", u"sur", u"la", u"le"]
    placeSplit = place.split(separator)
    placeSplitNew = [placeSplit[0]]
    if len(placeSplit) > 1:
        for word in placeSplit[1:]:
            if startsWithOneFromList(word, capitalizeBlackList):
                placeSplitNew.append(word)
            else:
                placeSplitNew.append(capitalizeFirst(word))
    placeNew = separator.join(placeSplitNew)
    return placeNew
