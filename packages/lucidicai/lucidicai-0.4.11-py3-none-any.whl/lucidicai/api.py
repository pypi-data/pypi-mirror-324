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
        self.agentResponseHistory = []

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
        Your goal is to **complete the task** ({task}) like a human, handling all necessary steps and resolving issues dynamically.  

        ### Context:
        - Current step: {context}  
        - Previous advice given: {self.agentResponseHistory}  

        ### Evaluation Rules:
        1. The action **must be immediately actionable on the current screen** (e.g., clicking a button, selecting an option, filling a field). If no valid action is available, determine what is preventing interaction.  
        2. If a **button or element is grayed out or unclickable**, a **previous step was likely missed or incomplete**—identify what must be done to enable it and fix that first. This often requires **scrolling up** to interact with a necessary field, selection, or confirmation.  
        3. Avoid repeating the same action unnecessarily.  
        4. If the **same advice has been given multiple times with no effect**, identify the **underlying issue from an earlier step**, which may also require **scrolling up**, and specify the exact corrective action.  

        ### Output Format (Only one of the following):  
        - `"Correct. Next action: Click/select/input [specific action immediately available on the current screen]."`  
        - `"Incorrect. Error: Incorrect action taken. Correct action: Click/select/input [specific action immediately available on the current screen]."`  
        - `"Incorrect. Error: A previous step may have been missed. Correct action: Scroll up and click/select/input [specific corrective action needed to proceed]."`
        """

        reverification_prompt = f"""
        Verify whether the following action can be performed on the given screen.

        ### Input:
        - **Screen Image**: [Provided image of the current screen]
        - **Proposed Action Statement**: <PROPOSED_ACTION>  
        (This will follow one of these formats:  
        - `"Correct. Next action: Click/select/input [specific action immediately available on the current screen]."`  
        - `"Incorrect. Error: Incorrect action taken. Correct action: Click/select/input [specific action immediately available on the current screen]."`  
        - `"Incorrect. Error: A previous step may have been missed. Correct action: Scroll up and click/select/input [specific corrective action needed to proceed]."`)

        ### Verification Rules:
        1. Extract the **specific action** from the provided statement.  
        2. Check if the **action is immediately visible and interactable on the current screen**.  
        3. **If the action is possible, return only `"YES"`**—no additional text, reasoning, or explanation.  
        4. Return `"NO"` only if the action is impossible due to one of the following:
        - The element is **grayed out, missing, off-screen, or unclickable**.
        - A required step (such as scrolling up or selecting a prerequisite field) **must be completed first**.
        5. If `"NO"` is returned, it **must** be followed by a specific reason explaining why the action cannot be taken.

        ### Output Format:
        - `"YES"` (if the action is fully possible on the current screen, regardless of any justification provided)
        - `"NO: [specific reason describing why the action cannot be performed and what must be corrected first]."`
        """
        
        lastResponse = ""
        while 'YES' not in lastResponse[:5].upper():
            if lastResponse != "":
                reverification_prompt = reverification_prompt.replace('<PROPOSED_ACTION>', response.choices[0].message.content)
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
            content2 = [    
                {
                    "type": "text",
                    "text": prompt
                },
            ]
            response2 = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": content2
                    }
                ],
                # max_tokens=5000,
            )
            lastResponse = response2.choices[0].message.content
            print(f"Lucidic AI: lastResponse was {lastResponse}")

        self.agentResponseHistory.append(response.choices[0].message.content)
        return response.choices[0].message.content





