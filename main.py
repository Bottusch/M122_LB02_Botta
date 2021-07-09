import configparser
import os
from generateFile import FileGenerator
from ftplib import FTP
import csv

config = configparser.ConfigParser()
config.read('config.ini')

#connect to ftp
ftp = FTP(config['FTP1']['server'], config['FTP1']['user'], config['FTP1']['pw'])
ftp.cwd(config['FTP1']['ftpPath'])
invoiceData = ''
path = config['LOCALPATHS']['downloadPath']

#get .data file at position 0
filesineed = [filename for filename in ftp.nlst() if '.data' in filename]
if len(filesineed) > 0:
    ftp.retrbinary("RETR " + filesineed[0], open(path+'\\'+filesineed[0], 'wb').write)
    invoiceData = invoiceData+ path+ '\\' + filesineed[0]
    #ftp.delete(filesineed[0])
ftp.quit()
print('Rechnungsdatei wurde heruntergeladen')

#separate csv
def getInvoiceData():
    with open(invoiceData, 'r', encoding="utf-8") as csvFile:
        rows = list(csv.reader(csvFile, delimiter=';'))
        csvFile.close()
        if len(rows) < 4:
            print('CSV Datei ist beschädigt')
        else:
            name = rows[0][0].split('_')
            if 'Rechnung' not in name[0] or len(rows[0]) != 6:
                print('Rechnungsnummer fehlt')
            elif 'Herkunft' not in rows[1][0] or len(rows[1]) != 8:
                print('Herkunft fehlt')
            elif 'Endkunde' not in rows[2][0] or len(rows[2]) != 5:
                print('Endkunde fehlt')
            elif 'RechnPos' not in rows[3][0] or len(rows[3]) != 7:
                print('Rechenposition fehlt')
            else:
                for i in rows:
                    if i[0] == 'RechnPos' and len(i) != 7:
                        print('Rechenposition fehlt')
                return rows

rows = getInvoiceData()
FileGenerator(rows)

ftp2 = FTP(config['FTP2']['server'], config['FTP2']['user'], config['FTP2']['pw'])
ftp2.cwd(config['FTP2']['ftpPath'])
path = config['LOCALPATHS']['uploadPath']
files = os.listdir(path)
for file in files :
    with open(path +'\\'+ file, "rb") as file1 :
        newPath = path + '\\' + file
        ftp2.storbinary('STOR ' + file, file1)
        file1.close()
ftp2.quit()
