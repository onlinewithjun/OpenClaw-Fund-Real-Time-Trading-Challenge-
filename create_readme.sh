#!/bin/bash
# 创建 data_mining 的 README.md

cat > /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/README.md << 'EOF'
# Data Mining ETL Framework

数据挖掘 ETL（Extract-Transform-Load）框架，为 OpenHarmony 分布式数据管理服务提供数据处理和转换能力。

## 目录结构

```
data_mining/
├── BUILD.gn              # GN 构建配置
├── README.md             # 本说明文档
├── include/              # 头文件目录
│   ├── etl_interfaces.h  # ETL 接口定义
│   └── pipeline.h        # Pipeline 引擎头文件
├── src/                  # 源代码目录
│   ├── etl_interfaces.cpp # ETL 接口实现
│   └── pipeline.cpp      # Pipeline 引擎实现
├── demo/                 # 示例代码
│   ├── demo_source.cpp   # Source 示例
│   ├── demo_operator.cpp # Operator 示例
│   ├── demo_slink.cpp    # Slink 示例
│   └── build_demo.sh     # 构建脚本
├── pipeline/             # Pipeline 配置
│   └── demo_pipeline.json # 示例配置
└── test/                 # 单元测试
    ├── interfaces_test.cpp
    └── pipeline_test.cpp
```

## 核心组件

### 1. ETL 接口 (`etl_interfaces.h`)

定义了 ETL 框架的基础接口：

- **Context**: 执行上下文，用于在节点间传递数据
- **AsyncData**: 异步数据通知机制
- **Source**: 数据源接口，负责数据输入
- **Operator**: 数据操作接口，负责数据处理和转换
- **Slink**: 数据输出接口，负责数据保存

### 2. Pipeline 引擎 (`pipeline.h`)

Pipeline 引擎负责：
- 解析 JSON 配置文件
- 加载动态库（SO 文件）
- 创建和管理 Operator 实例
- 执行数据流转发
- 生命周期管理（Initialize/Start/Stop/Trigger）

### 3. 节点类型

- **Source**: 数据源节点，负责产生或获取数据
- **Operator**: 数据处理节点，负责数据转换和计算
- **Slink**: 数据输出节点，负责保存或发送数据

## 使用示例

### 1. 创建 Pipeline 配置

```json
{
    "pipeline": {
        "name": "demo_etl_pipeline",
        "description": "ETL 数据挖掘示例 Pipeline",
        "trigger": {
            "type": "manual"
        }
    },
    "operators": [
        {
            "name": "demo_source",
            "type": "source",
            "library": "/path/to/libdemo_source.so",
            "create_symbol": "CreateDemoSource",
            "destroy_symbol": "DestroyDemoSource"
        },
        {
            "name": "demo_operator",
            "type": "operator",
            "library": "/path/to/libdemo_operator.so",
            "create_symbol": "CreateDemoOperator",
            "destroy_symbol": "DestroyDemoOperator"
        },
        {
            "name": "demo_slink",
            "type": "slink",
            "library": "/path/to/libdemo_slink.so",
            "create_symbol": "CreateDemoSlink",
            "destroy_symbol": "DestroyDemoSlink"
        }
    ],
    "nodes": [
        {
            "name": "source_node",
            "type": "source",
            "operator": "demo_source",
            "next": ["operator_node"]
        },
        {
            "name": "operator_node",
            "type": "operator",
            "operator": "demo_operator",
            "next": ["slink_node"]
        },
        {
            "name": "slink_node",
            "type": "slink",
            "operator": "demo_slink",
            "next": []
        }
    ]
}
```

### 2. 使用 C++ 代码

