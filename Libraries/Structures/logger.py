
from Libraries.consts import DATE_TIME

class Logger:
    registered = {}

    def __init__(self):
        self.registered = {}

    def register_log(self, systemName, dateTime, catalog,  continueSyle = False):
        if systemName in self.registered.keys(): return
        if continueSyle :
            self.registered[systemName] = open("logs/" + catalog +"/" + dateTime + " " + systemName , "a")
        else:
            self.registered[systemName] = open("logs/" + catalog +"/" + dateTime + " " + systemName , "w")

    def log(self, systemName, text):
        self.registered[systemName].write( text + "\n" )

LoggerInstance = Logger()