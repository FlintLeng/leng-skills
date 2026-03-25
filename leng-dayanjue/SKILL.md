---
name: Leng_dayanjue
description: 大衍诀 - 全球经济金融简报。当用户输入"大衍诀"时触发，返回当天及前一天全球重大经济金融新闻，以及白银现货(XAGUSD)、纳斯达克综合指数、英伟达(NVDA)、特斯拉(TSLA)的实时价格、当日涨跌幅、当日最高价、当日最低价。使用 Infoway API、NASDAQ API 和 akshare 获取真实数据。
---

# 大衍诀 - 全球经济金融简报

## 触发词

- "大衍诀"

## 功能说明

当用户输入"大衍诀"时，执行以下操作：

1. 获取全球重大经济金融新闻（当天及前一天）
2. 获取白银现货 XAGUSD 实时数据（优先使用 Infoway API）
3. 获取纳斯达克综合指数实时数据
4. 获取英伟达 NVDA 股票实时数据
5. 获取特斯拉 TSLA 股票实时数据

## 执行方式

运行脚本获取数据：

```bash
python3 scripts/dayanjue.py
```

## 输出格式

### 行情数据表格

| 品种 | 实时价格 | 当日涨跌幅 | 当日最高 | 当日最低 | 状态 |
|------|----------|------------|----------|----------|------|
| 白银现货 | xx.xx | ±x.xx% | xx.xx | xx.xx | ✅/❌ |
| 纳斯达克综合指数 | xxxxx.xx | ±x.xx% | xxxxx.xx | xxxxx.xx | ✅/❌ |
| 英伟达 | xxx.xx | ±x.xx% | xxx.xx | xxx.xx | ✅/❌ |
| 特斯拉 | xxx.xx | ±x.xx% | xxx.xx | xxx.xx | ✅/❌ |

### 财经新闻摘要

列出当天及前一天的重大财经新闻标题。

### 执行详情

显示每个数据获取步骤的成功/失败状态及错误信息。

## 数据来源

- **Infoway API**: 白银现货 XAGUSD 期货实时行情（优先使用）
- **NASDAQ API**: 美股实时行情（英伟达、特斯拉、纳斯达克指数）
- **akshare**: 东方财富财经新闻、沪银主力合约 (备用)

### 数据源优先级

1. 第一选择：Infoway API - XAGUSD 实时期货数据
2. 第二选择：akshare - 沪银主力连续合约 (AG0)
3. 第三选择：NASDAQ SLV ETF（参考）

## 配置说明

### Infoway API Key 配置

将 `INFOWAY_API_KEY` 放入以下任一位置：

**方法 1：配置文件（推荐）**
```json
// ~/.openclaw/workspace/skills/Leng_dayanjue/config.json
{
  "infoway_api_key": "your-api-key-here"
}
```

**方法 2：环境变量**
```bash
export INFOWAY_API_KEY="your-api-key-here"
```

**方法 3：其他配置文件**
- `~/.infoway/api_key`
- `~/.config/infoway/api_key`

获取 API Key: https://infoway.io/register

## 错误处理

- 所有数据获取失败时跳过，不影响其他数据
- 最终报告显示成功率和各步骤执行详情
- 自动降级机制：如果 Infoway API 不可用，自动切换到 akshare
- 不使用模拟数据，只返回真实获取的数据

## 依赖安装

```bash
pip install akshare
```

## 注意事项

- NASDAQ API 无需 API Key
- Infoway API 需要申请免费账户获取 API Key
- 美股数据在美股交易时段更新
- akshare 数据为国内期货市场数据（沪银主力合约）
