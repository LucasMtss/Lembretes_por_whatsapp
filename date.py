from dateutil.parser import *

def validateDate(message):
    message = message.replace("/","-",2)
    res = True
    try:
        res = bool(parser().parse(message))
    except ValueError:
        res = False
    return res

def formatDate(date):
    formatedDate = date.split('-')
    return f'{formatedDate[2]}/{formatedDate[1]}/{formatedDate[0]}'