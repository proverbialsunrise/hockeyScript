#!/usr/local/bin/python2.7

import xml.etree.ElementTree as ET
import urllib2
import os
import pdb
import pyperclip

class Game:
    """ holds data about a game

    Attributes
        homeTeamName:
        awayTeamName:
        homeTeamID:
        awayTeamID:
        homeTeamStream:
        awayTeamStream:
    """
    def __init__(self, homeTeamName, awayTeamName):
        self.homeTeamName = homeTeamName
        self.awayTeamName = awayTeamName
        self.homeTeamID = ""
        self.homeTeamStream = ""
        self.awayTeamID = ""
        self.awayTeamStream = ""

    def printOut(self):
        print self.homeTeamName.capitalize() + " vs. " + self.awayTeamName.capitalize()
        print self.homeTeamID + ": " + self.homeTeamStream
        print self.awayTeamID + ": " + self.awayTeamStream

    def description(self):
        return self.homeTeamName.capitalize() + " vs. " + self.awayTeamName.capitalize()

    def printStreams(self):
        print "(1)  " + self.homeTeamID + ": " + self.homeTeamStream
        print "(2)  " + self.awayTeamID + ": " + self.awayTeamStream


def parseFeed(xml_string):
    gamesXML = ET.fromstring(xml_string);
    games = []
    for gameXML in gamesXML: 
        homeTeamName =  gameXML.find('home_teamname').text
        awayTeamName = gameXML.find('away_teamname').text 

        game = Game(homeTeamName, awayTeamName)
        #print homeTeamName.capitalize() + " vs. " + awayTeamName.capitalize()

        assignments = gameXML.find('assignments')
        feeds = assignments.findall('assignment')
        homeFeed = feeds[0]
        game.homeTeamID = homeFeed.find('team_id').text
        game.homeTeamStream = homeFeed.find('ipad_url').text
        

        awayFeed = feeds[1]
        game.awayTeamID = awayFeed.find('team_id').text
        game.awayTeamStream = awayFeed.find('ipad_url').text

        #print teamName + ": " + feedURL

        games.append(game)

    return games
            

        

feedURL = "http://208.92.36.37/nlds/as3/get_games.php?client=nhl&playerclient=hop"
req = urllib2.Request(feedURL)
f = urllib2.urlopen(req)
xml_string = f.read()
games = parseFeed(xml_string)

print ""
i = 1
for game in games:
    print "Game " + str(i) 
    print "----------------------------"
    print game.description()
    print ""
    i += 1


gameNum = int(raw_input("Select a game number... ")) - 1 

game = games[gameNum]

print "Selected " + game.description()

print "Available Streams:"
game.printStreams() 


streamNum = int(raw_input("Select a stream number... ")) 

if streamNum == 1:
    selectedStream = game.homeTeamStream
else:
    selectedStream = game.awayTeamStream

pyperclip.copy(selectedStream)
print "Copied " + selectedStream + " to clipboard."
