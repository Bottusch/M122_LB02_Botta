import sys
import re

class Row4:
    def __init__(self, line) -> None:
        if 'RechnPos' not in line[0]:
            sys.exit() #TODO after errors
        else :
            self.__line = line
            self.__getValue()

    def __getValue(self) :
        self.billPosNo = self.__billPosNo()
        self.billPosDesc = self.__billPosDesc()
        self.quantity = self.__quantity()
        self.itemPrice = self.__itemPrice()
        self.totalPrice = self.__totalPrice()
        self.mwst = self.__mwst()



    def __billPosNo (self) :
        if len(self.__line[1]) < 1 :
            print('Fehler, Rechnungspositionsnummer fehlt')
        return self.__line[1]

    def __billPosDesc (self) :
        if len(self.__line[2]) < 1 :
            print('Fehler, Rechnungspositionsbezeichnung fehlt')
        return self.__line[2]

    def __quantity (self) :
        if len(self.__line[3]) < 1 :
            print('Fehler, Anzahl/Menge fehlt')
        return self.__line[3]

    def __itemPrice (self) :
        if not '%.2f' %float(self.__line[4]) == self.__line[4] :
            print('Fehler, Preis pro Stück ist falsch formatiert')
        return self.__line[4]

    def __totalPrice (self) :
        calculatedPrice = float(self.__quantity()) * float(self.__itemPrice())
        if not '%.2f' %float(self.__line[5]) == self.__line[5] :
            print('Fehler, Preis pro Stück ist falsch formatiert')
        elif not '%.2f' % calculatedPrice == self.__line[5]:
            print('Fehler, der berechnete Preis stimmt nicht')
        return self.__line[5]

    def __mwst (self) :
        if not re.match('MWST_\d{1}\.\d{2}\%', self.__line[6]) :
            print('Fehler, MwSt ist fehlerhaft')
        return self.__line[6].split('_')[1]