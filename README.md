# CDK Demo

## Running

First build the two docker images

	make build

Then push a version of those images to ECR
Note: Change the Makefile to the correct ECR repositories

	make push version=<version>

Finally deploy via AWS CDK, running

	cdk deploy -c version=<version>

If you need to run as a specialized profile this can be done thus

	cdk --profile <profile> <command>

AWS will create all required resources and output the loadbalancer URL

## Stopping

Simply run

	cdk destroy