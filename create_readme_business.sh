#!/bin/bash
# 重写 data_mining 的 README.md - 专注于业务逻辑

cat > /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/README.md << 'EOF'
# Data Mining ETL Framework

数据挖掘 ETL（Extract-Transform-Load）框架，为 OpenHarmony 分布式数据管理服务提供灵活的数据处理和转换能力。

## 业务架构

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                     应用层 (Application)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Pipeline 引擎 (PipelineEngine)               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  配置解析   │  │  动态库加载  │  │  生命周期管理 │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    节点执行层 (Node Layer)                    │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Source  │───▶│ Operator │───▶│  Slink   │              │
│  │  (数据源) │    │ (数据处理)│    │ (数据输出)│              │
│  └──────────┘    └──────────┘    └──────────┘              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据存储层 (Storage Layer)                  │
│         文件系统 / 数据库 / 网络 / 其他数据源                   │
└─────────────────────────────────────────────────────────────┘
```

## 核心业务流程

### 数据流向图

```
┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐
│ 数据源 1 │─────▶│         │      │         │      │         │
└─────────┘      │         │      │         │      │         │
                 │         │      │         │      │         │
┌─────────┐      │         │      │         │      │         │
│ 数据源 2 │─────▶│ Source  │─────▶│Operator│─────▶│ Slink   │
└─────────┘      │         │      │         │      │         │
                 │         │      │         │      │         │
┌─────────┐      │         │      │         │      │         │
│ 数据源 3 │─────▶│         │      │         │      │         │
└─────────┘      └─────────┘      └─────────┘      └─────────┘
                                    │
                                    ▼
                              ┌─────────┐
                              │ 输出结果 │
                              └─────────┘
```

## 核心组件说明

### 1. Source（数据源）

**职责**: 负责数据的采集和输入

**典型场景**:
- 从数据库读取数据
- 从文件加载数据
- 从网络接口获取数据
- 监听事件产生数据

**生命周期**:
```
OnInitialize() → Subscribe() → Trigger() → UnSubscribe() → OnStop()
```

### 2. Operator（数据处理器）

**职责**: 负责数据的转换、计算和处理

**典型场景**:
- 数据格式转换（JSON ↔ XML）
- 数据过滤和筛选
- 数据聚合和统计
- 数据加密和解密
- 业务逻辑处理

**处理模式**:
- **同步处理**: `Process(Context, input)` - 直接返回处理结果
- **异步处理**: `Process(Context, input, asyncData)` - 通过回调通知结果

### 3. Slink（数据输出）

**职责**: 负责数据的保存和输出

**典型场景**:
- 保存到文件系统
- 写入数据库
- 发送到网络接口
- 生成报表或日志

## Pipeline 执行流程

### 时序图

```
应用层              Pipeline 引擎              Source            Operator           Slink
  │                     │                       │                   │                  │
  │──Initialize()──────▶│                       │                   │                  │
  │                     │──解析配置文件─────────▶│                   │                  │
  │                     │──加载动态库───────────▶│                   │                  │
  │                     │──创建节点实例─────────▶│                   │                  │
  │                     │                       │                   │                  │
  │──Start()──────────▶│                       │                   │                  │
  │                     │                       │                   │                  │
  │──Trigger()────────▶│                       │                   │                  │
  │                     │──Trigger()──────────▶│                   │                  │
  │                     │                       │                   │                  │
  │                     │                    产生数据               │                  │
  │                     │──(数据)─────────────▶│                   │                  │
  │                     │                       │                   │                  │
  │                     │                       │──Process()──────▶│                  │
  │                     │                       │                   │ 处理数据         │
  │                     │                       │◀──(结果)─────────│                  │
  │                     │                       │                   │                  │
  │                     │                       │──Save()────────────────────────────▶│
  │                     │                       │                   │                  │ 保存数据
  │                     │                       │                   │                  │
  │──Stop()───────────▶│                       │                   │                  │
  │                     │──OnStop()───────────▶│                   │                  │
  │                     │                       │                   │                  │
```

### 节点执行流程图

```
开始
  │
  ▼
