ECR_REGISTRY="877105616701.dkr.ecr.us-east-1.amazonaws.com"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY
docker build -t aws-crud -f app/Dockerfile ./app
docker tag aws-crud:latest $ECR_REGISTRY/aws-crud:latest
docker push $ECR_REGISTRY/aws-crud:latest