# FinanceKit Contributing Guide

感谢你对 FinanceKit 的兴趣！我们欢迎所有贡献。

## 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 开发指南

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/booo-wang/financekit.git
cd financekit

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"
```

### 代码风格

- 遵循 PEP 8 标准
- 使用类型注解
- 添加文档字符串

### 代码格式化

```bash
# 使用 black 格式化
black financekit/

# 使用 flake8 检查
flake8 financekit/

# 使用 mypy 进行类型检查
mypy financekit/
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_analysis.py -v

# 生成覆盖率报告
pytest tests/ --cov=financekit --cov-report=html
```

## 代码规范

### 提交消息

请使用清晰的提交消息：

```
feat: 添加新功能
fix: 修复错误
docs: 文档更新
test: 添加测试
refactor: 代码重构
```

### 文档

所有公开函数必须有文档字符串：

```python
def my_function(param1: str, param2: int) -> bool:
    """
    简短的描述。
    
    更详细的描述（如果需要）。
    
    Args:
        param1: 第一个参数的描述
        param2: 第二个参数的描述
    
    Returns:
        返回值的描述
    
    Raises:
        ValueError: 可能的异常
    """
    pass
```

## 报告问题

请使用 GitHub Issues 报告问题，包含：
- 清晰的问题描述
- 重现步骤
- 期望行为
- 实际行为
- Python 版本和操作系统

## 功能建议

功能建议也欢迎！请创建 GitHub Issue 并打上 `enhancement` 标签。

## 许可证

贡献代码表示你同意在 MIT 许可证下发布该代码。
