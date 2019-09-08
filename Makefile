All: build

build:
	docker build -t cdk-demo-nginx nginx/
	docker build -t cdk-demo-api dummy/

push: build
	docker tag cdk-demo-nginx:latest 085816956471.dkr.ecr.us-east-2.amazonaws.com/frisch-cdk-test:latest
	docker push 085816956471.dkr.ecr.us-east-2.amazonaws.com/frisch-cdk-test:latest
	
	docker tag cdk-demo-api:latest 085816956471.dkr.ecr.us-east-2.amazonaws.com/frisch-cdk-test-django:$(version)
	docker push 085816956471.dkr.ecr.us-east-2.amazonaws.com/frisch-cdk-test-django