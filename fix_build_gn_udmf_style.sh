#!/bin/bash
# 参考 udmf 的 BUILD.gn 重新编写 data_mining 的 BUILD.gn

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

config("module_public_config") {
  visibility = [ ":*" ]

  include_dirs = [
    "include",
    "${data_service_path}/adapter/include/dfx",
  ]
}

ohos_source_set("data_mining_etl") {
  sources = [
    "src/etl_interfaces.cpp",
    "src/pipeline.cpp",
  ]

  configs = [ ":module_public_config" ]

  cflags = [
    "-D_LIBCPP_HAS_COND_CLOCKWAIT",
    "-Werror",
    "-Oz",
  ]

  deps = [
    "${data_service_path}/framework:distributeddatasvcfwk",
  ]

  external_deps = [
    "hilog:libhilog",
  ]

  cflags_cc = [
    "-fvisibility=hidden",
    "-Oz",
  ]

  subsystem_name = "distributeddatamgr"

  part_name = "datamgr_service"
}

# Demo SO 文件（独立编译，用于测试）
group("data_mining_demo") {
  public_deps = []
}
EOF

echo "Fixed BUILD.gn - following udmf pattern"
cat /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/BUILD.gn
