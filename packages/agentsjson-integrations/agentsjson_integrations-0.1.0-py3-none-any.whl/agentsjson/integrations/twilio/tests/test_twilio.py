from agentsjson.core.executor import execute
from agentsjson.core.models.schema import Flow, Link, Action
from agentsjson.core.models.auth import AuthType, BasicAuthConfig, UserPassCredentials
import argparse
import os
from typing import Callable, Dict

# Default test phone numbers
FROM_NUMBER = "+18665940570"  # Your Twilio phone number
TO_NUMBER = "+18777804236"    # Your verified number to test with

def get_auth_config(account_sid: str, auth_token: str) -> BasicAuthConfig:
    """Create auth config from credentials."""
    return BasicAuthConfig(
        type=AuthType.BASIC,
        credentials=UserPassCredentials(
            username=account_sid,
            password=auth_token,
            base64_encode=False
        )
    )

def test_list_available_numbers(auth: BasicAuthConfig):
    """Safe test that only lists available numbers without purchasing."""
    list_numbers_chain = Flow(
        id="list_numbers",
        name="List Available Numbers",
        displayName="List Available US Numbers",
        description="Lists available phone numbers in the US",
        fields={
            "parameters": [
                {"fieldName": "CountryCode"},
                {"fieldName": "SmsEnabled"},
                {"fieldName": "MmsEnabled"},
                {"fieldName": "AreaCode"}
            ],
            "requestBody": []
        },
        order=[
            Action(
                id="search_numbers",
                apiName="twilio",
                operationId="twilio_list_available_phone_number_local"
            )
        ],
        links=[
            Link(
                origin={"id": "list_numbers", "fieldType": "parameters", "fieldName": "CountryCode"},
                target={"id": "search_numbers", "fieldType": "parameters", "fieldName": "CountryCode"}
            ),
            Link(
                origin={"id": "list_numbers", "fieldType": "parameters", "fieldName": "SmsEnabled"},
                target={"id": "search_numbers", "fieldType": "parameters", "fieldName": "SmsEnabled"}
            ),
            Link(
                origin={"id": "list_numbers", "fieldType": "parameters", "fieldName": "MmsEnabled"},
                target={"id": "search_numbers", "fieldType": "parameters", "fieldName": "MmsEnabled"}
            ),
            Link(
                origin={"id": "list_numbers", "fieldType": "parameters", "fieldName": "AreaCode"},
                target={"id": "search_numbers", "fieldType": "parameters", "fieldName": "AreaCode"}
            )
        ]
    )
    
    # Execute search for available numbers
    list_result = execute(
        list_numbers_chain,
        auth,
        parameters={
            "CountryCode": "US",
            "SmsEnabled": True,
            "MmsEnabled": True,
            "AreaCode": "415"  # San Francisco area code
        },
        requestBody={}
    )
    print(f"List result: {list_result}")
    
    if not list_result or len(list_result) == 0:
        print("No available numbers found")
        return None
    
    print("\nAvailable numbers:")
    for number in list_result[:5]:  # Show first 5 numbers
        print(f"- {number['phone_number']}")
    
    return list_result[0]["phone_number"] if list_result else None

