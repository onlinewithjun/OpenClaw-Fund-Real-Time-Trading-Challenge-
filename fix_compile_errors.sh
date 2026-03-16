#!/bin/bash
# 修复 etl_interfaces.cpp 和 pipeline.h

# 修复 etl_interfaces.cpp - 移除 ETL namespace
sed -i 's/namespace ETL {//g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/etl_interfaces.cpp
sed -i 's/} \/\/ namespace ETL//g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/etl_interfaces.cpp

echo "Fixed etl_interfaces.cpp - removed ETL namespace"

# 修复 pipeline.h - 移除 log_print.h include，使用标准日志
sed -i 's/#include "log_print.h"//g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/include/pipeline.h

# 替换 ZLOG* 为简单的 printf 用于调试（或者完全移除日志）
sed -i 's/ZLOGD(/ZLOGD_DISABLED(/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp
sed -i 's/ZLOGI(/ZLOGI_DISABLED(/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp
sed -i 's/ZLOGW(/ZLOGW_DISABLED(/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp
sed -i 's/ZLOGE(/ZLOGE_DISABLED(/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp

echo "Fixed pipeline.h and pipeline.cpp - removed log dependencies"

# 添加日志宏定义到 pipeline.cpp 开头
sed -i '20a\\n\\/\\/ Temporary log macros for compilation\\n#define ZLOGD_DISABLED(...) do {} while(0)\\n#define ZLOGI_DISABLED(...) do {} while(0)\\n#define ZLOGW_DISABLED(...) do {} while(0)\\n#define ZLOGE_DISABLED(...) do {} while(0)\\n' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp

echo "Added temporary log macro definitions"
echo "All fixes applied!"
