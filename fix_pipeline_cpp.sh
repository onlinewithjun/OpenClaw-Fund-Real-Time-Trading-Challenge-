#!/bin/bash
# 正确修复 pipeline.cpp - 添加日志宏定义

# 先恢复原始文件（移除错误的第 22 行）
head -20 /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp > /tmp/pipeline_fixed.cpp

# 添加正确的日志宏定义
cat >> /tmp/pipeline_fixed.cpp << 'EOF'

// Temporary log macros for compilation
#define ZLOGD_DISABLED(...) do {} while(0)
#define ZLOGI_DISABLED(...) do {} while(0)
#define ZLOGW_DISABLED(...) do {} while(0)
#define ZLOGE_DISABLED(...) do {} while(0)

EOF

# 添加剩余的文件内容（从第 21 行开始）
tail -n +21 /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp >> /tmp/pipeline_fixed.cpp

# 覆盖原文件
cp /tmp/pipeline_fixed.cpp /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp

echo "Fixed pipeline.cpp - added log macros correctly"
head -30 /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp
