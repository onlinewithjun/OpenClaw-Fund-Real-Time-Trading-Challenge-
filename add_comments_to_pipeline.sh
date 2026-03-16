#!/bin/bash
# 为 pipeline.cpp 添加详细的中文注释

cat > /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp << 'EOF'
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

/**
 * @file pipeline.cpp
 * @brief Pipeline 引擎实现文件
 * 
 * 本文件实现了 ETL 框架的核心引擎，负责：
 * 1. 解析 JSON 配置文件
 * 2. 加载动态库（SO 文件）
 * 3. 创建和管理算子实例
 * 4. 构建执行图
 * 5. 执行数据流处理
 * 6. 生命周期管理
 */

#define LOG_TAG "PipelineEngine"
#include "pipeline.h"
#include "log_print.h"
#include <fstream>
#include <sstream>

namespace OHOS {
namespace DataMining {

/**
 * @brief 从 JSON 字符串中提取指定 key 的字符串值
 * 
 * @param json JSON 格式的字符串
 * @param key 要查找的键名
 * @return 提取的字符串值，如果找不到则返回空字符串
 * 
 * @note 这是一个简易的 JSON 解析器，仅支持基本的键值对提取
 *       复杂配置建议使用专业 JSON 库（如 nlohmann/json）
 * 
 * @example
 * // JSON: {"name": "test", "value": "123"}
 * ExtractStringValue(json, "name") 返回 "test"
 * ExtractStringValue(json, "value") 返回 "123"
 */
static std::string ExtractStringValue(const std::string &json, const std::string &key)
{
    // 输入验证：检查 JSON 字符串和 key 是否为空
    if (json.empty() || key.empty()) {
        return "";
    }

    // 构造搜索键（JSON 格式："key"）
    std::string searchKey = "\"" + key + "\"";
    
    // 查找键的位置
    size_t keyPos = json.find(searchKey);
    if (keyPos == std::string::npos) {
        // 未找到键，返回空字符串
        return "";
    }

    // 查找冒号位置
    size_t colonPos = json.find(':', keyPos);
    if (colonPos == std::string::npos) {
        return "";
    }

    // 查找起始引号
    size_t startQuote = json.find('"', colonPos);
    if (startQuote == std::string::npos) {
        return "";
    }

    // 查找结束引号
    size_t endQuote = json.find('"', startQuote + 1);
    if (endQuote == std::string::npos) {
        return "";
    }

    // 提取引号内的字符串值
    return json.substr(startQuote + 1, endQuote - startQuote - 1);
}

/**
 * @brief PipelineEngine 构造函数
 * 
 * 初始化 Pipeline 引擎，设置默认状态
 */
PipelineEngine::PipelineEngine()
{
    ZLOGD("PipelineEngine constructor called");
}

/**
 * @brief PipelineEngine 析构函数
 * 
 * 自动清理所有资源，包括：
 * 1. 关闭所有动态库
 * 2. 释放所有算子实例
 * 3. 清空所有容器
 */
PipelineEngine::~PipelineEngine()
{
    ZLOGD("PipelineEngine destructor called, cleaning up resources");
    Cleanup();
}

/**
 * @brief 初始化 Pipeline 引擎
 * 
 * 这是使用 Pipeline 的第一步，负责：
 * 1. 验证并解析配置文件
 * 2. 加载所有动态库
 * 3. 创建算子实例
 * 4. 构建执行图
 * 
 * @param configPath JSON 配置文件的完整路径
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 初始化成功后必须调用 Start() 才能执行 Pipeline
 * 
 * @example
 * PipelineEngine engine;
 * int ret = engine.Initialize("/path/to/config.json");
 * if (ret == 0) {
 *     engine.Start();
 * }
 */
int PipelineEngine::Initialize(const std::string &configPath)
{
    // 输入验证 1：检查配置文件路径是否为空
    if (configPath.empty()) {
        ZLOGE("Config path is empty");
        return -1;
    }

    // 输入验证 2：检查路径长度（防止缓冲区溢出）
    if (!ValidateString(configPath, MAX_CONFIG_STRING_LENGTH)) {
        ZLOGE("Config path is too long");
        return -1;
    }

    ZLOGD("PipelineEngine::Initialize - Loading config: %{public}s", configPath.c_str());

    // 创建配置对象
    PipelineConfig config;
    
    // 解析配置文件
    int ret = ParseConfig(configPath, config);
    if (ret != 0) {
        ZLOGE("Failed to parse config file: %{public}s", configPath.c_str());
        return -1;
    }

    // 验证解析后的配置
    if (!ValidateString(config.name, MAX_CONFIG_STRING_LENGTH)) {
        ZLOGE("Invalid pipeline name");
        return -1;
    }

    // 保存配置信息
    name_ = config.name;
    description_ = config.description;
    triggerType_ = config.triggerType;

    ZLOGD("Pipeline name: %{public}s, trigger type: %{public}s", 
          name_.c_str(), triggerType_.c_str());

    // 加载动态库
    ret = LoadLibraries(config);
    if (ret != 0) {
        ZLOGE("Failed to load libraries");
        return -1;
    }

    // 创建算子实例
    ret = CreateOperators(config);
    if (ret != 0) {
        ZLOGE("Failed to create operators");
        return -1;
    }

    // 构建执行图
    ret = BuildExecutionGraph(config);
    if (ret != 0) {
        ZLOGE("Failed to build execution graph");
        return -1;
    }

    ZLOGI("PipelineEngine initialized successfully: %{public}s", name_.c_str());
    return 0;
}

/**
 * @brief 启动 Pipeline
 * 
 * 将 Pipeline 设置为运行状态，准备执行数据处理
 * 
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 启动后才能调用 Trigger() 执行数据处理
 * 
 * @see Stop() - 停止 Pipeline
 */
int PipelineEngine::Start()
{
    // 检查是否已经在运行
    if (isRunning_) {
        ZLOGW("Pipeline is already running");
        return -1;
    }

    ZLOGI("PipelineEngine::Start - Starting pipeline: %{public}s", name_.c_str());
    
    // 设置运行状态
    isRunning_ = true;

    // 如果是自动触发模式，记录日志
    if (triggerType_ == "auto") {
        ZLOGD("Auto-trigger mode: pipeline will run automatically");
    }

    return 0;
}

/**
 * @brief 停止 Pipeline
 * 
 * 将 Pipeline 设置为停止状态，并停止所有 Source 节点
 * 
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 停止后可以再次调用 Start() 重新启动
 */
int PipelineEngine::Stop()
{
    // 如果已经停止，直接返回
    if (!isRunning_) {
        return 0;
    }

    ZLOGI("PipelineEngine::Stop - Stopping pipeline: %{public}s", name_.c_str());

    // 停止所有 Source 节点
    for (auto &pair : sourceNodes_) {
        if (pair.second.instance != nullptr) {
            pair.second.instance->OnStop();
        }
    }

    // 重置运行状态
    isRunning_ = false;
    
    ZLOGD("Pipeline stopped successfully");
    return 0;
}

/**
 * @brief 手动触发 Pipeline 执行
 * 
 * 适用于手动触发（manual）类型的 Pipeline，执行完整的数据处理流程：
 * 1. 触发所有 Source 节点产生数据
 * 2. 数据经过 Operator 处理
 * 3. 最终由 Sink 节点保存
 * 
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 必须在 Start() 之后调用
 * 
 * @see Start() - 启动 Pipeline
 */
int PipelineEngine::Trigger()
{
    // 检查是否在运行状态
    if (!isRunning_) {
        ZLOGW("Pipeline is not running, cannot trigger");
        return -1;
    }

    ZLOGI("PipelineEngine::Trigger - Manual trigger for: %{public}s", name_.c_str());

    // 检查是否有 Source 节点
    if (sourceNodes_.empty()) {
        ZLOGE("No source nodes found");
        return -1;
    }

    // 创建执行上下文（用于在节点间传递数据）
    Context context;
    
    // 创建异步数据通知对象
    auto asyncData = std::make_shared<AsyncData>();

    // 设置异步通知回调函数
    asyncData->SetNotifyCallback([](Context &ctx, const std::string &event, const std::any &data) {
        ZLOGD("Async event: %{public}s", event.c_str());
        (void)ctx;
        (void)data;
    });

    // 触发所有 Source 节点
    for (auto &pair : sourceNodes_) {
        if (pair.second.instance != nullptr) {
            // 调用 Source 的 Trigger 方法产生数据
            int ret = pair.second.instance->Trigger(context, asyncData);
            if (ret != 0) {
                ZLOGE("Source trigger failed: %{public}s", pair.first.c_str());
                return -1;
            }
        }
    }

    ZLOGD("Pipeline trigger completed successfully");
    return 0;
}

/**
 * @brief 获取 Pipeline 名称
 * 
 * @return const std::string& Pipeline 的名称
 */
const std::string &PipelineEngine::GetName() const
{
    return name_;
}

/**
 * @brief 解析 JSON 配置文件
 * 
 * 读取并解析配置文件，提取 Pipeline 的基本信息和结构
 * 
 * @param configPath 配置文件路径
 * @param config 输出参数，解析后的配置对象
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 当前使用简易解析器，仅支持基本字段提取
 */
int PipelineEngine::ParseConfig(const std::string &configPath, PipelineConfig &config)
{
    // 打开配置文件
    std::ifstream file(configPath);
    if (!file.is_open()) {
        ZLOGE("Cannot open config file: %{public}s", configPath.c_str());
        return -1;
    }

    // 读取整个文件内容到字符串
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string jsonContent = buffer.str();
    file.close();

    // 验证文件大小
    if (jsonContent.empty()) {
        ZLOGE("Config file is empty");
        return -1;
    }

    if (jsonContent.length() > MAX_CONFIG_STRING_LENGTH) {
        ZLOGE("Config file is too large");
        return -1;
    }

    // 提取基本信息
    config.name = ExtractStringValue(jsonContent, "name");
    config.description = ExtractStringValue(jsonContent, "description");

    // 提取 trigger 类型
    size_t triggerPos = jsonContent.find("\"trigger\"");
    if (triggerPos != std::string::npos) {
        size_t typePos = jsonContent.find("\"type\"", triggerPos);
        if (typePos != std::string::npos) {
            config.triggerType = ExtractStringValue(jsonContent.substr(triggerPos, 200), "type");
        }
    }

    ZLOGI("Parsed pipeline config: %{public}s, trigger: %{public}s", 
          config.name.c_str(), config.triggerType.c_str());

    return 0;
}

/**
 * @brief 加载所有动态库
 * 
 * 遍历配置中的所有算子，加载对应的 SO 文件
 * 
 * @param config Pipeline 配置
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 使用 dlopen 加载动态库，失败时返回 nullptr
 */
int PipelineEngine::LoadLibraries(const PipelineConfig &config)
{
    ZLOGD("Loading %{public}zu libraries", config.operators.size());

    // 遍历所有算子配置
    for (const auto &opConfig : config.operators) {
        // 检查是否已加载（避免重复加载）
        if (libraries_.find(opConfig.name) != libraries_.end()) {
            ZLOGD("Library already loaded: %{public}s", opConfig.name.c_str());
            continue;
        }

        // 验证库路径
        if (!ValidateString(opConfig.library, MAX_CONFIG_STRING_LENGTH)) {
            ZLOGE("Invalid library path: %{public}s", opConfig.library.c_str());
            return -1;
        }

        // 创建库句柄
        auto libHandle = std::make_unique<LibraryHandle>();
        libHandle->path = opConfig.library;

        // 使用 dlopen 加载动态库
        // RTLD_NOW: 立即解析所有符号
        libHandle->handle = dlopen(opConfig.library.c_str(), RTLD_NOW);
        if (libHandle->handle == nullptr) {
            // 加载失败，记录错误信息
            ZLOGE("Failed to load library: %{public}s, error: %{public}s", 
                  opConfig.library.c_str(), dlerror());
            return -1;
        }

        // 保存库句柄
        libraries_[opConfig.name] = std::move(libHandle);
        ZLOGI("Loaded library: %{public}s", opConfig.library.c_str());
    }

    ZLOGD("All libraries loaded successfully");
    return 0;
}

/**
 * @brief 创建所有算子实例
 * 
 * 根据配置创建 Source、Operator、Sink 实例
 * 
 * @param config Pipeline 配置
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 使用 dlsym 查找导出函数（CreateXXX/DestroyXXX）
 */
int PipelineEngine::CreateOperators(const PipelineConfig &config)
{
    ZLOGD("Creating operators from %{public}zu configurations", config.operators.size());

    // 遍历所有算子配置
    for (const auto &opConfig : config.operators) {
        // 查找对应的库句柄
        auto it = libraries_.find(opConfig.name);
        if (it == libraries_.end() || it->second->handle == nullptr) {
            ZLOGW("Library not found: %{public}s", opConfig.name.c_str());
            continue;
        }

        // 根据算子类型创建不同的实例
        if (opConfig.type == "source") {
            // ========== 创建 Source 实例 ==========
            
            // 查找创建函数
            auto creator = reinterpret_cast<SourceCreator>(
                dlsym(it->second->handle, opConfig.createSymbol.c_str()));
            if (creator == nullptr) {
                ZLOGE("Failed to find creator symbol: %{public}s", opConfig.createSymbol.c_str());
                return -1;
            }

            // 创建实例
            SourceNode node;
            node.name = opConfig.name;
            node.instance.reset(creator());
            if (node.instance != nullptr) {
                node.instance->SetName(opConfig.name);
                sourceNodes_[opConfig.name] = std::move(node);
                ZLOGI("Created source: %{public}s", opConfig.name.c_str());
            }
        } else if (opConfig.type == "operator") {
            // ========== 创建 Operator 实例 ==========
            
            auto creator = reinterpret_cast<OperatorCreator>(
                dlsym(it->second->handle, opConfig.createSymbol.c_str()));
            if (creator == nullptr) {
                ZLOGE("Failed to find creator symbol: %{public}s", opConfig.createSymbol.c_str());
                return -1;
            }

            OperatorNode node;
            node.name = opConfig.name;
            node.instance.reset(creator());
            if (node.instance != nullptr) {
                node.instance->SetName(opConfig.name);
                operatorNodes_[opConfig.name] = std::move(node);
                ZLOGI("Created operator: %{public}s", opConfig.name.c_str());
            }
        } else if (opConfig.type == "sink") {
            // ========== 创建 Sink 实例 ==========
            
            auto creator = reinterpret_cast<SinkCreator>(
                dlsym(it->second->handle, opConfig.createSymbol.c_str()));
            if (creator == nullptr) {
                ZLOGE("Failed to find creator symbol: %{public}s", opConfig.createSymbol.c_str());
                return -1;
            }

            SinkNode node;
            node.name = opConfig.name;
            node.instance.reset(creator());
            if (node.instance != nullptr) {
                node.instance->SetName(opConfig.name);
                sinkNodes_[opConfig.name] = std::move(node);
                ZLOGI("Created sink: %{public}s", opConfig.name.c_str());
            }
        } else {
            // 未知的算子类型
            ZLOGW("Unknown operator type: %{public}s", opConfig.type.c_str());
        }
    }

    // 记录创建的节点数量
    ZLOGD("Created %{public}zu sources, %{public}zu operators, %{public}zu sinks",
          sourceNodes_.size(), operatorNodes_.size(), sinkNodes_.size());
    return 0;
}

/**
 * @brief 构建节点执行图
 * 
 * 根据配置中的节点连接关系，建立节点间的执行顺序
 * 
 * @param config Pipeline 配置
 * @return int 成功返回 0，失败返回 -1
 * 
 * @note 执行图决定了数据流动的方向
 */
int PipelineEngine::BuildExecutionGraph(const PipelineConfig &config)
{
    ZLOGD("Building execution graph with %{public}zu nodes", config.nodes.size());

    // 遍历所有节点配置
    for (const auto &nodeConfig : config.nodes) {
        // 验证节点名称
        if (!ValidateString(nodeConfig.name, MAX_CONFIG_STRING_LENGTH)) {
            ZLOGW("Invalid node name");
            continue;
        }

        // 记录节点类型映射（用于 ExecuteNode 查找）
        nodeTypeMap_[nodeConfig.name] = nodeConfig.type;

        // 根据节点类型设置后续节点
        if (nodeConfig.type == "source") {
            auto it = sourceNodes_.find(nodeConfig.operatorRef);
            if (it != sourceNodes_.end()) {
                it->second.nextNodes = nodeConfig.nextNodes;
            }
        } else if (nodeConfig.type == "operator") {
            auto it = operatorNodes_.find(nodeConfig.operatorRef);
            if (it != operatorNodes_.end()) {
                it->second.nextNodes = nodeConfig.nextNodes;
            }
        }
        // Sink 节点没有后续节点
    }

    ZLOGI("Execution graph built successfully");
    return 0;
}

/**
 * @brief 执行单个节点
 * 
 * 根据节点类型执行相应的操作：
 * - Source: 调用 OnInitialize()
 * - Operator: 调用 Process()
 * - Sink: 调用 Save()
 * 
 * @param nodeName 节点名称
 * @param context 执行上下文（用于传递数据）
 * @return int 成功返回 0，失败返回 -1
 */
int PipelineEngine::ExecuteNode(const std::string &nodeName, Context &context)
{
    // 验证节点名称
    if (!ValidateString(nodeName, MAX_CONFIG_STRING_LENGTH)) {
        ZLOGW("Invalid node name");
        return -1;
    }

    // 查找节点类型
    auto typeIt = nodeTypeMap_.find(nodeName);
    if (typeIt == nodeTypeMap_.end()) {
        ZLOGW("Unknown node: %{public}s", nodeName.c_str());
        return -1;
    }

    const std::string &type = typeIt->second;

    // 根据节点类型执行相应操作
    if (type == "source") {
        auto it = sourceNodes_.find(nodeName);
        if (it != sourceNodes_.end() && it->second.instance != nullptr) {
            return it->second.instance->OnInitialize();
        }
    } else if (type == "operator") {
        auto it = operatorNodes_.find(nodeName);
        if (it != operatorNodes_.end() && it->second.instance != nullptr) {
            return it->second.instance->Process(context, std::any());
        }
    } else if (type == "sink") {
        auto it = sinkNodes_.find(nodeName);
        if (it != sinkNodes_.end() && it->second.instance != nullptr) {
            return it->second.instance->Save(context, std::any());
        }
    }

    ZLOGW("Failed to execute node: %{public}s", nodeName.c_str());
    return -1;
}

/**
 * @brief 验证字符串输入
 * 
 * 检查字符串是否有效（非空且不超过最大长度）
 * 
 * @param str 待验证的字符串
 * @param maxLength 最大允许长度
 * @return bool 有效返回 true，无效返回 false
 */
bool PipelineEngine::ValidateString(const std::string &str, size_t maxLength) const
{
    if (str.empty()) {
        return false;
    }
    if (str.length() > maxLength) {
        return false;
    }
    return true;
}

/**
 * @brief 清理所有资源
 * 
 * 析构时调用，负责：
 * 1. 关闭所有动态库（dlclose）
 * 2. 清空所有容器
 * 3. 重置运行状态
 * 
 * @note 由析构函数自动调用
 */
void PipelineEngine::Cleanup()
{
    ZLOGD("Cleaning up PipelineEngine resources");

    // 关闭所有动态库
    for (auto &pair : libraries_) {
        if (pair.second->handle != nullptr) {
            dlclose(pair.second->handle);
            // 设置为 nullptr 防止悬空指针
            pair.second->handle = nullptr;
        }
    }

    // 清空所有容器（智能指针会自动释放内存）
    libraries_.clear();
    sourceNodes_.clear();
    operatorNodes_.clear();
    sinkNodes_.clear();
    nodeTypeMap_.clear();
    
    // 重置运行状态
    isRunning_ = false;

    ZLOGD("Cleanup completed");
}

} // namespace DataMining
} // namespace OHOS
EOF

echo "Added detailed Chinese comments to pipeline.cpp"
echo ""
echo "=== File statistics ==="
wc -l /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp
