from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

sid=os.environ.get('ACCOUNT_SID')
authToken=os.environ.get('AUTH_TOKEN')
fromNumber=os.environ.get('FROM_NUMBER')
toNumber=os.environ.get('TO_NUMBER')

client = Client(sid, authToken)

def sendMessage(senderId, message):
  response = client.messages.create(from_=fromNumber,  
                                    body=message,      
                                    to=f'whatsapp:+{senderId}')
  return response