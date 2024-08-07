from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)

@app.route('/trigger-call', methods=['GET', 'POST'])
def trigger_call():
    account_sid = 'AC14b35aff9e7a031a8d29c138b9177e9d'
    auth_token = '767af8faf053705f8bbb35e4476f156c'
    client = Client(account_sid, auth_token)

    # List of numbers to call
    numbers_to_call = ['+919762477209', '+918624992332']
    call_sids = []  # To store Call SIDs

    for number in numbers_to_call:
        call = client.calls.create(
                            twiml='<Response><Say>Change Alert message here</Say></Response>',
                            to=number,
                            from_='+15735312558'
                        )
        call_sids.append(call.sid)

    # Joining all the Call SIDs to return in response
    call_sids_str = ', '.join(call_sids)
    return f"Call initiated with SIDs: {call_sids_str}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)