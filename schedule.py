
import datetime
import pytz

from scheduler import Scheduler
from reminders import findRemindersOfToday

from sendMessage import sendMessage
from users import searchAllUsers



def remindersOfToday():
  users = searchAllUsers()
  for user in users:
    message = findRemindersOfToday(user['user'])
    sendMessage(user['user'], message)

TZ_SERVER = datetime.timezone.utc  # can be any valid timezone
TZ_SAO_PAULO = pytz.timezone('America/Sao_Paulo') 
mySchedule = Scheduler(tzinfo=TZ_SERVER)
trigger_sp = datetime.time(hour=11, minute=30, tzinfo=TZ_SAO_PAULO)

mySchedule.daily(trigger_sp, remindersOfToday, args=(TZ_SAO_PAULO))