from twilio.rest import Client
import sys
sys.path.append('.')
from Database.Database import Database

account_sid = 'AC9bd99fb335724f3ee5789ba55c1fa361'
auth_token = '26ab824d1b179430eda3f227ec6cc534'
twilio_phone = '+12075033620'



def main(data = []):
    for data in data:
        name, body, phonenumber = data['name'], data['dishes'], data['phonenumber']
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_= twilio_phone,
            body=f'Hello {name}, for today\'s menu, you should avoid {body}. Stay healthy!',
            to=phonenumber
            )
        print(message.sid)
        print('message sent succesfully')
        return 0

if __name__ == '__main__':
    sys.exit(main(data = Database()._get_notification_data()))
    