from Comms import CommsListener, CommsSender
import sys
import json
import pygame
class Vector2Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pygame.math.Vector2):
            return {"x": obj.x, "y": obj.y}
        return super().default(obj)


class Messenger:
    """
    A Messenger class for multiplayer message passing
    
    Attributes
    ----------
    creds :
        users credentials
    callBack : optional
        Defaults to None
    user :
        user name
    commsListener :
        instance of CommsListener
    commsSender :
        instance of CommsSender

    
    Methods
    -------
    send(target, body)
        Send message from user to another user
    setCallback(callBack)
        sets the callback function for the messenger
    """
    def __init__(self, creds, callback=None):
        """
        Parameters
        ----------
            creds : 
                users credentials
            callback : optional
                Defaults to None
        """
        self.creds = creds
        self.callBack = callback

        if not self.creds:
            print(
                "Error: Message handler needs `creds` or credentials to log into rabbitmq. "
            )
            sys.exit()

        if self.callBack != None:
            # Start the comms listener to listen for incoming messages
            self.commsListener.threadedListen(self.callBack)

        self.user = self.creds["user"]

        # create instances of a comms listener and sender
        # to handle message passing.
        self.commsListener = CommsListener(**self.creds)
        self.commsSender = CommsSender(**self.creds)

    def send(self, target, body):
        """
        Send message from user to another user
        
        Parameters
        ----------
            target : 
            body : json
        """
        self.commsSender.send(
            target=target, sender=self.user, body=json.dumps(body,cls=Vector2Encoder), closeConnection=False
        )

    def setCallback(self, callBack):
        """
        sets the callback function for the messenger
        Args:
            callBack : 
        """
        self.callBack = callBack
        self.commsListener.threadedListen(self.callBack)
