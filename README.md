# Building & Deploying a ML API to AWS Lambda

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
