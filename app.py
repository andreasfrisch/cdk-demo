from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ssm as ssm,
    core,
)

class AutoScalingFargateService(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        logDriver = ecs.AwsLogDriver(
            stream_prefix = "CDKDEMO"
        )

        # Create a cluster
        vpc = ec2.Vpc(
            self, "CDKDEMO-Vpc",
            max_azs = 2
        )

        cluster = ecs.Cluster(
            self, 'CDKDEMO-Cluster',
            vpc = vpc
        )

        task_definition = ecs.FargateTaskDefinition(
            self, 'CDKDEMO-FARGATE-TaskDef',
            memory_limit_mib = 512,
            cpu = 256
        )

        # secret = aws_secretsmanager.Secret.from_secret_arn(
        #     self, "someSecret",
        #     secret_arn = ""
        # )
        # parameter = ssm.StringParameter.from_string_parameter_attributes(
        #     self, "SomeParameter",
        #     parameter_name = "CDKDEMO_SECRET"
        # )
        # parameter = ssm.StringParameter.from_string_parameter_name(
        #     self, "WHATEVER",
        #     string_parameter_name = "/CDKDEMO_SECRET"
        # )
        api_repository = ecr.Repository.from_repository_name(
            self, "CDKDEMO-Repo-Django",
            repository_name="frisch-cdk-test-django"
        )
        api_container = task_definition.add_container(
            "CDKDEMO-CONT-Django",
            image=ecs.ContainerImage.from_ecr_repository(api_repository, "latest"),
            logging=logDriver,
            environment={
                'CDKDEMO_ENVIRONMENT': 'AWS',
                'CDKDEMO_DEBUG': 'True',
                'CDKDEMO_SECRET': 'not really a secret'
            },
            # secrets = {
            #     'CDKDEMO_SECRET': ecs.Secret.from_ssm_parameter(parameter)
            # #     'CDKDEMO_SECRET': parameter
            # }
        )
        api_container.add_port_mappings(
            ecs.PortMapping(container_port=8000, host_port=8000)
        )

        repository = ecr.Repository.from_repository_name(
            self, "CDKDemo-Repo-Nginx",
            repository_name="frisch-cdk-test"
        )
        container = task_definition.add_container(
            "CDKDEMO-CONT-Nginx",
            image = ecs.ContainerImage.from_ecr_repository(repository, "latest"),
            logging = logDriver
        )
        container.add_port_mappings(
            ecs.PortMapping(container_port=80, host_port=80)
        )

        # Create Fargate Service
        fargate_service = ecs.FargateService(
            self, "CDKDEMO-SERVICE",
            cluster = cluster,
            task_definition = task_definition,
            desired_count = 1
        )

        loadbalancer = elbv2.ApplicationLoadBalancer(
            self, "CDKDEMO-ALB",
            vpc = vpc,
            internet_facing = True
        )
        listener = loadbalancer.add_listener(
            "LB-Listener",
            port = 80
        )
        listener.add_targets(
            "ECS",
            port = 80,
            targets = [fargate_service]
        )

        core.CfnOutput(
            self, "LoadBalancerDNS",
            value = loadbalancer.load_balancer_dns_name
        )

app = core.App()
AutoScalingFargateService(app, "CDK-070919")
core.Tag.add(app, 'context', 'CDK-DEMO')
app.synth()