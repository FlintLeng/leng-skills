# Leng Skills - OpenClaw 自建技能集

> 个人开发的 OpenClaw 技能集合，涵盖金融简报、新闻汇总、天气查询、旅游攻略、文件整理等功能。

---

## 📦 技能列表

### 💰 大衍诀 (leng-dayanjue)

全球经济金融简报技能。当用户输入 **"大衍诀"** 时触发，返回当天及前一天全球重大经济金融新闻，以及白银现货(XAGUSD)、纳斯达克综合指数、英伟达(NVDA)、特斯拉(TSLA)、拼多多(PDD)的实时价格、当日涨跌幅、当日最高价、当日最低价。

**触发词**: `大衍诀`

**功能特性**:
- 📰 全球经济金融新闻汇总
- 📈 白银现货 XAGUSD 实时报价
- 📊 纳斯达克综合指数行情
- 💻 英伟达(NVDA)股票实时价格
- 🚗 特斯拉(TSLA)股票实时价格
- 🛒 拼多多(PDD)股票实时价格

---

### 🔍 搜魂术 (leng-souhunshu)

全球新闻汇总技能。当用户输入 **"搜魂术"** 时触发，自动整理两日内全球政治、金融、经济、军事、科技方面的新闻 100 条，上传到飞书文档并共享给用户。

**触发词**: `搜魂术`

**功能特性**:
- 📰 自动抓取多源新闻
- 🗂️ 按类别分类整理
- ☁️ 自动上传飞书文档
- 🔗 自动共享给用户

**适用场景**:
- 每日新闻汇总
- 全球重大事件追踪
- 信息快速获取

---

### 🌤️ 掌天瓶 (leng-zhangtianping)

天气查询技能。当用户输入 **"掌天瓶"** 或询问天气时触发，返回当天及未来三天的天气预报。

**触发词**: `掌天瓶`

**功能特性**:
- 🌡️ 当前天气状况
- 📅 未来三天预报
- 📍 支持指定城市
- 🔧 使用 wttr.in 免费服务，无需 API 密钥

**示例**:
- `掌天瓶`
- `掌天瓶 北京`
- `掌天瓶 上海`

---

### ✈️ 风雷翅 (leng-fengleichi)

城市旅游攻略技能。当用户输入 **"风雷翅"** 后跟城市名称时触发，自动整理该城市的旅游攻略，上传到飞书文档并共享给用户。

**触发词**: `风雷翅 <城市名>`

**功能特性**:
- 🏛️ 必去景点 Top 10（含简介、地址、门票、开放时间）
- 🍜 必吃美食 Top 10（含推荐餐厅、人均消费）
- 🏨 推荐住宿位置（按区域分类、价格区间）
- 🚇 交通指南（机场/火车站到市区、市内交通）
- 📅 最佳旅游时间
- ⚠️ 注意事项

**示例**:
- `风雷翅 东京`
- `风雷翅 巴黎`
- `风雷翅 成都`

---

### 📦 虚天鼎 (leng-xutianding)

文件收集整理技能。当用户输入 **"虚天鼎"** 时触发，自动将用户同时提交的文件、文章、网页地址等整理保存到电脑统一文件夹中。

**触发词**: `虚天鼎`

**功能特性**:
- 📁 支持本地文件
- 🌐 支持网页 URL
- 📄 支持飞书文档链接
- ⚡ 自动跳过访问受限内容
- 📋 返回执行详情报告

**适用场景**:
- 批量收集资料
- 整理收藏内容
- 文件归档管理

---

## 🚀 安装方法

### 方法一：克隆仓库

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/FlintLeng/leng-skills.git
```

### 方法二：手动复制

将所需技能目录复制到 OpenClaw 的 skills 目录：

```bash
cp -r leng-dayanjue ~/.openclaw/workspace/skills/
cp -r leng-souhunshu ~/.openclaw/workspace/skills/
cp -r leng-zhangtianping ~/.openclaw/workspace/skills/
cp -r leng-fengleichi ~/.openclaw/workspace/skills/
cp -r leng-xutianding ~/.openclaw/workspace/skills/
```

---

## ⚙️ 依赖要求

| 技能 | 依赖 |
|------|------|
| 大衍诀 | Python 3.x, akshare, yfinance |
| 搜魂术 | Python 3.x, 飞书 API |
| 掌天瓶 | 无（使用 wttr.in 免费服务） |
| 风雷翅 | Python 3.x, 飞书 API |
| 虚天鼎 | Python 3.x |

---

## 📝 开发者

**FlintLeng**

- GitHub: [@FlintLeng](https://github.com/FlintLeng)

---

## 📜 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

> 💡 这些技能灵感来源于《凡人修仙传》中的法宝名称
