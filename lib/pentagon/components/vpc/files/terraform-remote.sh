#!/usr/bin/env  bash
#
# Copyright 2017 Reactive Ops Inc.
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
set -x

export STATE_STORAGE=s3
export STATE_BUCKET=${KOPS_STATE_STORE}
# change for multiple VPCs:
export STATE_KEY=${INFRASTRUCTURE_BUCKET}/${DEFAULT_VPC_TAG}/tfstate
export STATE_REGION=${AWS_DEFAULT_REGION}

echo "configuring remote state ${STATE_STORAGE}://${STATE_BUCKET}/${STATE_KEY} in ${STATE_REGION}"

terraform remote config -backend="${STATE_STORAGE}"              \
                        -backend-config="bucket=${STATE_BUCKET}" \
                        -backend-config="key=${STATE_KEY}"       \
                        -backend-config="region=${STATE_REGION}"
