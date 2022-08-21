
from unidecode import unidecode
from flask import  request
from app import app
import time
from schedule import mySchedule
import numpy


from constants import CREATE_REMINDER_SAMPLE, ERROR_MESSAGE, INFORM_THE_DATE, INITIAL_MESSAGE
from date import validateDate
from reminders import createReminder, findReminders, findRemindersOfToday, formatReminderToCreate
from schedule import remindersOfToday 
from sendMessage import sendMessage
from users import saveUser, searchUser



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
    
    return ERROR_MESSAGE

def checkIfNewReminder(message):
    if numpy.size(message.split("\n")) == 3:
        return True
    else:
        return False


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    user = request.form['From'].split('+')[1]
    saveUser(user)
    response = handleUserMessage(getMessage(request), user)
    senderId = user
    if(response != ERROR_MESSAGE):
        sendMessage(senderId=senderId, message=response)
    else:
        sendMessage(senderId=senderId, message=ERROR_MESSAGE)
        sendMessage(senderId=senderId, message=INITIAL_MESSAGE)
    return '200'

if __name__ == "__main__":
    app.run()

