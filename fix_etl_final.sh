#!/bin/bash
# 修复 etl_interfaces.cpp 的 LOG_TAG 位置

FILE="/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/etl_interfaces.cpp"

# 重新创建正确的文件
cat > /tmp/etl_fixed.cpp << 'EOF'
/*
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

#define LOG_TAG "ETLInterfaces"
#include "etl_interfaces.h"

namespace OHOS {
namespace DataMining {

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

} // namespace DataMining
} // namespace OHOS
EOF

cp /tmp/etl_fixed.cpp "$FILE"
echo "Fixed etl_interfaces.cpp"
head -20 "$FILE"
