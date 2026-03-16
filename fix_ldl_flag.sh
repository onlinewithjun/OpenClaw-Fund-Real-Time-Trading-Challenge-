#!/bin/bash
# 修复 data_mining 的 BUILD.gn - 移除 -ldl 标志

cat > /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/BUILD.gn << 'ENDOFFILE'
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
}

# ETL 框架主库（包含 Pipeline 引擎）
# 注意：静态库不需要 -ldl，链接时由主程序处理
ohos_static_library("data_mining_etl") {
  sources = [
    "src/etl_interfaces.cpp",
    "src/pipeline.cpp",
  ]
  include_dirs = [ "include" ]
  configs = [ ":data_mining_config" ]
}

# Demo SO 文件（独立编译，用于测试）
group("data_mining_demo") {
  public_deps = []
}
ENDOFFILE

echo "BUILD.gn fixed - removed -ldl flag from static library"
cat /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/BUILD.gn
