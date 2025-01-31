import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class SecretsManager:
    def __init__(self):
        self.client = boto3.client('secretsmanager')

    def get_secret(self, secret_name):
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
            return get_secret_value_response['SecretString']
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
            return None
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None
        
        
    def upload_secret(self, secret_name, secret_value):
        try:
            #check if secret already exists
            self.client.describe_secret(SecretId=secret_name)
            print(f"Secret {secret_name} already exists.")
            
            #if it exists, update the secret
            self.client.update_secret(
                SecretId=secret_name,
                SecretString=secret_value,
            )
            print(f"Secret {secret_name} updated successfully.")
            
        except self.client.exceptions.ResourceNotFoundException:
            print(f"Secret {secret_name} does not exist. Creating secret.")
            self.client.create_secret(
                Name=secret_name,
                SecretString=secret_value,
            )
            print(f"Secret {secret_name} created successfully.")
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
        except Exception as e:
            print(f"Error uploading secret {secret_name}: {e}")
            