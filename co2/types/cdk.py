class TYPES:
    _ = {
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnVPC.html#cfnvpc
            "AWS::EC2::VPC": {
                "scope" : None,
                "id" : None,
                "cidr_block" : None,
                "enable_dns_hostnames" : None,
                "enable_dns_support" : None,
                "instance_tenancy" : None,
                "tags" : None
            },
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnRouteTable.html#cfnroutetable
            "AWS::EC2::RouteTable": {
                "scope": None,
                "id": None,
                "vpc_id": None,
                "tags": None
            },
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnSecurityGroup.html#cfnsecuritygroup
            "AWS::EC2::SecurityGroup": {
                "scope": None,
                "id": None,
                "group_description": None,
                "group_name": None,
                "security_group_egress": None,
                "security_group_ingress": None,
                "tags": None,
                "vpc_id": None,
            },
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnSubnet.html#cfnsubnet
            "AWS::EC2::Subnet": {
                "scope": None,
                "id": None,
                "cidr_block": None,
                "vpc_id": None,
                "assign_ipv6_address_on_creation": None,
                "availability_zone": None,
                "ipv6_cidr_block": None,
                "map_public_ip_on_launch": None,
                "outpost_arn": None,
                "tags": None,
            },
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnSubnetRouteTableAssociation.html#cfnsubnetroutetableassociation 
            "AWS::EC2::SubnetRouteTableAssociation": {
                "scope": None,
                "id": None,
                "route_table_id": None,
                "subnet_id": None,
            },
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnRoute.html#cfnroute
            "AWS::EC2::Route": {
                "scope": None,
                "id": None,
                "route_table_id": None,
                "carrier_gateway_id": None,
                "destination_cidr_block": None,
                "destination_ipv6_cidr_block": None,
                "egress_only_internet_gateway_id":None,
                "gateway_id":None,
                "instance_id": None,
                "local_gateway_id": None,
                "nat_gateway_id": None,
                "network_interface_id": None,
                "transit_gateway_id": None,
                "vpc_endpoint_id": None,
                "vpc_peering_connection_id": None,
            },
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnInstance.html#cfninstance
            "AWS::EC2::Instance": {
                "scope": None,
                "id": None,
                "additional_info": None,
                "affinity": None,
                "availability_zone": None,
                "block_device_mappings": None,
                "cpu_options": None,
                "credit_specification": None,
                "disable_api_termination": None,
                "ebs_optimized":None,
                "elastic_gpu_specifications": None,
                "elastic_inference_accelerators": None,
                "enclave_options": None,
                "hibernation_options": None,
                "host_id": None,
                "host_resource_group_arn": None,
                "iam_instance_profile": None,
                "image_id": None,
                "instance_initiated_shutdown_behavior": None,
                "instance_type": None,
                "ipv6_address_count": None,
                "ipv6_addresses": None,
                "kernel_id":None,
                "key_name": None,
                "launch_template": None,
                "license_specifications": None,
                "monitoring": None,
                "network_interfaces": None,
                "placement_group_name": None,
                "private_ip_address": None,
                "ramdisk_id": None,
                "security_group_ids": None,
                "security_groups": None,
                "source_dest_check": None,
                "ssm_associations": None,
                "subnet_id": None,
                "tags": None,
                "tenancy": None,
                "user_data": None,
                "volumes": None,
            }
    }

