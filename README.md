# ClusterManagementSystem

基于 Flask 的 Linux 集群管理系统示例，包含管理端与集群端。管理端提供 YOLO 训练启动、集群生命周期管理、状态监控、分布式任务部署与状态大屏接口；集群端暴露训练与数据接收接口，便于与管理端交互。

## 快速开始

```bash
pip install -r requirements.txt
python run.py
```

- 管理端页面: `http://localhost:5000/management/`
- 集群端状态接口: `http://localhost:5000/agent/status`
- 集群状态大屏数据: `http://localhost:5000/management/status`

## 主要目录
- `app/management`: 管理端蓝图与接口
- `app/agent`: 集群端蓝图与接口
- `app/templates`: 管理端前端页面
- `app/static`: 前端样式与脚本
- `app/data_store.py`: 内存数据存储与模拟训练任务
