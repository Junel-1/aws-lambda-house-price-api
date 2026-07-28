# Building & Deploying a ML API to AWS Lambda

## Requirements
1. Docker
2. AWS CLI
3. AWS Account
4. Google Colab or other Python environment
5. Postman(for testing)


## Phase 1: Local Setup & Environment Preparation
Create a Folder(you can create via CLI but this is optional)

`mkdir C:\projects\house-price-api`\
`cd C:\projects\house-price-api`


## Phase 2: Model Training & API Code
Step 1: Train & Save the Machine Learning Model
Create a script named `house_price_prediction.ipynb`(I used google colab for this one) to train your scikit-learn regression model and save it locally. 

Step 2: Save the joblib file in your local folder.

Step 3: Buld the FastAPI App & Lambda Adapter
Create `main.py`(I used local editor like notepad) to serve inference requests using FastAPI and wrap it with Mangum for AWS Lambda compatibility:

## Phase 3: Containerization with Docker
Step 1: Create a file named Dockerfile (no extension) using AWS's official Python 3.10 Lambda base image\

Step 2: Build the Docker Image Locally\
Build your image using explicit architecture (linux/amd64) and provenance flags to prevent multi-manifest errors in AWS Lambda:\
in cli `docker build --platform linux/amd64 --provenance false -t house-price-api .`

## Phase 4: AWS ECR Authentications & Image Push
Step 1: Configure AWS Credentials
Ensure your terminal(cli) is authenticated with your AWS Account:
`aws configure`

Verify authentication:
`aws sts get-caller-identity`

Step 2: Create a private container registry in ECR:

`aws ecr create-repository --repository-name house-price-api --region <region>`

Step 3: Authenticate Docker with ECR, Tag, & Push
Authenticate Docker: `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <AWS Account ID>.dkr.ecr.ap-<region>`

Tag Image: `docker tag house-price-api:latest <AWS Account ID>.dkr.ecr.<region>.amazonaws.com/house-price-api:latest`

Push to ECR: `docker push <AWS Account ID>.dkr.ecr.<Region>.amazonaws.com/house-price-api:latest`

## Phase 5: AWS Lambda & Function URL Deployment
Step 1: Create Lambda Function\
_In your AWS console_
1. Log in to the AWS Management Console and open Lambda in region ap-southeast-1.
2. Click Create function ➔ Select Container image.
3. Function Name: house-price-predictor
4. Click Browse images, select repository house-price-api, pick tag latest, and click Select image.
5. Leave Architecture set to x86_64 and click Create function.

Step 2: Tune Timeout & Memory
_Configuration Tab_
1. Inside the function, select Configuration ➔ General configuration ➔ Edit.
2. Set Memory: 512 MB (or 1024 MB).
3. Set Timeout: 15 seconds.
4.Click Save.

Step 3: Generate Public Endpoint
_Function URL_
1. Navigate to Configuration ➔ Function URL ➔ Create function URL.
2. Set Auth type: NONE.
3. Check Configure cross-origin resource sharing (CORS).
4. Click Save to receive your unique endpoint:
https://<function-id>.lambda-url.<region>.on.aws/


## Phase 6: Testing the Live Cloud API
We have two methods to test our API

Method A: via Postman

* HTTP Method: POST
* URL: https://<function-id>.lambda-url.ap-southeast-1.on.aws/predict
* Headers: Content-Type: application/json
* Body (raw JSON):

`{
  "sqft": 2200,
  "bedrooms": 3,
  "bathrooms": 2.5
}`

and then Run it.

Method B: Python Test Script
Create a `test_api.py` locally
and then run it in cli `python test_api.py`













