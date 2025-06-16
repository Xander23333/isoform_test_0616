# Python REST API 服务

这是一个简单的REST API服务，提供两个POST接口。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口

### POST /flags
接收JSON格式的数据

### POST /evaluate
接收JSON格式的数据

## 示例请求

使用curl测试接口：

```bash
# 测试 /flags 接口
curl -X POST http://localhost:5000/flags \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# 测试 /evaluate 接口
curl -X POST http://localhost:5000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
``` 