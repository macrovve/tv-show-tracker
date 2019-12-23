import json

# import requests
import boto3

def lambda_handler(event, context):
    event = event
    email = event['email']

    input_passcode = event['passcode']

    isCorrect = input_passcode == db_search(email)

    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": str(isCorrect),
            # "location": ip.text.replace("\n", "")
        }),
    }


def db_search(email):
    email = email

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    visitors = dynamodb.Table('project-user-info')

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    print(visitors.creation_date_time)
    #
    # visitors.putItem(item={
    # 'faceId': faceId,
    # 'name': name,
    # 'phoneNumber': phoneNumber,
    # 'photos': photos
    # })

    response = visitors.get_item(
        Key={
            'email': email
        }
    )
    try:
        # print(response)
        item = response['Item']['passcode']
    except:
        print("error")
        raise ValueError

    if (response == []):
        return "error"
    else:
        item = response['Item']['passcode']
        # print(item)
        return item

event={"email":"abcd@qq.com",
      "passcode":"123"}
lambda_handler(event, "1")