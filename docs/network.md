# VPC Description
We create a base VPC with [terraform-vpc](https://github.com/reactiveops/terraform-vpc) that allocates capacity for AWS-based resources that a client needs to host, including `kubernetes`. We then let `kops` work in the same VPC to carve out a dedicated space for itself so that `kubernetes` is self-contained and manageable.

After running `pentagon start-project` you can alter the configuration of the VPC by editing the  `default/vpc/terraform.tfvars` and  `default/vpc/main.tf` files in the infrastructure. You can also configure the VPC using command line arguments to `pentagon start-project`

## VPC
The VPC is created by Terraform VPC which sets up a standard RO-style network platform. `kops` is then used to configure and deploy `kubernetes` into this existing VPC.

### Subnets
Per AZ, terraform-vpc creates 4 subnets: 1 `admin`, 1 `public`, and 2 `private` (one `working` and one `production`). Use these subnets to deploy any resources other than those directly associated with `kubernetes`.

Let `kops` create dedicated public and private subnets that run in parallel to those created by terraform-vpc. Each AZ consists of a pair of kops-defined subnets- `public` and `private`. In `kops edit cluster`, allocate CIDRs of available address space.  

### NAT Gateways
NAT Gateways are created by terraform-vpc and one is needed for each AZ. You can share a NAT Gateway for use by `kubernetes` and your other AWS-based resources simultaneously. This is the only exception to the separation of `kops` and TF. During `kops edit cluster`, specify the NAT Gateway in the private subnet using the keyword `egress` as shown in the [kops Example networking spec](#kops-example-networking-spec). Egress is currently only useful if you are using private subnets as defined in kops.

## Route tables
terraform-vpc sets up route tables for all of the standard subnets. The `private` subnets default route for external traffic is the NAT Gateway in that zone. The `public` subnets default route is through an Internet Gateway.

`kops` manages the subnets for your `kubernetes` resources so it also manages these route tables. Specifying the NAT Gateway that terraform-vpc created in `egress` will configure the default routes for these subnets to its specified NAT Gateway.

Because NAT Gateways don't have tags on AWS, `kops` keeps track of this NAT Gateway by AWS-tagging the route table with K=V pair `AssociatedNatGateway=nat-05ee835341f099286`. This is for the delete logic in `kops` that likely wouldn't actually be able to delete the Gateway (because it would still be in use by other routes), but it would attempt to delete it as a "related resource".

## Tags
terraform-vpc tags all of the resources that it creates and manages as `Managed By=Terraform`. Likewise, `kops` tags the resources that it creates and manages with `KubernetesCluster=<clustername>`. By letting `kops` create its own subnets, `kops` related tags are all restricted to resources that are owned by `kops`, so terraform-vpc doesn't ever need to know about `kops` and vice versa.

## kops Example networking spec

## Network overview diagram

| **Subnet Name (abstracted)**     | **Example Name**                                         | **Private / Public** | **Created / Managed by** |
| -------------------------------- | -------------------------------------------------------- | -------------------- | ------------------------ |
| admin_az$n                       | admin_az1                                                | Private              | terraform-vpc            |
| private_working_az$n             | private_working_az1                                      | Private              | terraform-vpc            |
| private_prod_az$n                | private_prod_az1                                         | Private              | terraform-vpc            |
| public_ax$n                      | public_az1                                               | Public               | terraform-vpc            |
| az$n.$cluster_identifier         | us-east-1a.working-1.shareddev.dev.hillghost.com         | Private              | kops                     |
| utility-az$n.$cluster_identifier | utility-us-east-1a.working-1.shareddev.dev.hillghost.com | Public               | kops                     |



CIDRs should always be allocated assuming a 4AZ layout for possible future expansion, even if the client doesn't initially need all of the AZs. This also helps to keep our DaaS network layout as consistent as possible. The CIDR math with /24 subnets has a theoretical limit of 29 kubernetes clusters in private topology in addition to `admin`, `public`, `private_prod` and `private_working` environments created by terraform.

| **Subnet Name**                  | **AZ**                                                   | **CIDR**        |
| -------------------------------- | -------------------------------------------------------- | --------------- |
| admin_az1                        | us-east-1a                                               | 172.20.0.0/24   |
| admin_az2                        | us-east-1b                                               | 172.20.1.0/24   |
| admin_az3                        | us-east-1c                                               | 172.20.2.0/24   |
| public_az1                       | us-east-1a                                               | 172.20.4.0/24  |
| public_az2                       | us-east-1b                                               | 172.20.5.0/24  |
| public_az3                       | us-east-1c                                               | 172.20.6.0/24  |
| private_prod_az1                 | us-east-1a                                               | 172.20.8.0/24  |
| private_prod_az2                 | us-east-1b                                               | 172.20.9.0/24  |
| private_prod_az3                 | us-east-1c                                               | 172.20.10.0/24  |
| private_working_az1              | us-east-1a                                               | 172.20.12.0/24  |
| private_working_az2              | us-east-1b                                               | 172.20.13.0/24  |
| private_working_az3              | us-east-1c                                               | 172.20.14.0/24  |
| us-east-1a.working-1.shareddev.dev.hillghost.com | us-east-1a                               | 172.20.16.0/24  |
| us-east-1b.working-1.shareddev.dev.hillghost.com | us-east-1b                               | 172.20.17.0/24  |
| us-east-1c.working-1.shareddev.dev.hillghost.com | us-east-1c                               | 172.20.18.0/24  |
| utility-us-east-1a.working-1.shareddev.dev.hillghost.com | us-east-1a                       | 172.20.20.0/24  |
| utility-us-east-1b.working-1.shareddev.dev.hillghost.com | us-east-1b                       | 172.20.21.0/24  |
| utility-us-east-1c.working-1.shareddev.dev.hillghost.com | us-east-1c                       | 172.20.22.0/24  |
| us-east-1a.production-1.shareddev.dev.hillghost.com | us-east-1a                            | 172.20.24.0/24  |
| us-east-1b.production-1.shareddev.dev.hillghost.com | us-east-1b                            | 172.20.25.0/24 |
| us-east-1c.production-1.shareddev.dev.hillghost.com | us-east-1c                            | 172.20.26.0/24 |
| utility-us-east-1a.production-1.shareddev.dev.hillghost.com | us-east-1a                    | 172.20.28.0/24 |
| utility-us-east-1b.production-1.shareddev.dev.hillghost.com | us-east-1b                    | 172.20.29.0/24 |
| utility-us-east-1c.production-1.shareddev.dev.hillghost.com | us-east-1c                    | 172.20.30.0/24 |

The above table, with 2 clusters, and CIDRs included. Note this cluster has subnets defined in 3 AZs, but space for an additional AZ if the client requires expansion.



```yaml
subnets:
- cidr: 172.20.16.0/24
  egress: nat-05ee835341f099286
  name: us-east-1a
  type: Private
  zone: us-east-1a
- cidr: 172.20.17.0/24
  egress: nat-0973eca2e99f9249c
  name: us-east-1b
  type: Private
  zone: us-east-1b
- cidr: 172.20.18.0/24
  egress: nat-015aa74ead665693d
  name: us-east-1c
  type: Private
  zone: us-east-1c
- cidr: 172.20.20.0/24
  name: utility-us-east-1a
  type: Utility
  zone: us-east-1a
- cidr: 172.20.21.0/24
  name: utility-us-east-1b
  type: Utility
  zone: us-east-1b
- cidr: 172.20.22.0/24
  name: utility-us-east-1c
  type: Utility
  zone: us-east-1c
```








