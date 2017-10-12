import socket
import time

class User:
    eventLog = list()
    eventCounter = 0;
    blockedUsers = dict()
    maxtrixClock = list()
    peers = list()
    userId = 0


    """""
     @param int,list[int],int
    """""
    def __init__(self, userId, peers,amount):
        self.userId = userId
        self.peers = peers
        #Initilize matrixClock to all zero values
        for i in range(0,amount):
            newList = list()
            for j in range(0,amount):
                newList.append(0)
                maxtrixClock.append(newList)
        for i in range(0,len(peers)):
            if(i != userId):
                blockedUsers[i] = "unblock"
    """
    @param tuple,int
        -eventRecord is a tuple containing eventName, message of event, timestamp, userId, and UTC time
    @return
        returns true or false depending on if the receiver has already bene updated with the given event
    """
    def hasRec(eventRecord,receiver):
        return matrixClock[receiver][eventRecord[3]] >= eventRecord[2]

    """""
    @param String, String, int
        -eventName will either be "tweet","block","unblock"
        -message contains a String that consists of the body of a tweet, or an empty
        String for block or unblock
        -time contains the timestamp of the event to be stored
    @modifies
        eventCounter increases by one
        matrixClock is updated at the indices of the userId
        eventLog has a new eventRecord added to it
    @return
        returns a tuple containing the eventName, message of event, timestamp, userId, and UTC time
    """""
    def insert(eventName,message,time):
        eventCounter += 1
        matrixClock[userId][userId] = eventCounter
        eventRecord = (eventName,message,eventCounter,userId,time)
        eventLog.append(eventRecord)
        return eventRecord





    """"
    @param
        message: a message will come in form of a string
    @modifies:
        Will modify matrixClock, eventLog. will send out a message depending
        on what values are not in the blockedUsers list
    @return
        return a list containing all the eventRecords, the tweet event, and
        the matrixClock
    """
    def tweet(message,time,receiver):
        eventRecord = insert("tweet",message,time)
        NP = list()
        for i in range(0,len(eventLog)):
            pastEvent = eventLog[i]
            if(not (hasRec(currentEvent,receiver))):
                NP.append(eventRecord,matrixClock,currentEvent)
        return NP

    def block(time,receiver):
        eventRecord = insert("block","",time)
        ### add truncation code here
        blockedUsers[receiver] = "block"

    def unblock(time,receiver):
        eventRecord = insert("unblock","",time)
        ### add truncation code here
        blockedUsers[receiver] = "unblock"

    def view():
        for i in range(0,len(evenLog)):
            
