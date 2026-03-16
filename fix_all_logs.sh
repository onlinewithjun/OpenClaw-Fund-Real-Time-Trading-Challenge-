#!/bin/bash
# 修复 data_mining 所有文件的日志

# 修复 pipeline.h - 添加 log_print.h include
sed -i '/#include "etl_interfaces.h"/a #include "log_print.h"' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/include/pipeline.h

echo "Fixed pipeline.h"

# 修复 pipeline.cpp - 正确的日志格式
cat > /tmp/fix_pipeline_logs.sh << 'SCRIPT'
#!/bin/bash
FILE="/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp"

# 读取文件内容，删除错误的宏定义和 namespace 包装
head -15 "$FILE" > /tmp/pipeline_new.cpp
echo '#define LOG_TAG "PipelineEngine"' >> /tmp/pipeline_new.cpp
echo '#include "pipeline.h"' >> /tmp/pipeline_new.cpp
echo '#include "log_print.h"' >> /tmp/pipeline_new.cpp
echo '#include <fstream>' >> /tmp/pipeline_new.cpp
echo '#include <sstream>' >> /tmp/pipeline_new.cpp
echo '' >> /tmp/pipeline_new.cpp
echo 'namespace OHOS {' >> /tmp/pipeline_new.cpp
echo 'namespace DataMining {' >> /tmp/pipeline_new.cpp

# 跳过旧的头部（到第 29 行）
tail -n +30 "$FILE" | sed 's/ZLOGD_DISABLED/ZLOGD_MACRO/g; s/ZLOGI_DISABLED/ZLOGI_MACRO/g; s/ZLOGW_DISABLED/ZLOGW_MACRO/g; s/ZLOGE_DISABLED/ZLOGE_MACRO/g' >> /tmp/pipeline_new.cpp

cp /tmp/pipeline_new.cpp "$FILE"
echo "Fixed pipeline.cpp"
SCRIPT

chmod +x /tmp/fix_pipeline_logs.sh
/tmp/fix_pipeline_logs.sh

# 修复 etl_interfaces.cpp - 添加 LOG_TAG
cat > /tmp/fix_etl_logs.sh << 'SCRIPT'
#!/bin/bash
FILE="/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/etl_interfaces.cpp"

# 读取文件，在版权头后添加 LOG_TAG
head -13 "$FILE" > /tmp/etl_new.cpp
echo '#define LOG_TAG "ETLInterfaces"' >> /tmp/etl_new.cpp
tail -n +14 "$FILE" >> /tmp/etl_new.cpp

cp /tmp/etl_new.cpp "$FILE"
echo "Fixed etl_interfaces.cpp"
SCRIPT

chmod +x /tmp/fix_etl_logs.sh
/tmp/fix_etl_logs.sh

# 验证修复结果
echo "=== Verifying pipeline.cpp ==="
head -25 /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp

echo ""
echo "=== Verifying etl_interfaces.cpp ==="
head -20 /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/etl_interfaces.cpp

echo ""
echo "All log fixes applied!"
