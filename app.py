from pyexpat.errors import messages
from timeit import repeat
from sqlalchemy import null, true
from unidecode import unidecode
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import numpy
from dateutil.parser import *
import os
from dotenv import load_dotenv
from sendMessage import sendMessage
from datetime import datetime

# MENSAGENS
INITIAL_MESSAGE = """Olá, em que posso ajudá-lo?
[1] Verificar lembretes de hoje
[2] Verificar lembretes de outro dia
[3] Adicionar lembrete
"""
ERROR_MESSAGE = 'Desculpe, não consegui entender o que você digitou :('
CREATE_REMINDER_ERROR_MESSAGE = 'Desculpe, não foi possível criar o lembrete :('
CREATE_REMINDER_SUCCESS_MESSAGE = 'Lembrete criado com sucesso!!'
SEPARATOR='\n--------------------------------------------------------------------\n\n'
INFORM_THE_DATE='Informe a data: (dd/mm/aaaa)'
CREATE_REMINDER_SAMPLE="""Por favor, informe seu lembrete no seguinte formato:

Dia: dd/mm/aaaa
Hora: HH:mm
Lembrete: 'Lembrar de...'
"""

load_dotenv()

dbName=os.environ.get('DB_NAME')
dbHost=os.environ.get('DB_HOST')
dbUser=os.environ.get('DB_USER')
dbPassword=os.environ.get('DB_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{dbUser}:{dbPassword}@{dbHost}/{dbName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_POOL_PRE_PING'] = True

db = SQLAlchemy(app)

class Lembrete(db.Model):
    id = db.Column(db.Integer, primary_key=true)
    user = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.String(5), nullable=False)
    notes = db.Column(db.String(100))
    active = db.Column(db.Boolean(), nullable=False)
    repeat = db.Column(db.String(15))

    def toJson(self):
        return {
            "id": self.id,
            "user": self.user,
            "date": self.date,
            "hour": self.hour,
            "notes": self.notes,
            "active": self.active,
            "repeat": self.repeat,
        }

def formatRemindersForMessage(reminders, date):
    if(numpy.size(reminders) == 0):
        return f'Você não tem lembretes para o dia {date}'

    message = f"LEMBRETES DO DIA {date}\n\n"
    for reminder in reminders:
        message = message + f"{reminder['hour']}h"
        message = message + ' - '
        message = message + reminder['notes'] 
        message = message + SEPARATOR
    return message

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

def findRemindersOfToday(user):
    today = f'{datetime.today()}'
    today = today[:10]
    return findReminders(formatDate(today), user)

def findReminders(date, user):
    reminders = Lembrete.query.filter_by(date=date, user=user)
    response = [reminder.toJson() for reminder in reminders]
    return formatRemindersForMessage(response, date)

def formatReminderToCreate(message, user):
    splitMessage = message.split("\n")
    newReminder = null
    newReminder.date = splitMessage[0]
    newReminder.user = user
    newReminder.hour = splitMessage[1]
    newReminder.notes = splitMessage[2]
    newReminder.active = True
    newReminder.repeat = ''
    return newReminder

def createReminder(reminder):
    try:
        newReminder = Lembrete(
            user=reminder.user,
            date=reminder.date,
            hour=reminder.hour,
            notes=reminder.notes,
            active=reminder.active,
            repeat=reminder.repeat
            )
        db.session.add(newReminder)
        db.session.commit()
        return CREATE_REMINDER_SUCCESS_MESSAGE
    except Exception as error:
        print('ERROR', error)
        return CREATE_REMINDER_ERROR_MESSAGE

def getMessage(request):
    return request.form['Body']

def handleUserMessage(message, user):
    formatedMessage = unidecode(message.lower())
    if formatedMessage == 'ola':
        return INITIAL_MESSAGE
    if formatedMessage == '1':
        return findRemindersOfToday(user)
    if formatedMessage == '2':
        return INFORM_THE_DATE
    if formatedMessage == '3':
        return CREATE_REMINDER_SAMPLE
    if checkIfNewReminder(formatedMessage) == True:
        reminder = formatReminderToCreate(message, user)
        response = createReminder(reminder)
        return response
    if validateDate(message) == True:
        res = findReminders(message, user)
        return res
    else:
        return ERROR_MESSAGE

def checkIfNewReminder(message):
    if numpy.size(message.split("\n")) == 3:
        return True
    else:
        return False

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    user = request.form['From'].split('+')[1]
    response = handleUserMessage(getMessage(request), user)
    if(response != ERROR_MESSAGE):
        senderId = user
        sendMessage(senderId=senderId, message=response)
    else:
        sendMessage(senderId=senderId, message=ERROR_MESSAGE)
        sendMessage(senderId=senderId, message=INITIAL_MESSAGE)
    return '200'

if __name__ == "__main__":
    app.run()