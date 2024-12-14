from orangeSMS import OrangeSMSAPI


client_id = "<your_client_id>"
client_secret = "<your_client_secret_code>"

api = OrangeSMSAPI(client_id, client_secret)

try:
    token = api.get_token()
    print("Access Token:", token)

    sender = "+224611"
    receiver = "+224611"
    message = "Salam from Guinea"

    response = api.send_sms(sender, receiver, message)
    print("SMS Response:", response)


    stats = api.get_usage_stats()
    print("Usage Stats:", stats)

    balance = api.show_balance_sms()
    print("SMS Balance:", balance)

except Exception as e:
    print("Error:", str(e))
