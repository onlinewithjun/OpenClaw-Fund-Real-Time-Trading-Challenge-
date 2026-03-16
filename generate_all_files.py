#!/usr/bin/env python3
"""
Data Mining ETL Framework - Complete File Generator
Generates all source files with correct OpenHarmony copyright and coding style
"""

import os

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

# 1. etl_interfaces.h
with open(f"{BASE}/include/etl_interfaces.h", "w") as f:
    f.write(COPYRIGHT_CPP + '''
#ifndef OHOS_DISTRIBUTED_DATA_MGR_SERVICE_DATA_MINING_ETL_INTERFACES_H
#define OHOS_DISTRIBUTED_DATA_MGR_SERVICE_DATA_MINING_ETL_INTERFACES_H

#include <string>
#include <memory>
#include <functional>
#include <any>
#include <map>
#include <vector>

namespace OHOS {
namespace DataMining {
namespace ETL {

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

} // namespace ETL
} // namespace DataMining
} // namespace OHOS

#endif // OHOS_DISTRIBUTED_DATA_MGR_SERVICE_DATA_MINING_ETL_INTERFACES_H
''')
print("✓ Created etl_interfaces.h")

# 2. etl_interfaces.cpp
with open(f"{BASE}/src/etl_interfaces.cpp", "w") as f:
    f.write(COPYRIGHT_CPP + '''
#include "etl_interfaces.h"

namespace OHOS {
namespace DataMining {
namespace ETL {

// Context implementation
void Context::Set(const std::string &key, const std::any &value)
{
    data_[key] = value;
}

std::any Context::Get(const std::string &key) const
{
    auto it = data_.find(key);
    if (it != data_.end()) {
        return it->second;
    }
    return std::any();
}

bool Context::Has(const std::string &key) const
{
    return data_.find(key) != data_.end();
}

void Context::SetOperatorName(const std::string &name)
{
    operatorName_ = name;
}

const std::string &Context::GetOperatorName() const
{
    return operatorName_;
}

// AsyncData implementation
void AsyncData::SetNotifyCallback(NotifyCallback callback)
{
    notifyCallback_ = std::move(callback);
}

void AsyncData::Notify(Context &ctx, const std::string &event, const std::any &data)
{
    if (notifyCallback_) {
        notifyCallback_(ctx, event, data);
    }
}

// Source implementation
Source::Source() : name_("unknown_source") {}

Source::~Source() {}

const std::string &Source::GetName() const
{
    return name_;
}

void Source::SetName(const std::string &name)
{
    name_ = name;
}

// Operator implementation
Operator::Operator() : name_("unknown_operator") {}

Operator::~Operator() {}

const std::string &Operator::GetName() const
{
    return name_;
}

void Operator::SetName(const std::string &name)
{
    name_ = name;
}

// Slink implementation
Slink::Slink() : name_("unknown_slink") {}

Slink::~Slink() {}

const std::string &Slink::GetName() const
{
    return name_;
}

void Slink::SetName(const std::string &name)
{
    name_ = name;
}

} // namespace ETL
} // namespace DataMining
} // namespace OHOS
''')
print("✓ Created etl_interfaces.cpp")

# 3. demo_source.cpp
with open(f"{BASE}/demo/demo_source.cpp", "w") as f:
    f.write(COPYRIGHT_CPP + '''
#include "../include/etl_interfaces.h"
#include <iostream>

namespace OHOS {
namespace DataMining {
namespace ETL {

class DemoSource : public Source {
public:
    int OnInitialize() override
    {
        std::cout << "DemoSource::OnInitialize - " << name_ << std::endl;
        return 0;
    }

    int Trigger(Context &context, std::shared_ptr<AsyncData> asyncData) override
    {
        std::cout << "DemoSource::Trigger - " << name_ << std::endl;
        if (asyncData) {
            asyncData->Notify(context, "data_ready", std::string("Hello from DemoSource"));
        }
        return 0;
    }

    int Subscribe(Context &context, std::shared_ptr<AsyncData> asyncData) override
    {
        (void)context;
        (void)asyncData;
        return 0;
    }

    int UnSubscribe(Context &context) override
    {
        (void)context;
        return 0;
    }

    int OnStop() override
    {
        return 0;
    }
};

} // namespace ETL
} // namespace DataMining
} // namespace OHOS

extern "C" {
    __attribute__((visibility("default"))) OHOS::DataMining::ETL::Source *CreateDemoSource()
    {
        return new OHOS::DataMining::ETL::DemoSource();
    }

    __attribute__((visibility("default"))) void DestroyDemoSource(OHOS::DataMining::ETL::Source *source)
    {
        delete source;
    }
}
''')
print("✓ Created demo_source.cpp")

