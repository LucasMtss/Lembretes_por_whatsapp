from datetime import datetime
import numpy

from sqlalchemy import null
from constants import CREATE_REMINDER_ERROR_MESSAGE, CREATE_REMINDER_SUCCESS_MESSAGE, SEPARATOR
from date import formatDate
from db import db

class Lembrete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