def test_phone_number_purchase_workflow(auth: BasicAuthConfig):
    """
    WARNING: This test will actually purchase a phone number!
    Only run this when you intend to buy a new number.
    """
    # Step 1: List and select a number
    available_number = test_list_available_numbers(auth)
    if not available_number:
        return
    
    print(f"\nProceeding to purchase number: {available_number}")
    
    # Step 2: Purchase the phone number
    purchase_chain = Flow(
        id="purchase_number",
        name="Purchase Number",
        displayName="Purchase Phone Number",
        description="Purchases a Twilio phone number",
        fields={
            "parameters": [
                {"fieldName": "PhoneNumber"},
                {"fieldName": "SmsUrl"},
                {"fieldName": "SmsMethod"}
            ],
            "requestBody": []
        },
        order=[
            Action(
                id="buy_number",
                apiName="twilio",
                operationId="twilio_create_incoming_phone_number"
            )
        ],
        links=[
            Link(
                origin={"id": "purchase_number", "fieldType": "parameters", "fieldName": "PhoneNumber"},
                target={"id": "buy_number", "fieldType": "parameters", "fieldName": "PhoneNumber"}
            ),
            Link(
                origin={"id": "purchase_number", "fieldType": "parameters", "fieldName": "SmsUrl"},
                target={"id": "buy_number", "fieldType": "parameters", "fieldName": "SmsUrl"}
            ),
            Link(
                origin={"id": "purchase_number", "fieldType": "parameters", "fieldName": "SmsMethod"},
                target={"id": "buy_number", "fieldType": "parameters", "fieldName": "SmsMethod"}
            ),
            Link(
                origin={"id": "buy_number", "fieldType": "responses", "fieldName": "phone_number"},
                target={"id": "purchase_number", "fieldType": "responses", "fieldName": "phone_number"}
            )
        ]
    )
    
    # Execute purchase
    purchase_result = execute(
        purchase_chain,
        auth,
        parameters={
            "PhoneNumber": available_number,
            "SmsUrl": "https://webhook.site/c633306f-4b8c-4254-b4f9-10c5d88d4359",  # Replace with your webhook URL
            "SmsMethod": "POST"
        },
        requestBody={}
    )
    
    new_number = purchase_result["phone_number"]
    print(f"Successfully purchased number: {new_number}")
    
    # Step 3: Send a test message using the new number
    test_chain = Flow(
        id="test_new_number",
        name="Test New Number",
        displayName="Test New Phone Number",
        description="Sends a test message from the newly purchased number",
        fields={
            "parameters": [
                {"fieldName": "To"},
                {"fieldName": "From"},
                {"fieldName": "Body"}
            ],
            "requestBody": []
        },
        order=[
            Action(
                id="send_test",
                apiName="twilio",
                operationId="twilio_create_message"
            )
        ],
        links=[
            Link(
                origin={"id": "test_new_number", "fieldType": "parameters", "fieldName": "To"},
                target={"id": "send_test", "fieldType": "parameters", "fieldName": "To"}
            ),
            Link(
                origin={"id": "test_new_number", "fieldType": "parameters", "fieldName": "From"},
                target={"id": "send_test", "fieldType": "parameters", "fieldName": "From"}
            ),
            Link(
                origin={"id": "test_new_number", "fieldType": "parameters", "fieldName": "Body"},
                target={"id": "send_test", "fieldType": "parameters", "fieldName": "Body"}
            ),
            Link(
                origin={"id": "send_test", "fieldType": "responses", "fieldName": "sid"},
                target={"id": "test_new_number", "fieldType": "responses", "fieldName": "message_sid"}
            )
        ]
    )
    
    # Send test message
    test_result = execute(
        test_chain,
        auth,
        parameters={
            "To": TO_NUMBER,
            "From": new_number,
            "Body": "Hello! This is a test message from your newly purchased Twilio number!"
        },
        requestBody={}
    )
    
    print(f"Sent test message from new number, SID: {test_result['message_sid']}")

def test_send_sms(auth: BasicAuthConfig):
    # Create a chain that sends an SMS message
    chain = Flow(
        id="test_sms",
        name="Send SMS",
        displayName="Send SMS Message",
        description="Sends an SMS message using Twilio",
        fields={
            "parameters": [
                {"fieldName": "To"},
                {"fieldName": "From"},
                {"fieldName": "Body"}
            ],
            "requestBody": []
        },
        order=[
            Action(
                id="send_sms",
                apiName="twilio",
                operationId="twilio_create_message"
            )
        ],
        links=[
            Link(
                origin={"id": "test_sms", "fieldType": "parameters", "fieldName": "To"},
                target={"id": "send_sms", "fieldType": "parameters", "fieldName": "To"}
            ),
            Link(
                origin={"id": "test_sms", "fieldType": "parameters", "fieldName": "From"},
                target={"id": "send_sms", "fieldType": "parameters", "fieldName": "From"}
            ),
            Link(
                origin={"id": "test_sms", "fieldType": "parameters", "fieldName": "Body"},
                target={"id": "send_sms", "fieldType": "parameters", "fieldName": "Body"}
            ),
            Link(
                origin={"id": "send_sms", "fieldType": "responses", "fieldName": "sid"},
                target={"id": "test_sms", "fieldType": "responses", "fieldName": "message_sid"}
            )
        ]
    )
    
    # Execute the chain
    result = execute(
        chain,
        auth,
        parameters={
            "To": TO_NUMBER,
            "From": FROM_NUMBER,
            "Body": "Hello from Wildcard Twilio integration test!"
        },
        requestBody={}
    )
    print(f"Sent SMS with SID: {result['message_sid']}")
    return result['message_sid']

