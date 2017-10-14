import socket
import time

class User:
    eventLog = list()
    eventCounter = 0;
    blockedUsers = list()
    maxtrixClock = list()
    peers = list()
    userId = 0


    """""
     This is the constructor for the User class. A User corresponds to a site.
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

    """
    Checks if a matrixClock contains a timestamp larger than what's in the eventRecord.
    @param tuple,int
        -eventRecord is a tuple containing eventName, message of event, timestamp, userId, and UTC time
    @return
        returns true or false depending on if the receiver has already been updated with the given event/
        If true is returned, then, the process knows the most recent event.
        If fals is returned the process does not know the most recent event
    """
    def hasRec(recievedClock,eventRecord,receiver):
        return receivedClock[receiver][eventRecord[3]] >= eventRecord[2]

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
        Will modify matrixClock, eventLog. Will send out a message depending
        on what values are not in the blockedUsers list
    @return
        returns a tuple containg the following:
            [0] -> the sender's userID
            [1] -> the sender's matrixClock
            [2] -> a list containing all the eventRecords
    """
    def tweet(message,time,receiver):
        print "Sending following tweet "+message+" to all unblocked users\n"
        eventRecord = insert("tweet",message,time)
        NP = list()
        for i in range(0,len(eventLog)):
            pastEvent = eventLog[i]
            if(not (hasRec(matrixClock,currentEvent,receiver))):
                NP.append(eventRecord,matrixClock,currentEvent,userID)
        sendBody = ((userID,matrixClock,NP))
        return sendBody

    def block(time,receiver):
        blocked = False
        print "Blocked User "+receiver+"\n"
        eventRecord = insert("block",receiver,time)
        ### add truncation code here for log
        for i in range(0,len(blockedUsers)):
            if(blockedIds[i][0] == userId and blockedIds[i][1] == receiver):
                blocked = True
        if(not (blocked)):
            blockedUsers.append((userId,receiver))

    def unblock(time,receiver):
        print "Unblocked User "+receiver+"\n"
        for i in range(0,len(blockedIds)):
            if(blockedIds[i][0] == userId and blockedIds[i][1] == receiver):
                del blockedUsers[i]
                break
        eventRecord = insert("unblock","",time)


    def view():
        print "View command selected \n"
        for i in range(0,len(eventLog)):
            currentEvent = eventLog[i]
            eventType = currentEvent[0]
            eventCreator =  currentEvent[3]
            if(eventType == "tweet" and blockedUsers[eventCreator] == "unblock"):
                print eventType + "\n"
        eventRecord = insert("view","",time)

    def receive(message,receivedClock,receivedNP):
        sentID = -1
        for k in range(0,len(peers)):
            if(peers[k] == sendAddress):
                siteID = peers[k]
        NE = list()
        for i in range(0,len(receivedNP)):
            pastEvent = receivedNP[i]
            if(not (hasRec(receivedClock,pastEvent,userId))):
                NE.append(pastEvent)

        ##now we truncate the received log before moving forward to insert values into the dictionary

        ##After truncating received log, also must truncate partial log

        #This loop updates the local dictionary depending on what was in the received dictionary
        for i in range(0,len(NE)):
            blockEvent = NE[i][0]
            blockReceiver = NE[i][1]
            receiverId = NE[i][3]
            if(blockEvent == "block"):
                blockedUsers.append((receiverId,blockReceiver))
            if(blockEvent == "unblock"):
                for j in range(0,len(blockedUsers)):
                    if(blockedUsers[j][0] == receiverId and blockedUsers[j][1] == blockReceiver):
                        del blockedUsers[i]
                        break
        #The first item in the received message contains the ID of the sender
        sender = message[0]
        fullUnion = eventLog.merge(NE)

        for k in range(0,len(peers)):
            matrixClock[userId][k] = max(matrixClock[userId][k],receivedClock[sender][k])

        #the combination of k and l will correctly update the matrixClock
        for k in range(0,len(peers)):
            for l in range(0,len(peers)):
                matrixClock[userId][k] = max(matrixClock[k][l],receivedClock[k][l])
            clearedLog = eventLog.clear()
            #the m loop goes through the fullUnion of the partialLog and eventRecord
            #the loop checks for all relevant partialLog options
            for m in range(0,len(fullUnion)):
                currentRecord = NE[m]
                if(not hasRec(matrixClock,currentRecord,k)):
                    clearedLog.append(currentRecord)
        #the eventLog changes to this filled once clearedLog
        eventLog = clearedLog
