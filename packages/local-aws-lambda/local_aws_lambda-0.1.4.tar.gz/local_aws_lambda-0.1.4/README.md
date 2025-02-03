# 🚀 Local AWS Lambda

**Local AWS Lambda** is a Python package that allows you to simulate AWS Lambda functions in your local development environment. This helps you test and debug your serverless applications without deploying them to AWS.

---

## 📦 Installation

```bash
pip install local-aws-lambda
```

---

## ⚡ Usage

### ✅ Basic Example

```python
from local_lambda import LocalLambda

def handler(event, context):
    return {"message": "Hello from Local AWS Lambda!", "event": event}

lambda_runtime = LocalLambda(handler)
event = {"key": "value"}
print(lambda_runtime.invoke(event))
```

---

## 🛠️ Configuration

You can customize the Lambda environment:

```python
lambda_runtime = LocalLambda(handler, timeout=5, memory=256)
```

- **`timeout`**: Max execution time (in seconds)
- **`memory`**: Simulated memory allocation (in MB)

---

## 🧪 Contributing

Contributions are welcome! 🚀

1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Open a Pull Request

---

## 🦢 Running Tests

```bash
pytest tests/
```

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## 🌐 Links

- [Homepage](https://www.aswath.dev/)
- 
- [PyPI Package](https://pypi.org/project/local-aws-lambda/)