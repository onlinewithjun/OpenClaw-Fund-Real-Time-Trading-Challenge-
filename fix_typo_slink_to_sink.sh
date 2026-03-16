#!/bin/bash
# 修复所有拼写错误：slink → sink

echo "Fixing typos: slink -> sink"

# 修复 etl_interfaces.h
sed -i 's/Slink/Sink/g; s/slink/sink/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/include/etl_interfaces.h

# 修复 etl_interfaces.cpp
sed -i 's/Slink/Sink/g; s/slink/sink/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/etl_interfaces.cpp

# 修复 pipeline.h
sed -i 's/SlinkNode/SinkNode/g; s/slinkNodes_/sinkNodes_/g; s/Slink/Sink/g; s/slink/sink/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/include/pipeline.h

# 修复 pipeline.cpp
sed -i 's/SlinkNode/SinkNode/g; s/slinkNodes_/sinkNodes_/g; s/Slink/Sink/g; s/slink/sink/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/src/pipeline.cpp

# 修复 demo 文件
sed -i 's/Slink/Sink/g; s/slink/sink/g; s/DemoSlink/DemoSink/g; s/demo_slink/demo_sink/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/demo/demo_slink.cpp

# 重命名 demo_slink.cpp 为 demo_sink.cpp
mv /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/demo/demo_slink.cpp /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/demo/demo_sink.cpp

# 修复 demo_pipeline.json
sed -i 's/slink/sink/g; s/demo_slink/demo_sink/g; s/DemoSlink/DemoSink/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/pipeline/demo_pipeline.json

# 修复 README.md
sed -i 's/Slink/Sink/g; s/slink/sink/g' /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/README.md

echo "All typos fixed!"
echo ""
echo "=== Verifying fixes ==="
echo "Checking etl_interfaces.h:"
grep -i "sink" /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/include/etl_interfaces.h | head -5

echo ""
echo "Checking pipeline.h:"
grep -i "sink" /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/include/pipeline.h | head -5

echo ""
echo "Checking demo files:"
ls -la /home/lizhuojun/workspace/oh/foundation/distributeddatamgr/datamgr_service/services/distributeddataservice/service/data_mining/demo/