def test_send_mms_with_gif(auth: BasicAuthConfig):
    # Create a chain that sends an MMS with a GIF
    chain = Flow(
        id="test_mms_gif",
        name="Send MMS with GIF",
        displayName="Send MMS with GIF",
        description="Sends an MMS message with a GIF attachment using Twilio",
        fields={
            "parameters": [
                {"fieldName": "To"},
                {"fieldName": "From"},
                {"fieldName": "Body"},
                {"fieldName": "MediaUrl"}
            ],
            "requestBody": []
        },
        order=[
            Action(
                id="send_mms",
                apiName="twilio",
                operationId="twilio_create_message"
            )
        ],
        links=[
            Link(
                origin={"id": "test_mms_gif", "fieldType": "parameters", "fieldName": "To"},
                target={"id": "send_mms", "fieldType": "parameters", "fieldName": "To"}
            ),
            Link(
                origin={"id": "test_mms_gif", "fieldType": "parameters", "fieldName": "From"},
                target={"id": "send_mms", "fieldType": "parameters", "fieldName": "From"}
            ),
            Link(
                origin={"id": "test_mms_gif", "fieldType": "parameters", "fieldName": "Body"},
                target={"id": "send_mms", "fieldType": "parameters", "fieldName": "Body"}
            ),
            Link(
                origin={"id": "test_mms_gif", "fieldType": "parameters", "fieldName": "MediaUrl"},
                target={"id": "send_mms", "fieldType": "parameters", "fieldName": "MediaUrl"}
            ),
            Link(
                origin={"id": "send_mms", "fieldType": "responses", "fieldName": "sid"},
                target={"id": "test_mms_gif", "fieldType": "responses", "fieldName": "message_sid"}
            )
        ]
    )
    
    # Execute the chain
    result = execute(
        chain,
        auth,
        parameters={
            "To": TO_NUMBER,
            "From": FROM_NUMBER,
            "Body": "Check out this GIF!",
            "MediaUrl": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDd6Y2E4NHF4Y3E2M2t0OWF1NnJ5YnB2bXFvNGxxbzFwbWx0cXh6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MDJ9IbxxvDUQM/giphy.gif"]
        },
        requestBody={}
    )
    print(f"Sent MMS with GIF, result: {result}")
    return result['message_sid']

def test_message_status(auth: BasicAuthConfig):
    # First send a message
    message_sid = test_send_sms(auth)
    
    # Create a chain that checks message status
    chain = Flow(
        id="test_status",
        name="Check Message Status",
        displayName="Check Message Status",
        description="Checks the status of a sent message",
        fields={
            "parameters": [{"fieldName": "Sid"}],
            "requestBody": []
        },
        order=[
            Action(
                id="check_status",
                apiName="twilio",
                operationId="twilio_fetch_message"
            )
        ],
        links=[
            Link(
                origin={"id": "test_status", "fieldType": "parameters", "fieldName": "Sid"},
                target={"id": "check_status", "fieldType": "parameters", "fieldName": "Sid"}
            ),
            Link(
                origin={"id": "check_status", "fieldType": "responses", "fieldName": "status"},
                target={"id": "test_status", "fieldType": "responses", "fieldName": "message_status"}
            )
        ]
    )
    
    # Execute the chain
    result = execute(
        chain,
        auth,
        parameters={"Sid": message_sid},
        requestBody={}
    )
    print(f"Message status: {result['message_status']}")

