#!/bin/bash
# 修复 data_mining 的 BUILD.gn - 添加 hilog 依赖

cat > /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/BUILD.gn << 'EOF'
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import("//build/ohos.gni")
import("//foundation/distributeddatamgr/datamgr_service/datamgr_service.gni")

config("data_mining_config") {
  include_dirs = [ "include" ]
  # 添加 hilog 的 include 路径
  include_dirs += [
    "//foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/adapter/include/dfx",
  ]
}

# ETL 框架主库（包含 Pipeline 引擎）
ohos_static_library("data_mining_etl") {
  sources = [
    "src/etl_interfaces.cpp",
    "src/pipeline.cpp",
  ]
  include_dirs = [ "include" ]
  configs = [ ":data_mining_config" ]
  # 添加 hilog 依赖
  deps = [
    "//foundation/hiviewdfx/hilog_native:libhilog",
  ]
}

# Demo SO 文件（独立编译，用于测试）
group("data_mining_demo") {
  public_deps = []
}
EOF

echo "Fixed BUILD.gn - added hilog dependency"
cat /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/BUILD.gn
