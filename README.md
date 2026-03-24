# Leng Skills - OpenClaw 自建技能集

个人自建的 OpenClaw Agent Skills 技能包。

## 技能列表

### 🔮 大衍诀 (dayanjue)

全球经济金融简报技能。

**功能：**
- 获取全球重大经济金融新闻
- 白银现货 (XAGUSD/沪银主力) 实时行情
- 纳斯达克综合指数实时行情
- 英伟达 (NVDA) 股票实时行情
- 特斯拉 (TSLA) 股票实时行情

**触发词：** `大衍诀`

**数据源：**
- NASDAQ API（美股行情）
- akshare（财经新闻、沪银期货）

### 🌤️ 掌天瓶 (zhangtianping)

天气预报查询技能。

**功能：**
- 查询当天及未来三天的天气预报
- 支持指定城市查询
- 中文显示

**触发词：** `掌天瓶`、`天气`、`天气预报`

**数据源：**
- wttr.in（免费天气服务，无需 API 密钥）

## 安装方法

将技能目录复制到 OpenClaw 的 skills 目录：

```bash
# 复制到 OpenClaw skills 目录
cp -r dayanjue ~/.openclaw/workspace/skills/Leng_dayanjue
cp -r zhangtianping ~/.openclaw/workspace/skills/leng-zhangtianping
```

## 依赖

### 大衍诀
```bash
pip install akshare
```

### 掌天瓶
无需额外依赖，使用 curl 调用 wttr.in API。

## License

MIT
