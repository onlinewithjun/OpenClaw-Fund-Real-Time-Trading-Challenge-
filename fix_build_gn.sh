#!/bin/bash
# 修复 BUILD.gn 添加 data_mining 依赖

BUILD_FILE="/home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/BUILD.gn"

# 读取文件内容
head -119 "$BUILD_FILE" > /tmp/build_fixed.txt
echo '  deps += [ "//foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining:data_mining_etl" ]' >> /tmp/build_fixed.txt
tail -n +120 "$BUILD_FILE" >> /tmp/build_fixed.txt

# 覆盖原文件
cp /tmp/build_fixed.txt "$BUILD_FILE"

echo "BUILD.gn updated successfully"
sed -n '114,130p' "$BUILD_FILE"