┌─────────────────┐
│  Initialize()   │  ← 解析配置文件
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LoadLibraries()│  ← 加载 SO 文件
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ CreateOperators()│  ← 创建节点实例
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BuildGraph()   │  ← 构建执行图
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Start()      │  ← 启动 Pipeline
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Trigger│
    └───┬────┘
        │
        ▼
   ┌──────────┐
   │  Source  │  ← 产生数据
   └────┬─────┘
        │
        ▼
   ┌──────────┐
   │ Operator │  ← 处理数据
   └────┬─────┘
        │
        ▼
   ┌──────────┐
   │  Slink   │  ← 保存数据
   └────┬─────┘
        │
        ▼
┌─────────────────┐
│     Stop()      │
└─────────────────┘
        │
        ▼
       结束
```

## 典型应用场景

### 场景 1: 数据同步

```
[数据库 A] → [Source] → [Operator: 格式转换] → [Slink] → [数据库 B]
```

**用途**: 将数据从一个数据库同步到另一个数据库，并进行格式转换

### 场景 2: 数据清洗

```
[原始数据] → [Source] → [Operator: 过滤] → [Operator: 验证] → [Slink] → [干净数据]
```

**用途**: 对原始数据进行清洗、过滤和验证

### 场景 3: 实时数据处理

```
[事件源] → [Source: 监听] → [Operator: 实时计算] → [Slink: 实时推送]
```

**用途**: 实时监听事件并进行处理和推送

### 场景 4: 批量数据处理

```
[文件列表] → [Source: 批量读取] → [Operator: 批量处理] → [Slink: 批量写入]
```

**用途**: 批量处理大量数据文件

## 配置说明

### Pipeline 配置结构

```json
{
    "pipeline": {
        "name": "pipeline 名称",
        "description": "pipeline 描述",
        "trigger": {
            "type": "触发类型 (manual/auto/schedule)"
        }
    },
    "operators": [
        {
            "name": "operator 名称",
            "type": "类型 (source/operator/slink)",
            "library": "SO 文件路径",
            "create_symbol": "创建函数名",
            "destroy_symbol": "销毁函数名",
            "parameters": {
                "参数名": "参数值"
            }
        }
    ],
    "nodes": [
        {
            "name": "节点名称",
            "type": "节点类型",
            "operator": "引用的 operator",
            "parameters": {
                "节点参数"
            },
            "next": ["下一个节点名称"]
        }
    ]
}
```

## 数据传递机制

### Context（上下文）

用于在节点间传递数据：

```cpp
// 设置数据
context.Set("key", std::any(value));

// 获取数据
auto value = std::any_cast<Type>(context.Get("key"));

// 检查是否存在
if (context.Has("key")) {
    // ...
}
```

### AsyncData（异步通知）

用于异步事件通知：

```cpp
// 设置回调
asyncData->SetNotifyCallback([](Context &ctx, const std::string &event, const std::any &data) {
    // 处理异步事件
});

// 触发通知
asyncData->Notify(context, "event_name", data);
```

## 扩展开发

### 开发自定义 Operator

1. 继承 `Operator` 基类
2. 实现 `Process()` 方法
3. 导出 C 接口（Create/Destroy 函数）
4. 编译为 SO 文件
5. 在配置文件中引用

### 开发自定义 Source

1. 继承 `Source` 基类
2. 实现 `Trigger()` 方法（产生数据）
3. 可选实现 `Subscribe()`/`UnSubscribe()`（事件订阅）
4. 导出 C 接口

### 开发自定义 Slink

1. 继承 `Slink` 基类
2. 实现 `Save()` 方法（保存数据）
3. 导出 C 接口

## 安全特性

- **输入验证**: 所有外部输入都经过严格验证
- **空指针检查**: 所有指针使用前都进行 nullptr 检查
- **CFI 保护**: 启用控制流完整性保护
- **内存安全**: 使用智能指针管理内存

## 相关文件

- `include/etl_interfaces.h`: ETL 接口定义
- `include/pipeline.h`: Pipeline 引擎接口
- `src/etl_interfaces.cpp`: ETL 接口实现
- `src/pipeline.cpp`: Pipeline 引擎实现
- `pipeline/demo_pipeline.json`: 示例配置文件
- `demo/`: 示例代码

## 许可证

Copyright (c) 2026 Huawei Device Co., Ltd.

Licensed under the Apache License, Version 2.0.
EOF

echo "Created README.md with business logic focus"
echo ""
echo "=== README.md 文件统计 ==="
wc -l /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/README.md