def test_list_messages(auth: BasicAuthConfig):
    # Create a chain that lists recent messages
    chain = Flow(
        id="test_list",
        name="List Messages",
        displayName="List Recent Messages",
        description="Lists recent messages from your Twilio account",
        fields={
            "parameters": [{"fieldName": "Limit"}],
            "requestBody": []
        },
        order=[
            Action(
                id="list_messages",
                apiName="twilio",
                operationId="twilio_list_message"
            )
        ],
        links=[
            Link(
                origin={"id": "test_list", "fieldType": "parameters", "fieldName": "Limit"},
                target={"id": "list_messages", "fieldType": "parameters", "fieldName": "Limit"}
            ),
            Link(
                origin={"id": "list_messages", "fieldType": "responses", "fieldName": "messages"},
                target={"id": "test_list", "fieldType": "responses", "fieldName": "messages"}
            )
        ]
    )
    
    # Execute the chain
    result = execute(
        chain,
        auth,
        parameters={"Limit": 5},
        requestBody={}
    )
    print(f"Found {len(result['messages'])} recent messages")

# Map of test names to test functions
TESTS: Dict[str, Callable[[BasicAuthConfig], None]] = {
    "sms": test_send_sms,
    "mms": test_send_mms_with_gif,
    "status": test_message_status,
    "list": test_list_messages,
    "search": test_list_available_numbers,
    "purchase": test_phone_number_purchase_workflow,
}

def list_available_tests():
    """Print available test names and their descriptions."""
    print("\nAvailable tests:")
    print("  sms      - Test sending SMS messages")
    print("  mms      - Test sending MMS messages with GIF")
    print("  status   - Test checking message status")
    print("  list     - Test listing recent messages")
    print("  search   - Test searching for available phone numbers")
    print("  purchase - Test purchasing a phone number (requires --purchase flag)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Twilio integration tests')
    parser.add_argument('--account-sid', 
                      help='Twilio Account SID (or set TWILIO_ACCOUNT_SID env var)')
    parser.add_argument('--auth-token', 
                      help='Twilio Auth Token (or set TWILIO_AUTH_TOKEN env var)')
    parser.add_argument('--purchase', action='store_true', 
                      help='Allow running tests that purchase phone numbers (WARNING: This will charge your account!)')
    parser.add_argument('test', choices=list(TESTS.keys()) + ['all'],
                      help='Name of the test to run, or "all" to run all tests')
    parser.add_argument('--list', action='store_true',
                      help='List available tests and exit')
    args = parser.parse_args()

    if args.list:
        list_available_tests()
        exit(0)

    # Get credentials from args or environment
    account_sid = args.account_sid or os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = args.auth_token or os.environ.get('TWILIO_AUTH_TOKEN')

    if not account_sid or not auth_token:
        parser.error("Twilio credentials required. Provide them via arguments or environment variables:\n"
                    "  --account-sid or TWILIO_ACCOUNT_SID\n"
                    "  --auth-token or TWILIO_AUTH_TOKEN")

    auth = get_auth_config(account_sid, auth_token)

    print("Testing Twilio Integration")
    print("-----------------------")

    # Check if trying to run purchase test without flag
    if args.test == "purchase" and not args.purchase:
        parser.error("Must include --purchase flag to run purchase test")

    if args.test == "all":
        # Run all tests except purchase
        for test_name, test_func in TESTS.items():
            if test_name == "purchase":
                continue
            print(f"\nRunning test: {test_name}")
            test_func(auth)
        
        # Run purchase test if flag is provided
        if args.purchase:
            print("\nWARNING: Running phone number purchase workflow...")
            print("This will charge your Twilio account!")
            confirmation = input("Are you sure you want to continue? (yes/no): ")
            if confirmation.lower() == 'yes':
                print("\nProceeding with phone number purchase:")
                TESTS["purchase"](auth)
            else:
                print("Skipping phone number purchase.")
    else:
        # Run single test
        print(f"\nRunning test: {args.test}")
        TESTS[args.test](auth) 