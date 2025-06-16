# Feature Flag Service

## 项目描述
这是一个基于Flask的Feature Flag服务，采用MVC架构，用于管理用户的功能标志。该服务支持通过API添加和更新标志，并根据用户属性评估标志的状态。

## 功能
- 添加和更新功能标志
- 根据用户属性评估标志状态
- 支持灰度发布

## 项目结构
- **Model**: 数据模型定义在 `models.py` 中
- **Service**: 业务逻辑在 `service.py` 中
- **Controller**: API响应和错误处理在 `controllers.py` 中

## 使用说明
1. 启动服务：
   ```bash
   python controllers.py
   ```

2. 添加或更新标志：
   ```bash
   curl -X POST http://localhost:5001/flags -H "Content-Type: application/json" -d '{"name": "new_feature", "rules": [{"conditions": [{"column": "region", "operator": "=", "value": "us"}, {"column": "tier", "operator": "=", "value": "pro"}], "rollout": 20, "priority": 1}], "default": false}'
   ```

3. 评估标志：
   ```bash
   curl -X POST http://localhost:5001/evaluate -H "Content-Type: application/json" -d '{"user_id": "user15", "flag": "new_feature"}'
   ```

## 测试
运行测试用例：
```bash
pytest test.py
```

## 注意事项
- 确保在运行测试之前，服务已经启动。
- 当前实现中，标志数据存储在内存中，服务重启后数据会丢失。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```