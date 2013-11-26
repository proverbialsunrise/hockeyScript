#!/usr/local/bin/python2.7

import urllib2
import pdb
import pyperclip
import json
import datetime
import time


class Game:
    """ holds data about a game

    Attributes
        date:
        gameID:
        homeTeamID:
        awayTeamID:
        homeTeamStream:
        awayTeamStream:
    """
   
    def __init__(self, homeTeamID, awayTeamID):
        self.homeTeamID = homeTeamID
        self.awayTeamID = awayTeamID
        

    def printOut(self):
        print self.homeTeamID + " vs. " + self.awayTeamID
        print self.homeTeamID + ": " + self.homeTeamStream
        print self.awayTeamID + ": " + self.awayTeamStream

    def description(self):
        return time.strftime("%d/%m/%Y %H:%M:%S", self.date) + ": " +  self.homeTeamID + " vs. " + self.awayTeamID + " " + str(self.gameID)

    def printStreams(self):
        print "(1)  " + self.homeTeamID + ": " + self.homeTeamStream
        print "(2)  " + self.awayTeamID + ": " + self.awayTeamStream


def addStreamsToGame(game):
    ID1 = str(game.gameID)[4:6]
    ID2 = str(game.gameID)[6:11]
    jsonURL = "http://smb.cdnak.neulion.com/fs/nhl/mobile/feed_new/data/streams/2013/ipad/" + ID1 + "_" + ID2 + ".json"
    req = urllib2.Request(jsonURL)
    f = urllib2.urlopen(req)
    streamObj = json.loads(f.read())
    game.homeTeamStream = streamObj["gameStreams"]["ipad"]["home"]["live"]["bitrate0"]
    game.awayTeamStream = streamObj["gameStreams"]["ipad"]["away"]["live"]["bitrate0"]

def gameFromJSON(gameJSON):
    game = Game(gameJSON['h'], gameJSON['a'])
    game.date = time.strptime(gameJSON['est'], "%Y%m%d %H:%M:%S")
    game.gameID = gameJSON['id']
    return game


def getAllGames(scheduleURL):
    req = urllib2.Request(scheduleURL)
    f = urllib2.urlopen(req)
    jsonSchedule = f.read()
    gameList = json.loads(jsonSchedule)
    games = []
    for gameJSON in gameList:
        games.append(gameFromJSON(gameJSON))
   
    return games

def getGames(scheduleURL, checkTime):
    allGames=getAllGames(scheduleURL)
    margin = datetime.timedelta(hours = 12) 
    
    todayGames = []
    for game in allGames:
        gameDT = datetime.datetime.fromtimestamp(time.mktime(game.date))
        if checkTime - margin <= gameDT <= checkTime + margin:
            try:
                addStreamsToGame(game)
                todayGames.append(game)
            except KeyError:
                continue

    return todayGames
  
'''all_names = {
        BOS : "Boston Bruins",
        BUF : "Buffalo Sabres",
        CGY : "Calgary Flames",
        CHI : "Chicago Blackhawks",
        DET : "Detroit Red Wings",
        EDM : "Edmonton Oilers",
        CAR : "Carolina Hurricanes",
        LAK : "Los Angeles Kings",
        MTL : "Montreal Canadiens",
        DAL : "Dallas Stars",
        NJD : "New Jersey Devils",
        NYI : "New York Islanders",
        NYR : "New York Rangers",
        PHI : "Philadelphia Flyers",
        PIT : "Pittsburgh Penguins",
        COL : "Colorado Avalanche",
        STL : "St. Louis Blues",
        TOR : "Toronto Maple Leafs",
        VAN : "Vancouver Canucks",
        WSH : "Washington Capitals",
        PHX : "Phoenix Coyotes",
        SJS : "San Jose Sharks",
        OTT : "Ottawa Senators",
        TBL : "Tampa Bay Lightning",
        ANA : "Anaheim Ducks",
        FLA : "Florida Panthers",
        CBJ : "Columbus Blue Jackets",
        MIN : "Minnesota Wild",
        NSH : "Nashville Predators",
        WPG : "Winnipeg Jets"
    }
'''
scheduleURL = "http://live.nhl.com/GameData/SeasonSchedule-20132014.json"

checkTime = datetime.datetime.now()

games = getGames(scheduleURL, checkTime)

pdb.set_trace()


print ""
i = 1
for game in games:
    print "Game " + str(i) + "   ---   " + game.description()
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



