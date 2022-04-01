import json
import boto3
from botocore.exceptions import ClientError

# Replace the sender@example.com with the "From" address emails should come from.  Must be verified by AWS SES
SENDER = "my_email_address@example.com"

# Replace the AWS_REGION with the region you've deployed SES to
AWS_REGION = "us-east-1"

# Character encoding for the email
CHARSET = 'UTF-8'

def lambda_handler(event, context):
    print("Received event object: {}".format(event))
    
    # Retrieve the email from the signup form and send a notification via SES
    try:
        # Check and ensure that an "email" address was passed in to this function
        if 'email' not in event:
            raise KeyError("No email provided in event object, aborting...")
        email = event['email']
        
        # Create a "subject" variable which will be the subject line of the welcome email
        subject = "FILL IN THIS SECTION WITH THE CONTENT YOU WANT IN THE SUBJECT LINE OF YOUR WELCOME EMAIL"
        
        # Create the HTML string that will populate the "body" of the email
        body_html = """
            <html>
                <head></head>
                <body>
                    FILL IN THIS SECTION WITH THE CONTENT YOU WANT IN THE BODY OF YOUR WELCOME EMAIL
                </body>
            </html>
        """

        # Backup string in case the email client doesn't support HTML for emails (unlikely)
        body_text = """
            If your email client doesn't support HTML (unlikely) the body of your welcome email needs to be a simple
            text string.  You can think of this as a "backup" in case you can't send the HTML version of your welcome email
        """

        # Send the email using the send_email() function and note the response
        response = send_email(subject=subject, email_body_html=body_html, email_body_text=body_text, recipient=email)
        
        # If we get here, we can return a "success" response of HTTP.status_code = 200
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "isBase64Encoded": False,
            "body": json.dumps({
                "result": "Email send success!",
                "messageId": response['MessageId'],
                'requestId': context.aws_request_id
            })
        }
    except KeyError as e:
        raise Exception("No data field present in event object")
    except ClientError as e:
        print(e.response['Error']['Message'])
        raise Exception("Failed to send the notification email to {}".format(email))

# Function to send the welcome email
def send_email(subject, email_body_html, email_body_text, recipient):
    client = boto3.client('ses', region_name=AWS_REGION)
    response = client.send_email(
        Destination = {
            'ToAddresses': [
                recipient,    
            ],
        },
        Message= {
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': email_body_html,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': (email_body_text),
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': subject,
            },
        },
        Source=SENDER
    )
    return response