import requests
import os
import boto3
from botocore.exceptions import ClientError
from mimetypes import MimeTypes
from dotenv import load_dotenv
from openai import OpenAI

class LucidicAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Api-Key {self.api_key}"}
        self.base_url = "https://dashboard.lucidic.ai/demo/api/v1"
        self.endpoints = {
            "verifyAPIKey": "verifyAPIkey",
            "initializejob": "initializejob",
            "assumeAWSS3Role": "getS3creds",
        }
        self.agentResponseHistory = 'None'

    def _makeRequest(self, endpoint, params=None):
        try:
            url = f'{self.base_url}/{self.endpoints[endpoint]}'
            response = requests.get(
                url,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during API Call, status {response.status_code}: {e}")
            raise
        except KeyError as e:
            print(f"Error: Specified endpoint not found.")
            raise


    def _tryCreateS3Bucket(self, creds, bucket_name):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'],
            region_name='us-west-2'
        )

        try:
            s3_client.head_bucket(Bucket=bucket_name)
            bucket_exists = True
            print(f"S3 bucket '{bucket_name}' already exists.")
            return False
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                print(f"S3 bucket '{bucket_name}' does not exist. Creating the bucket...")
            else:
                print(f"Error checking bucket existence: {e}")
                raise
        
        try:
            create_bucket_params = {
                'Bucket': bucket_name,
                'CreateBucketConfiguration': {
                    'LocationConstraint': 'us-west-2'
                    }
                }
            s3_client.create_bucket(**create_bucket_params)
            print(f"S3 bucket '{bucket_name}' created successfully.")
            return True
        except Exception as e:
            print(f"Error creating bucket: {e}")
            raise


    def _queueFiles(self, creds, bucket_name, pathToDataFolder):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'],
            region_name='us-west-2'
        )
        mime = MimeTypes()
        for root, _, files in os.walk(pathToDataFolder):
            for file in files:
                file_path = os.path.join(root, file)
                key = os.path.relpath(file_path, pathToDataFolder)  # Key is relative path in S3
                mime_type, _ = mime.guess_type(file_path)

                # Check if the file is an image or video
                if mime_type and (mime_type.startswith('image/') or mime_type.startswith('video/')):
                    try:
                        # Check if the file already exists in the bucket
                        try:
                            s3_client.head_object(Bucket=bucket_name, Key=key)
                            print(f"File already exists: s3://{bucket_name}/{key}. Skipping upload.")
                            continue
                        except ClientError as e:
                            if int(e.response['Error']['Code']) == 404:
                                # File does not exist, proceed with upload
                                pass
                            else:
                                raise

                        # Upload the file
                        s3_client.upload_file(file_path, bucket_name, key)
                        print(f"Uploaded: {file_path} -> s3://{bucket_name}/{key}")
                    except Exception as e:
                        print(f"Error uploading {file_path}: {e}")


    def verifyAPIKey(self):
        response = self._makeRequest('verifyAPIKey')
        return response.json().get('project', None)
    

    def startJob(self, pathToDataFolder):
        print(f"Starting job, verifying API key...")
        project = self.verifyAPIKey()
        assert project is not None
        print(f"API Key verified for project {project}!")

        print(f"Initializing job...")
        jobInitializationResponseJSON = self._makeRequest('initializejob').json() 
        print(f"{jobInitializationResponseJSON}")
        jobID = jobInitializationResponseJSON.get('jobID', None)
        assert jobID is not None
        print(f"Job Initialized with jobID: {jobID}")

        print(f"Issuing temporary AWS S3 Credentials...")
        creds = self._makeRequest('assumeAWSS3Role').json()
        assert 'AccessKeyId' in creds and 'SecretAccessKey' in creds and 'Expiration' in creds
        print(f"Temporary AWS Credentials Issued!")

        print(f"Creating AWS S3 Bucket...")
        bucketName = project
        if len(project) > 25:
            bucketName = project[:25]
        bucketName += '.' + jobID
        self._tryCreateS3Bucket(creds, bucketName)

        print(f"Uploading files...")
        self._queueFiles(creds, bucketName, pathToDataFolder)

    def analyzeAgentActions(self, task, screenshots, context):
        load_dotenv()
        OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
        client = OpenAI(api_key=OPENAI_API_KEY)
        image_quality = 'auto'
        # prompt = f'I am an AI agent working to browse the web and complete tasks for my user. My current task is {task}. It seems like I made a mistake, please identify what the mistake is from the screenshots I have attached, and please tell me some actionable steps to fix my mistake and complete my task. Tell me which screenshot number contains the mistake made.'
        prompt = f"""
        Our goal is to **successfully complete the task** ({task}) like a human, handling all necessary steps and solving issues as they arise.  

        ### Context:
        - Current step: {context}  
        - Previous advice given: {self.agentResponseHistory}  

        ### Evaluation Rules:
        1. The action must be **necessary and appropriate for the current screen**.  
        2. The agent must **only take one immediate actionable step available on the screen**.  
        3. Repeating the same action unnecessarily is incorrect.  
        4. If an issue arises, solve it in a logical, human-like way.  

        ### Output Format (Only one of the following):  
        - If correct: Output **only** this message:  
        `"Correct. Next action: [one immediate actionable step available on the screen]."`  
        - If incorrect: Output **only** this message:  
        `"Incorrect. Error: [most_likely_mistake]. Correct action: [one immediate next step that should be taken]."`
        """

        content = [    
            {
                "type": "text",
                "text": prompt
            },
        ]
        for index, image in enumerate(screenshots):
            content.append(
                {
                    'type': 'text',
                    'text': f'This is image number {index + 1}',
                }
            )
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image}",
                        "detail": image_quality,
                    }
                }
            )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            # max_tokens=5000,
        )
        self.agentResponseHistory = response.choices[0].message.content
        return response.choices[0].message.content





