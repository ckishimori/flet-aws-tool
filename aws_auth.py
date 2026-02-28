import boto3
import asyncio # Changed to asyncio for non-blocking sleep

class AWSAuthManager:
    def initiate_sso(self, start_url, region):
        # Create client based on user input
        self.sso_oidc = boto3.client('sso-oidc', region_name=region)
        
        client = self.sso_oidc.register_client(
            clientName='FletApp',
            clientType='public'
        )
        auth_data = self.sso_oidc.start_device_authorization(
            clientId=client['clientId'],
            clientSecret=client['clientSecret'],
            startUrl=start_url
        )
        return auth_data, client

    async def poll_for_token_async(self, auth_data, client_info):
        while True:
            try:
                response = self.sso_oidc.create_token(
                    clientId=client_info['clientId'],
                    clientSecret=client_info['clientSecret'],
                    grantType='urn:ietf:params:oauth:grant-type:device_code',
                    deviceCode=auth_data['deviceCode']
                )
                return response['accessToken']
            except self.sso_oidc.exceptions.AuthorizationPendingException:
                # Use non-blocking sleep
                await asyncio.sleep(auth_data.get('interval', 5))
            except Exception as e:
                return f"Error: {str(e)}"
