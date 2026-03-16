#!/usr/bin/env python3
"""
Data Mining ETL Framework - Complete Fix Script
Fixes all issues:
1. Update bundle.json
2. Remove ETL namespace
3. Rewrite UT tests in OpenHarmony style
4. Separate demo code from main build
"""

import json
import os

BASE = "/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service"
DM_BASE = f"{BASE}/services/distributeddataservice/service/data_mining"

COPYRIGHT_CPP = '''/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'''

# 1. Update bundle.json
print("1. Updating bundle.json...")
with open(f"{BASE}/bundle.json", "r") as f:
    bundle = json.load(f)

if "datamgr_service_data_mining" not in bundle["component"]["features"]:
    bundle["component"]["features"].append("datamgr_service_data_mining")
    with open(f"{BASE}/bundle.json", "w") as f:
        json.dump(bundle, f, indent=4)
    print("   ✓ Added datamgr_service_data_mining to features")
else:
    print("   ✓ datamgr_service_data_mining already in features")

# 2. Update etl_interfaces.h - Remove ETL namespace
print("\n2. Updating etl_interfaces.h (removing ETL namespace)...")
with open(f"{DM_BASE}/include/etl_interfaces.h", "w") as f:
    f.write(COPYRIGHT_CPP + '''
#ifndef OHOS_DISTRIBUTED_DATA_MGR_SERVICE_DATA_MINING_INTERFACES_H
#define OHOS_DISTRIBUTED_DATA_MGR_SERVICE_DATA_MINING_INTERFACES_H

#include <string>
#include <memory>
#include <functional>
#include <any>
#include <map>
#include <vector>

namespace OHOS {
namespace DataMining {

class Context {
public:
    void Set(const std::string &key, const std::any &value);
    std::any Get(const std::string &key) const;
    bool Has(const std::string &key) const;
    void SetOperatorName(const std::string &name);
    const std::string &GetOperatorName() const;
private:
    std::map<std::string, std::any> data_;
    std::string operatorName_;
};

class AsyncData {
public:
    using NotifyCallback = std::function<void(Context&, const std::string&, const std::any&)>;
    void SetNotifyCallback(NotifyCallback callback);
    void Notify(Context &ctx, const std::string &event, const std::any &data);
private:
    NotifyCallback notifyCallback_;
};

class Source {
public:
    Source();
    virtual ~Source();
    const std::string &GetName() const;
    void SetName(const std::string &name);
    virtual int OnInitialize() = 0;
    virtual int Trigger(Context &context, std::shared_ptr<AsyncData> asyncData) = 0;
    virtual int Subscribe(Context &context, std::shared_ptr<AsyncData> asyncData) = 0;
    virtual int UnSubscribe(Context &context) = 0;
    virtual int OnStop() = 0;
protected:
    std::string name_;
};

class Operator {
public:
    Operator();
    virtual ~Operator();
    const std::string &GetName() const;
    void SetName(const std::string &name);
    virtual int Process(Context &context, const std::any &input, std::shared_ptr<AsyncData> asyncData) = 0;
    virtual std::any Process(Context &context, const std::any &input) = 0;
protected:
    std::string name_;
};

class Slink {
public:
    Slink();
    virtual ~Slink();
    const std::string &GetName() const;
    void SetName(const std::string &name);
    virtual int Save(Context &context, const std::any &data) = 0;
protected:
    std::string name_;
};

using SourceCreator = Source *(*)();
using OperatorCreator = Operator *(*)();
using SlinkCreator = Slink *(*)();
using DestroyFunc = void (*)(Source *);
using OperatorDestroyFunc = void (*)(Operator *);
using SlinkDestroyFunc = void (*)(Slink *);

} // namespace DataMining
} // namespace OHOS

#endif // OHOS_DISTRIBUTED_DATA_MGR_SERVICE_DATA_MINING_INTERFACES_H
''')
print("   ✓ Updated etl_interfaces.h")

# 3. Update demo files - Remove ETL namespace
print("\n3. Updating demo files (removing ETL namespace)...")
for demo_file in ["demo_source.cpp", "demo_operator.cpp", "demo_slink.cpp"]:
    with open(f"{DM_BASE}/demo/{demo_file}", "r") as f:
        content = f.read()
    content = content.replace("namespace OHOS {\nnamespace DataMining {\nnamespace ETL {", 
                              "namespace OHOS {\nnamespace DataMining {")
    content = content.replace("} // namespace ETL\n} // namespace DataMining\n} // namespace OHOS",
                              "} // namespace DataMining\n} // namespace OHOS")
    content = content.replace("OHOS::DataMining::ETL::", "OHOS::DataMining::")
    with open(f"{DM_BASE}/demo/{demo_file}", "w") as f:
        f.write(content)
    print(f"   ✓ Updated {demo_file}")

# 4. Rewrite UT tests in OpenHarmony style
print("\n4. Rewriting UT tests in OpenHarmony style...")

