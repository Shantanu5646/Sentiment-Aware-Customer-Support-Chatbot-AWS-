import json
import boto3
#NEW
from datetime import datetime
#END

# Use default credentials attached to Lambda role (no hardcoding)
comprehend = boto3.client('comprehend', region_name='us-east-1')

#NEW
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerFeedback')
#END

def validate(slots):
    # Safely extract the 'Starting' slot value
    starting = slots['Starting']['value']['interpretedValue'] if slots.get('Starting') and slots['Starting'].get('value') else None

    # Case 1: Handle "Review and Feedback" scenario
    if starting == 'Review and Feedback':
        feedback = slots.get('FeedBackText')
        if not feedback or not feedback.get('value') or not feedback['value'].get('interpretedValue'):
            return {
                'isValid': False,
                'violatedSlot': 'FeedBackText'
            }
        return {'isValid': True}

    # Case 2: Handle all other issues (Payment, Delivery, etc.)
    required_slots = ['ProductID', 'FirstName', 'LastName', 'Date', 'ZIP']
    for slot in required_slots:
        if not slots.get(slot) or not slots[slot].get('value') or not slots[slot]['value'].get('interpretedValue'):
            return {
                'isValid': False,
                'violatedSlot': slot
            }

    return {'isValid': True}

def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    source = event['invocationSource']

    # Debug print statements
    print("Invocation Source:", source)
    print("Intent:", intent)
    print("Slots:", slots)
    print("FEEDBACK SLOT RAW:", slots.get('FeedBackText'))

    if source == 'DialogCodeHook':
        validation_result = validate(slots)
        if not validation_result['isValid']:
            return {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name': intent,
                    'slots': slots
                }
            }
        }

    # Fulfillment section
    elif source == 'FulfillmentCodeHook':
        starting = slots['Starting']['value']['interpretedValue'] if slots.get('Starting') and slots['Starting'].get('value') else None

        print("STARTING:", starting)
        print("FEEDBACK TEXT SLOT:", slots.get('FeedBackText'))

        #NEW
        table.put_item(
            Item={
                'IssueType': starting, 
                'ProductID': slots['ProductID']['value']['interpretedValue'],
                'FirstName': slots['FirstName']['value']['interpretedValue'],
                'LastName': slots['LastName']['value']['interpretedValue'],
                'Date': slots['Date']['value']['interpretedValue'],
                'ZIP': slots['ZIP']['value']['interpretedValue'],
                'Feedback': '-',
                'Sentiment': '-',
                'Timestamp': datetime.utcnow().isoformat()  # Optional: for sorting later
            }
        )
        #END
    
        message = "Thank you, I have raised your complaint."

        if starting == 'Review and Feedback':

            print(">>> Inside FulfillmentCodeHook for Review and Feedback")

            feedback_text = slots['FeedBackText']['value']['interpretedValue']
            sentiment_response = comprehend.detect_sentiment(Text=feedback_text,LanguageCode='en')
            print("Sentiment Response:", sentiment_response)

            sentiment = sentiment_response['Sentiment']
            #NEW
            table.put_item(
                Item={
                    'IssueType': starting, 
                    'ProductID': slots['ProductID']['value']['interpretedValue'],
                    'FirstName': slots['FirstName']['value']['interpretedValue'],
                    'LastName': slots['LastName']['value']['interpretedValue'],
                    'Date': slots['Date']['value']['interpretedValue'],
                    'ZIP': slots['ZIP']['value']['interpretedValue'],
                    'Feedback': feedback_text,
                    'Sentiment': sentiment,
                    'Timestamp': datetime.utcnow().isoformat()  # Optional: for sorting later
                }
            )
            #END
            message = f"Thank you for your feedback! We detected that you're feeling {sentiment.lower()}."

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name': intent,
                    'slots': slots,
                    'state': 'Fulfilled'
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": message
                }
            ]
        }