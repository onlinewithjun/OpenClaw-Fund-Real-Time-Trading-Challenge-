#!/bin/bash
# 修复所有日志宏 - 去掉_MACRO 后缀

# 修复 pipeline.cpp
sed -i 's/ZLOGD_MACRO/ZLOGD/g; s/ZLOGI_MACRO/ZLOGI/g; s/ZLOGW_MACRO/ZLOGW/g; s/ZLOGE_MACRO/ZLOGE/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp

echo "Fixed pipeline.cpp - removed _MACRO suffix"

# 验证
grep 'ZLOG' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp | head -5

echo "All log macros fixed!"
