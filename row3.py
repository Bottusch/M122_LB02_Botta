import sys
import re

class Row3:
    def __init__(self, line) -> None:
        if 'Endkunde' not in line[0]:
            sys.exit() #TODO after errors
        else :
            self.__line = line
            self.__getValue()

    def __getValue(self) :
        self.customerID = self.__customerID()
        self.name = self.__name()
        self.address = self.__address()
        self.zip = self.__zip()





    def __customerID (self) :
        if not re.match(r'\d{17}', self.__line[1]) :
            print('Fehler, Kundennummer hat falsches Format')
        return self.__line[1]

    def __name (self) :
        if len(self.__line[2]) < 1 :
            print('Fehler, Name fehlt')
        return self.__line[2]

    def __address (self) :
        if len(self.__line[3]) < 1 :
            print('Fehler, Adresse fehlt')
        return self.__line[3]

    def __zip (self) :
        if len(self.__line[4]) < 1 :
            print('Fehler, PLZ fehlt')
        return self.__line[4]