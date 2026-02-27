import boto3
import time
import webbrowser

# --- Configuration ---
# Get these values from your AWS IAM Identity Center (SSO) console settings.
SSO_REGION = 'us-west-2' # The region where AWS SSO is configured
SSO_START_URL = 'https://d-92671513a4.awsapps.com/start/'
CLIENT_NAME = 'MyAppName' 

# The desired account ID and role name after authentication
TARGET_ACCOUNT_ID = '126136695610' 
TARGET_ROLE_NAME = 'AWSReadOnlyAccess'

# 1. Register the client device
# Use the sso-oidc client to initiate the device registration
oidc_client = boto3.client('sso-oidc', region_name=SSO_REGION)
client_registration = oidc_client.register_client(
    clientName=CLIENT_NAME,
    clientType='public' # 'public' is the only supported type
)

client_id = client_registration['clientId']
client_secret = client_registration['clientSecret']

# 2. Start the device authorization flow
# This generates the user code and verification URI.
device_authorization = oidc_client.start_device_authorization(
    clientId=client_id,
    clientSecret=client_secret,
    startUrl=SSO_START_URL
)

device_code = device_authorization['deviceCode']
user_code = device_authorization['userCode']
verification_uri = device_authorization['verificationUri']
expires_in = device_authorization['expiresIn']
interval = device_authorization['interval']

print(f"Please go to this URL in your browser: {verification_uri}")
print(f"And enter the code: {user_code}")

# Optionally open the browser automatically
# webbrowser.open(device_authorization['verificationUriComplete'])

print(device_authorization['verificationUriComplete'])

# 3. Poll for the access token
# Keep polling the create_token endpoint until the user authenticates in the browser.
start_time = time.time()
print("Waiting for authorization...", end="", flush=True)
while time.time() - start_time < expires_in:
    try:
        token_response = oidc_client.create_token(
            clientId=client_id,
            clientSecret=client_secret,
            deviceCode=device_code,
            grantType='urn:ietf:params:oauth:grant-type:device_code'
        )
        access_token = token_response['accessToken']
        print("\nSuccessfully authenticated!")
        break
    except oidc_client.exceptions.AuthorizationPendingException:
        print("...", end="", flush=True)
        time.sleep(interval)
    except Exception as e:
        print(f"\nAn error occurred during polling: {e}")
        break
else:
    print("\nAuthentication timed out.")
    exit()

# 4. Use the access token to get account role credentials
# Use the sso client to list and then get specific role credentials
sso_client = boto3.client('sso', region_name=SSO_REGION)

# Use a paginator to handle potentially large results
paginator = sso_client.get_paginator('list_accounts')

# Iterate through pages of accounts using the accessToken
# Documentation: https://docs.aws.amazon.com
pages = paginator.paginate(accessToken=access_token)

accounts = []
for page in pages:
    for account in page.get('accountList', []):
        accounts.append(account)
        # Example account structure (dict): 
        # {'accountId': '123456789012', 'accountName': 'ExampleAccount', ...}

if accounts:
        print("AWS Accounts assigned to the user:")
        for acct in accounts:
            print(f"- Account ID: {acct['accountId']}, Name: {acct['accountName']}")

