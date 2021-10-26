from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ssm as ssm,
    core,
    aws_ecs_patterns as ecs_patterns
)

PROJECT = {"stack": "ak", "name": "allderms-ak", "image": "allderms-ak", "region": "eu-west-3"} #AK
# PROJECT = {"stack": "pso", "name": "allderms", "image": "allderms-pso", "region": "eu-west-3"} #PSO

app = core.App()
stack = core.Stack(app, "%s-stack" % PROJECT["stack"], env={"region": PROJECT["region"]})
vpc = ec2.Vpc(stack, "%s-VPC" % PROJECT["stack"])
# cluster = ecs.Cluster(stack, "test-cluster", vpc=vpc)

api_repository = ecr.Repository.from_repository_name(
    stack,
    "DermView_Repository",
    repository_name="valinos-ak-dermview" # this is always 'ak' for historical reasons
)

securityGroup = ec2.SecurityGroup(stack, '%s-security-group' % PROJECT["name"],
    vpc=vpc,
    allow_all_outbound=True,
    description='DermView %s Security Group' % PROJECT["stack"],
    # securityGroupName=SECURITY_GROUP_ALPHA
)

for derm in [1,2,3,4,5]:
    load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(stack, "%s-%s-%s-Service" % (PROJECT["name"], PROJECT["stack"], derm),
        vpc=vpc,
        memory_limit_mib=2048,
        cpu=512,
        task_image_options={
            "image": ecs.ContainerImage.from_ecr_repository(api_repository, PROJECT["image"])
        },
        security_groups=[securityGroup]
    )
    
    load_balanced_fargate_service.target_group.configure_health_check(
        path="/"
    )

app.synth()