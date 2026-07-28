**Complete End-to-End Pipeline**
1. ML Model Training
2. FastAPI + Mangum Wrapper
3. Local Docker Build(Platform & Governance)
4. Push to ECR
5. AWS Lambda Execution
6. Function URL & Postman Test

**Step 1: Model Training & Serialization**
* Model: Built and trained a simple house price prediction model in Python using scikit-learn.
* Export: Serialized the trained model artifacts into a binary .joblib file (house_price_model.joblib) for zero-overhead loading at runtime.

**Step 1: Model Training & Serialization**
* Model: Built and trained a simple house price prediction model in Python using scikit-learn.
* Export: Serialized the trained model artifacts into a binary .joblib file (house_price_model.joblib) for zero-overhead loading at runtime.

**Step 2: REST API Construction (FastAPI + Mangum)**
* Framework: Created main.py using FastAPI to define input schema models (like sqft, bedrooms, bathrooms) and write the /predict POST endpoint.
* Serverless Adapter: Wrapped the ASGI app using mangum (handler = Mangum(app)) so AWS Lambda can translate incoming HTTP event payloads directly into standard FastAPI requests.

**Step 3: Containerization & Docker Desktop Setup**
* Environment Base: Created a Dockerfile built on top of AWS's official Linux runtime image (public.ecr.aws/lambda/python:3.10) to eliminate OS-level C-library compilation mismatches
* Virtualization: Enabled hardware virtualization (VT-x/AMD-V) and WSL 2 on Windows so Docker Desktop could execute Linux containers.
* Architecture Fix: Built the container with specific cross-platform flags to strip extra Docker Buildx attestations that AWS Lambda rejects:

 `docker build --platform linux/amd64 --provenance false -t house-price-api .`

 **Step 4: AWS Authentication & Amazon ECR Push**
* Credentials: Configured access via `aws configure` using freshly generated IAM Access Keys and Secret Access Keys.
* Registry Creation: Created a private container registry in the `ap-southeast-1` region:
  `aws ecr create-repository --repository-name house-price-api --region ap-southeast-1`

* Docker Login & Push: Authenticated local Docker with ECR via temporary AWS CLI tokens, tagged the image, and pushed all image layers up to the cloud:

  `aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com`

  `docker tag house-price-api:latest <ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com/house-price-api:latest`

  `docker push <ACCOUNT_ID>.dkr.ecr.ap-southeast-1.amazonaws.com/house-price-api:latest`
  

**Step 5: AWS Lambda Deployment**
* Function Creation: Provisioned an AWS Lambda function selecting Container image as the source package pointing directly to `house-price-api:latest` in ECR.
* Resource Sizing: Scaled function memory to 512 MB and timeout to 15 seconds to accommodate Machine Learning library warmups.
* Public Function URL: Generated a HTTPS endpoint with CORS enabled and public NONE authentication for testing.

* **Step 6: Testing & Verification**
* Swagger UI: Verified live interactive API documentation by navigating to `<FUNCTION_URL>/docs` in the browser.
* Postman Client: Issued live `POST` requests to `<FUNCTION_URL>/predict` passing JSON feature payloads, receiving real-time price predictions back from the serverless microVMs!

 