```cpp
#include "pipeline.h"

using namespace OHOS::DataMining;

int main()
{
    // 创建 Pipeline 引擎
    Pipeline::PipelineEngine engine;
    
    // 初始化（加载配置文件）
    std::string configPath = "/path/to/pipeline.json";
    int ret = engine.Initialize(configPath);
    if (ret != 0) {
        ZLOGE("Failed to initialize pipeline");
        return -1;
    }
    
    // 启动 Pipeline
    engine.Start();
    
    // 手动触发（适用于 manual 触发类型）
    engine.Trigger();
    
    // 停止 Pipeline
    engine.Stop();
    
    return 0;
}
```

### 3. 自定义 Operator

```cpp
#define LOG_TAG "MyOperator"
#include "etl_interfaces.h"
#include "log_print.h"

namespace OHOS {
namespace DataMining {

class MyOperator : public Operator {
public:
    int Process(Context &context, const std::any &input, 
                std::shared_ptr<AsyncData> asyncData) override
    {
        (void)context;
        try {
            // 获取输入数据
            std::string inputStr = std::any_cast<std::string>(input);
            
            // 处理数据
            std::string outputStr = inputStr + "_processed";
            
            ZLOGI("Processed: %{public}s -> %{public}s", 
                  inputStr.c_str(), outputStr.c_str());
            
            // 通知异步事件
            if (asyncData != nullptr) {
                asyncData->Notify(context, "data_processed", outputStr);
            }
            
            return 0;
        } catch (const std::bad_any_cast &e) {
            ZLOGE("Invalid input type: %{public}s", e.what());
            return -1;
        }
    }
    
    std::any Process(Context &context, const std::any &input) override
    {
        (void)context;
        try {
            std::string inputStr = std::any_cast<std::string>(input);
            return std::any(std::string(inputStr + "_processed"));
        } catch (const std::bad_any_cast &e) {
            ZLOGE("Invalid input type: %{public}s", e.what());
            return std::any();
        }
    }
};

} // namespace DataMining
} // namespace OHOS

// 导出 C 接口
extern "C" {
    __attribute__((visibility("default"))) 
    OHOS::DataMining::Operator *CreateMyOperator()
    {
        return new OHOS::DataMining::MyOperator();
    }
    
    __attribute__((visibility("default"))) 
    void DestroyMyOperator(OHOS::DataMining::Operator *op)
    {
        delete op;
    }
}
```

## 构建说明

### 编译 data_mining 库

```bash
cd /home/lizhuojun/workspace/oh
./build.sh --product-name rk3568 --build-target datamgr_service
```

### 编译 Demo SO 文件

```bash
cd demo
./build_demo.sh
```

### 运行单元测试

```bash
cd /home/lizhuojun/workspace/oh
./build.sh --product-name rk3568 --build-target data_mining_unittest
```

## 依赖关系

- **hilog**: 日志系统 (`external_deps = [ "hilog:libhilog" ]`)
- **distributeddatasvcfwk**: 分布式数据服务框架

## 安全特性

- **CFI (Control Flow Integrity)**: 启用控制流完整性保护
- **UBSan (Undefined Behavior Sanitizer)**: 未定义行为检测
- **Boundary Sanitize**: 边界检查
- **输入验证**: 所有外部输入都经过严格验证
- **空指针检查**: 所有指针使用前都进行 nullptr 检查

## 编码规范

- 遵循 OpenHarmony C++ 编码规范
- 使用 `ZLOGD`/`ZLOGI`/`ZLOGW`/`ZLOGE` 进行日志记录
- 所有 if 语句都使用大括号
- 成员变量使用 `lowerCamelCase_` 命名
- 完整的中文注释

## 相关文件

- `etl_interfaces.h`: ETL 接口定义
- `pipeline.h`: Pipeline 引擎接口
- `demo_pipeline.json`: 示例配置文件
- `BUILD.gn`: GN 构建配置

## 联系方式

如有问题或建议，请联系 OpenHarmony 分布式数据管理服务团队。

## 许可证

Copyright (c) 2026 Huawei Device Co., Ltd.

Licensed under the Apache License, Version 2.0.
EOF

echo "Created README.md"
echo ""
echo "=== README.md 内容预览 ==="
head -50 /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/README.md