# 4. demo_operator.cpp
with open(f"{BASE}/demo/demo_operator.cpp", "w") as f:
    f.write(COPYRIGHT_CPP + '''
#include "../include/etl_interfaces.h"
#include <iostream>
#include <algorithm>

namespace OHOS {
namespace DataMining {
namespace ETL {

class DemoOperator : public Operator {
public:
    int Process(Context &context, const std::any &input, std::shared_ptr<AsyncData> asyncData) override
    {
        (void)context;
        try {
            std::string inputStr = std::any_cast<std::string>(input);
            std::string outputStr = inputStr;
            std::transform(outputStr.begin(), outputStr.end(), outputStr.begin(), ::toupper);
            std::cout << "DemoOperator::Process - " << inputStr << " -> " << outputStr << std::endl;
            if (asyncData) {
                asyncData->Notify(context, "data_processed", outputStr);
            }
            return 0;
        } catch (const std::bad_any_cast &e) {
            std::cerr << "Invalid input type: " << e.what() << std::endl;
            return -1;
        }
    }

    std::any Process(Context &context, const std::any &input) override
    {
        (void)context;
        try {
            std::string inputStr = std::any_cast<std::string>(input);
            std::string outputStr = inputStr;
            std::transform(outputStr.begin(), outputStr.end(), outputStr.begin(), ::toupper);
            return outputStr;
        } catch (const std::bad_any_cast &e) {
            std::cerr << "Invalid input type: " << e.what() << std::endl;
            return std::any();
        }
    }
};

} // namespace ETL
} // namespace DataMining
} // namespace OHOS

extern "C" {
    __attribute__((visibility("default"))) OHOS::DataMining::ETL::Operator *CreateDemoOperator()
    {
        return new OHOS::DataMining::ETL::DemoOperator();
    }

    __attribute__((visibility("default"))) void DestroyDemoOperator(OHOS::DataMining::ETL::Operator *op)
    {
        delete op;
    }
}
''')
print("✓ Created demo_operator.cpp")

# 5. demo_slink.cpp
with open(f"{BASE}/demo/demo_slink.cpp", "w") as f:
    f.write(COPYRIGHT_CPP + '''
#include "../include/etl_interfaces.h"
#include <iostream>
#include <fstream>

namespace OHOS {
namespace DataMining {
namespace ETL {

class DemoSlink : public Slink {
public:
    int Save(Context &context, const std::any &data) override
    {
        try {
            std::string dataStr = std::any_cast<std::string>(data);
            std::string savePath = "/tmp/data_mining_output.txt";
            if (context.Has("save_path")) {
                savePath = std::any_cast<std::string>(context.Get("save_path"));
            }
            std::ofstream outFile(savePath);
            if (outFile.is_open()) {
                outFile << dataStr << std::endl;
                outFile.close();
                std::cout << "DemoSlink::Save - Data saved to: " << savePath << std::endl;
                return 0;
            }
            std::cerr << "Failed to open file: " << savePath << std::endl;
            return -1;
        } catch (const std::bad_any_cast &e) {
            std::cerr << "Invalid data type: " << e.what() << std::endl;
            return -2;
        }
    }
};

} // namespace ETL
} // namespace DataMining
} // namespace OHOS

extern "C" {
    __attribute__((visibility("default"))) OHOS::DataMining::ETL::Slink *CreateDemoSlink()
    {
        return new OHOS::DataMining::ETL::DemoSlink();
    }

    __attribute__((visibility("default"))) void DestroyDemoSlink(OHOS::DataMining::ETL::Slink *slink)
    {
        delete slink;
    }
}
''')
print("✓ Created demo_slink.cpp")

print("\n✅ All source files created successfully!")
