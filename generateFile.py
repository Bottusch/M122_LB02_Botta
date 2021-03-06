from row4 import Row4
from helper import totalPriceXml
from helper import totalPriceTxt
from helper import totalPriceTxtWthSpc
from row1 import Row1
from row2 import Row2
from row3 import Row3
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class FileGenerator() :
    def __init__(self, lines) -> None :
        self.__lines = lines
        self.txt = self.__genTxtFile()
        self.__xmlFile = self.__openXmlFile()
        self.xml = self.__genXmlFile()
        

    def __genTxtFile(self) :
        l1 = Row1(self.__lines[0])
        l2 = Row2(self.__lines[1])
        l3 = Row3(self.__lines[2])
        fileName = l2.customerID + '_' + l1.invoiceNr + '_invoice.txt'
        listOfItems = []
        for line in self.__lines :
            if line[0] == 'RechnPos' :
                listOfItems.append(line)

        source = l1.city + ', den ' + l1.date
        txt = [''] * 65
        txt[4] = l2.name
        txt[5] = l2.address
        txt[6] = l2.zip
        txt[8] = l2.taxID
        txt[13] = '{:<48s}{:<}'.format(source, l3.name)
        txt[14] = '{:<48s}{:<}'.format('', l3.address)
        txt[15] = '{:<48s}{:<}'.format('', l3.zip)
        txt[17] = '{:<16s}{:>8}'.format('Kundennummer:', l2.customerID)
        txt[18] = '{:<16s}{:>8}'.format('Auftragsnummer:', l1.orderNr)
        txt[20] = '{:<16s}{:>8}'.format('Rechnung Nr:', l1.invoiceNr)
        txt[21] = '------------------------'
        for item in listOfItems:
            i = Row4(item)
            txt[21 + int(i.billPosNo)] = '{:4s}{:<4s}{:<44s}{:<4s}{:>11s}{:<5s}{:>11s}{:>7}'.format(
                '', i.billPosNo, i.billPosDesc, i.quantity, i.itemPrice, '  CHF', i.totalPrice, i.mwst)
        txt[22 + len(listOfItems)] = '{:>83}'.format('-----------')
        txt[23 + len(listOfItems)] = '{:>68}{:>15}'.format(
            'Total CHF', totalPriceTxt(self.__lines))
        txt[25 + len(listOfItems)] = '{:>68}{:>15}'.format('Mwst  CHF', '0.00')
        txt[44] = 'Zahlungsziel ohne Abzug {} Tage ({})'.format(
            l1.daysTillPay, l1.calculateDueDate)
        txt[46] = 'Einzahlungsschein'
        txt[58] = '{:>13s}{:>29s}{:<5s}{:<}'.format(totalPriceTxtWthSpc(
            self.__lines), totalPriceTxtWthSpc(self.__lines), '', l3.name)
        txt[59] = '{:<47}{}'.format('', l3.address)
        txt[60] = '{:<47}{}'.format('0 00000 00000 00000', l3.zip)
        txt[62] = l3.name
        txt[63] = l3.address
        txt[64] = l3.zip
        try:
            with open(config['LOCALPATHS']['uploadPath'] + '\\'+ fileName, 'w', encoding='utf-8') as file:
                file.write('\n'.join(txt))
                file.close()
            print('TXT Rechnung wurde erstellt')
        except:
            print('TXT Rechnung konnte nicht erstellt werden')

    def __openXmlFile(self) :
        with open('invoice.xml') as file :
            string = file.read()
            file.close()
        return string

    def __genXmlFile(self) :
        l1 = Row1(self.__lines[0])
        l2 = Row2(self.__lines[1])
        l3 = Row3(self.__lines[2])
        fileName = l2.customerID + '_' + l1.invoiceNr + '_invoice.xml'
        xmlFile = self.__xmlFile % ( 
            l2.partyID, 
            l3.customerID,
            l1.dateTimeStamp,
            l1.dateStamp,
            l1.dateStamp,
            l1.invoiceNr,
            l1.dateStamp,
            l1.orderNr,
            l1.dateStamp,
            l1.dateStamp,
            l2.customerID,
            l2.partyID,
            l2.name,
            l2.address,
            l2.zip,
            l3.customerID,
            l3.name,
            l3.address,
            l3.zip,
            totalPriceXml(self.__lines),
            l1.daysTillPay,
            l1.dueDateStamp
        )
        try:
            with open(config['LOCALPATHS']['uploadPath'] + '\\'+ fileName, 'w', encoding='utf-8') as file:
                file.write(xmlFile)
                file.close()
            print('XML Rechnung wurde erstellt')
        except:
            print('XML Rechnung konnte nicht erstellt werden')

    