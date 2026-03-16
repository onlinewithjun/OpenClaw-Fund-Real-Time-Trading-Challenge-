#!/usr/bin/env python3
"""Generate BUILD.gn and pipeline config files"""

import os

COPYRIGHT_GN = '''# Copyright (c) 2026 Huawei Device Co., Ltd.
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

'''

BASE = "/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining"

# BUILD.gn
with open(f"{BASE}/BUILD.gn", "w") as f:
    f.write(COPYRIGHT_GN + '''import("//build/ohos.gni")
import("//foundation/distributeddatamgr/datamgr_service/datamgr_service.gni")

config("data_mining_config") {
  include_dirs = [ "include" ]
}

ohos_static_library("data_mining_etl") {
  sources = [
    "src/etl_interfaces.cpp",
  ]
  include_dirs = [ "include" ]
  configs = [ ":data_mining_config" ]
}

ohos_shared_library("libdemo_source") {
  sources = [ "demo/demo_source.cpp" ]
  include_dirs = [ "include" ]
  configs = [ ":data_mining_config" ]
}

ohos_shared_library("libdemo_operator") {
  sources = [ "demo/demo_operator.cpp" ]
  include_dirs = [ "include" ]
  configs = [ ":data_mining_config" ]
}

ohos_shared_library("libdemo_slink") {
  sources = [ "demo/demo_slink.cpp" ]
  include_dirs = [ "include" ]
  configs = [ ":data_mining_config" ]
}

ohos_unittest("data_mining_unittest") {
  sources = [
    "test/etl_interfaces_test.cpp",
    "test/operator_loader_test.cpp",
  ]
  include_dirs = [ "include" ]
  deps = [
    ":data_mining_etl",
    "//third_party/googletest:gtest_main",
  ]
  configs = [ ":data_mining_config" ]
}
''')
print("✓ Created BUILD.gn")

# Pipeline config
with open(f"{BASE}/pipeline/demo_pipeline.json", "w") as f:
    f.write('''{
    "pipeline": {
        "name": "demo_etl_pipeline",
        "description": "ETL 数据挖掘示例 Pipeline",
        "trigger": {
            "type": "manual",
            "config": ""
        }
    },
    "operators": [
        {
            "name": "demo_source",
            "type": "source",
            "library": "/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/demo/libdemo_source.so",
            "create_symbol": "CreateDemoSource",
            "destroy_symbol": "DestroyDemoSource",
            "parameters": {}
        },
        {
            "name": "demo_operator",
            "type": "operator",
            "library": "/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/demo/libdemo_operator.so",
            "create_symbol": "CreateDemoOperator",
            "destroy_symbol": "DestroyDemoOperator",
            "parameters": {}
        },
        {
            "name": "demo_slink",
            "type": "slink",
            "library": "/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/demo/libdemo_slink.so",
            "create_symbol": "CreateDemoSlink",
            "destroy_symbol": "DestroyDemoSlink",
            "parameters": {
                "save_path": "/tmp/data_mining_output.txt"
            }
        }
    ],
    "nodes": [
        {
            "name": "source_node",
            "type": "source",
            "operator": "demo_source",
            "parameters": {},
            "next": ["operator_node"]
        },
        {
            "name": "operator_node",
            "type": "operator",
            "operator": "demo_operator",
            "parameters": {},
            "next": ["slink_node"]
        },
        {
            "name": "slink_node",
            "type": "slink",
            "operator": "demo_slink",
            "parameters": {
                "save_path": "/tmp/data_mining_output.txt"
            },
            "next": []
        }
    ]
}
''')
print("✓ Created demo_pipeline.json")

# Test file
with open(f"{BASE}/test/etl_interfaces_test.cpp", "w") as f:
    f.write(COPYRIGHT_GN + '''
#include <gtest/gtest.h>
#include "../include/etl_interfaces.h"

using namespace OHOS::DataMining::ETL;

TEST(EtlInterfacesTest, ContextTest)
{
    Context ctx;
    ctx.Set("key1", std::string("value1"));
    EXPECT_TRUE(ctx.Has("key1"));
    std::any value = ctx.Get("key1");
    EXPECT_EQ(std::any_cast<std::string>(value), "value1");
}

TEST(EtlInterfacesTest, AsyncDataTest)
{
    AsyncData asyncData;
    bool notified = false;
    asyncData.SetNotifyCallback([&notified](Context &, const std::string &, const std::any &) {
        notified = true;
    });
    Context ctx;
    asyncData.Notify(ctx, "test", std::any());
    EXPECT_TRUE(notified);
}

TEST(EtlInterfacesTest, SourceTest)
{
    EXPECT_TRUE(true);  // Placeholder for Source tests
}

TEST(EtlInterfacesTest, OperatorTest)
{
    EXPECT_TRUE(true);  // Placeholder for Operator tests
}

TEST(EtlInterfacesTest, SlinkTest)
{
    EXPECT_TRUE(true);  // Placeholder for Slink tests
}
''')
print("✓ Created etl_interfaces_test.cpp")

# operator_loader_test.cpp
with open(f"{BASE}/test/operator_loader_test.cpp", "w") as f:
    f.write(COPYRIGHT_GN + '''
#include <gtest/gtest.h>
// #include "../include/operator_loader.h"

TEST(OperatorLoaderTest, LoadDemoSource)
{
    // Test loading demo_source.so
    EXPECT_TRUE(true);  // Placeholder
}

TEST(OperatorLoaderTest, LoadDemoOperator)
{
    // Test loading demo_operator.so
    EXPECT_TRUE(true);  // Placeholder
}

TEST(OperatorLoaderTest, LoadDemoSlink)
{
    // Test loading demo_slink.so
    EXPECT_TRUE(true);  // Placeholder
}
''')
print("✓ Created operator_loader_test.cpp")

print("\n✅ All configuration files created!")
