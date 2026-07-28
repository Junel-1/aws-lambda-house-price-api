FROM public.ecr.aws/lambda/python:3.10

# Copy application dependencies and code
COPY requirements.txt ./
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY main.py house_price_model.joblib ./

# Set the Lambda handler function
CMD [ "main.handler" ]