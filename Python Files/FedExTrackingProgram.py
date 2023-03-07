import requests
import csv
from dotenv import load_dotenv
import os


#Function to get authorization 
def getBearerAuthorization():
    url= "https://apis-sandbox.fedex.com/oauth/token"

    #Load client_secret
    load_dotenv()
    client_secret = os.getenv('client_secret')
    payload = 'grant_type=client_credentials&client_id=l77df5e3df47214580970dded26bb3e652&client_secret='+client_secret
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    authorization = (response.json()['access_token'])

    return authorization


#Variables and Parameters 
token = getBearerAuthorization()
url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"
text = open('1. Tracking Numbers.txt',"r")
output=open('3. Tracking Results.csv',"w")
writer=csv.writer(output, lineterminator = '\n')
writer.writerow(['Tracking Number', 'Delivery Status', ' Recieved By', 'Date of Latest Scan'])

#complete API request
while True:

    trackingNumber = text.readline()

    if not trackingNumber:
        break
    
    headers = {
        'content-Type': "application/json",
        'authorization': "Bearer "+token
        }
    
    payload = '{ "trackingInfo": [ { "trackingNumberInfo": { "trackingNumber": "'+trackingNumber.strip()+'" } } ], "includeDetailedScans": true }'

    response = requests.post(url, data= payload, headers=headers)


    print(trackingNumber)

    trackingNumber = response.json()['output']['completeTrackResults'][0]['trackingNumber']
    deliveryStatus = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['description']
    if deliveryStatus == "Delivered":
        recievedByName = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['deliveryDetails']['receivedByName']
        scanEvent = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['scanEvents'][0]
        dateDelivered = scanEvent['date'][0:10]
    else:
        recievedByName=""
        dateDelivered=""

    writer.writerow([trackingNumber,deliveryStatus,recievedByName,dateDelivered])


    
text.close()
output.close()