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
        print("Waiting for authorization...")
        time.sleep(interval)
    except Exception as e:
        print(f"An error occurred during polling: {e}")
        break
else:
    print("Authentication timed out.")
    exit()

# 4. Use the access token to get account role credentials
# Use the sso client to list and then get specific role credentials
sso_client = boto3.client('sso', region_name=SSO_REGION)

# First, get the available account roles
roles = sso_client.list_account_roles(
    accessToken=access_token,
    accountId=TARGET_ACCOUNT_ID
)

# Find the target role
role_credentials = None
for role in roles['roleList']:
    if role['roleName'] == TARGET_ROLE_NAME:
        role_credentials = sso_client.get_role_credentials(
            accessToken=access_token,
            accountId=TARGET_ACCOUNT_ID,
            roleName=TARGET_ROLE_NAME
        )['roleCredentials']
        break

if not role_credentials:
    print(f"Could not find role {TARGET_ROLE_NAME} in account {TARGET_ACCOUNT_ID}")
    exit()

# 5. Create a new Boto3 session with the retrieved credentials
# These temporary credentials are valid for a short period, and Boto3 manages their usage.
session = boto3.Session(
    aws_access_key_id=role_credentials['accessKeyId'],
    aws_secret_access_key=role_credentials['secretAccessKey'],
    aws_session_token=role_credentials['sessionToken'],
    region_name=SSO_REGION
)

# Test the session by making an AWS API call
sts_client = session.client('sts')
identity = sts_client.get_caller_identity()
print(f"\nSuccessfully created session. Caller identity: {identity['Arn']}")