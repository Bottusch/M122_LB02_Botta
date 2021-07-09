from row4 import Row4

def totalPriceTxt(lines) :
    totalPrice = 0.00
    for line in lines :
        if line[0] == 'RechnPos' :
            price = Row4(line)
            totalPrice = totalPrice + float(price.totalPrice)
    return '%.2f' % totalPrice

def totalPriceTxtWthSpc(lines) :
    totalPrice = 0.00
    for line in lines :
        if line[0] == 'RechnPos' :
            price = Row4(line)
            totalPrice = totalPrice + float(price.totalPrice)
    price2 =str('%.2f' % totalPrice)
    p = price2.split('.')
    return p[0] + ' . ' + p[1]

def totalPriceXml(lines) :
    totalPrice = 0.00
    for line in lines :
        if line[0] == 'RechnPos' : 
            price = Row4(line)
            totalPrice = totalPrice + float(price.totalPrice)
    total = '%.2f' %totalPrice
    price = ''.join(total.split('.'))
    return price.zfill(10)