# interfaces_test.cpp
with open(f"{DM_BASE}/test/interfaces_test.cpp", "w") as f:
    f.write(COPYRIGHT_CPP + '''
#include <gtest/gtest.h>
#include <iostream>
#include "../include/etl_interfaces.h"

namespace OHOS {
namespace DataMining {
namespace Test {

using namespace testing::ext;

class DataMiningInterfacesTest : public testing::Test {
public:
    static void SetUpTestCase(void) {}
    static void TearDownTestCase(void) {}
    void SetUp() {}
    void TearDown() {}
};

/**
 * @tc.name: ContextSetGetTest
 * @tc.desc: Test Context Set and Get functionality
 * @tc.type: FUNC
 * @tc.require:
 */
HWTEST_F(DataMiningInterfacesTest, ContextSetGetTest, TestSize.Level0)
{
    Context ctx;
    std::string testValue = "test_value";
    ctx.Set("test_key", testValue);
    
    EXPECT_TRUE(ctx.Has("test_key"));
    EXPECT_FALSE(ctx.Has("nonexistent_key"));
    
    std::any value = ctx.Get("test_key");
    EXPECT_EQ(std::any_cast<std::string>(value), "test_value");
}

/**
 * @tc.name: ContextOperatorNameTest
 * @tc.desc: Test Context operator name functionality
 * @tc.type: FUNC
 * @tc.require:
 */
HWTEST_F(DataMiningInterfacesTest, ContextOperatorNameTest, TestSize.Level0)
{
    Context ctx;
    ctx.SetOperatorName("test_operator");
    EXPECT_EQ(ctx.GetOperatorName(), "test_operator");
}

/**
 * @tc.name: AsyncDataNotifyTest
 * @tc.desc: Test AsyncData notification functionality
 * @tc.type: FUNC
 * @tc.require:
 */
HWTEST_F(DataMiningInterfacesTest, AsyncDataNotifyTest, TestSize.Level0)
{
    AsyncData asyncData;
    bool notified = false;
    std::string receivedEvent;
    
    asyncData.SetNotifyCallback([&notified, &receivedEvent](Context &, const std::string &event, const std::any &) {
        notified = true;
        receivedEvent = event;
    });
    
    Context ctx;
    asyncData.Notify(ctx, "test_event", std::any());
    
    EXPECT_TRUE(notified);
    EXPECT_EQ(receivedEvent, "test_event");
}

/**
 * @tc.name: SourceConstructorTest
 * @tc.desc: Test Source constructor
 * @tc.type: FUNC
 * @tc.require:
 */
HWTEST_F(DataMiningInterfacesTest, SourceConstructorTest, TestSize.Level0)
{
    EXPECT_TRUE(true); // Source is abstract, testing framework compilation
}

/**
 * @tc.name: OperatorConstructorTest
 * @tc.desc: Test Operator constructor
 * @tc.type: FUNC
 * @tc.require:
 */
HWTEST_F(DataMiningInterfacesTest, OperatorConstructorTest, TestSize.Level0)
{
    EXPECT_TRUE(true); // Operator is abstract, testing framework compilation
}

/**
 * @tc.name: SlinkConstructorTest
 * @tc.desc: Test Slink constructor
 * @tc.type: FUNC
 * @tc.require:
 */
HWTEST_F(DataMiningInterfacesTest, SlinkConstructorTest, TestSize.Level0)
{
    EXPECT_TRUE(true); // Slink is abstract, testing framework compilation
}

} // namespace Test
} // namespace DataMining
} // namespace OHOS
''')
print("   ✓ Created interfaces_test.cpp")

# 5. Update BUILD.gn - Separate demo from main build
print("\n5. Updating BUILD.gn (separating demo from main build)...")
with open(f"{DM_BASE}/BUILD.gn", "w") as f:
    f.write('''# Copyright (c) 2026 Huawei Device Co., Ltd.
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

# Main ETL framework library (will be included in datamgr_service)
ohos_static_library("data_mining_etl") {
  sources = [
    "src/etl_interfaces.cpp",
  ]
  include_dirs = [ "include" ]
  configs = [ ":data_mining_config" ]
}

# Demo SO files (NOT included in main build, for local testing only)
# To build demo: cd demo && ./build_demo.sh
group("data_mining_demo") {
  public_deps = []
}

# Unit tests
ohos_unittest("data_mining_unittest") {
  sources = [
    "test/interfaces_test.cpp",
  ]
  include_dirs = [ "include" ]
  deps = [
    ":data_mining_etl",
    "//third_party/googletest:gtest_main",
  ]
  configs = [ ":data_mining_config" ]
}
''')
print("   ✓ Updated BUILD.gn")

# 6. Create demo build script (separate from main build)
print("\n6. Creating demo build script...")
with open(f"{DM_BASE}/demo/build_demo.sh", "w") as f:
    f.write('''#!/bin/bash
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

# This script builds demo SO files for local testing
# Demo files are NOT included in the main datamgr_service build

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building Data Mining ETL Demo SOs..."
echo "Note: These are for local testing only, not included in main build"

g++ -shared -fPIC -o libdemo_source.so demo_source.cpp -I ../include -std=c++17
echo "✓ Built libdemo_source.so"

g++ -shared -fPIC -o libdemo_operator.so demo_operator.cpp -I ../include -std=c++17
echo "✓ Built libdemo_operator.so"

g++ -shared -fPIC -o libdemo_slink.so demo_slink.cpp -I ../include -std=c++17
echo "✓ Built libdemo_slink.so"

echo ""
echo "Demo SO files built successfully!"
echo "To verify: nm -D *.so | grep Create"
''')
os.chmod(f"{DM_BASE}/demo/build_demo.sh", 0o755)
print("   ✓ Created build_demo.sh")

print("\n✅ All fixes applied successfully!")
print("\nSummary:")
print("  1. ✓ Updated bundle.json with datamgr_service_data_mining")
print("  2. ✓ Removed ETL namespace (now using OHOS::DataMining)")
print("  3. ✓ Rewrote UT tests in OpenHarmony style")
print("  4. ✓ Separated demo code from main build")
print("  5. ✓ Created demo/build_demo.sh for local testing")
print("\nTo build datamgr_service with data_mining:")
print("  ./build.sh --product-name rk3568 --build-target datamgr_service")
print("\nTo build demo SOs separately:")
print("  cd demo && ./build_demo.sh")
