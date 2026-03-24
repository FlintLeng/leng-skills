---
name: leng-zhangtianping
description: 掌天瓶天气查询技能。当用户输入"掌天瓶"或询问天气时触发，返回当天及未来三天的天气预报。使用 wttr.in 免费天气服务，无需 API 密钥。
---

# 掌天瓶 - 天气预报

当用户说"掌天瓶"时，查询当天及未来三天的天气预报。

## 使用方法

```bash
# 获取4天天气预报（今天 + 未来3天）
curl -s "wttr.in/?lang=zh&format=3&1"
curl -s "wttr.in/?lang=zh&T" | head -30
```

## 指定城市

如果用户未指定城市，默认使用北京：

```bash
# 北京4天天气预报
curl -s "wttr.in/Beijing?lang=zh&format=3"
curl -s "wttr.in/Beijing?lang=zh"
```

## 输出格式

返回以下信息：
- **今天**: 天气状况、温度、湿度、风速
- **明天**: 天气状况、温度范围
- **后天**: 天气状况、温度范围
- **大后天**: 天气状况、温度范围

## wttr.in 参数说明

- `?lang=zh` - 中文显示
- `?format=3` - 简洁格式
- `?T` - 终端文本格式
- `?m` - 公制单位（摄氏度）
- `?1` - 只显示今天

## 示例命令

```bash
# 完整4天预报（中文）
curl -s "wttr.in/Shanghai?lang=zh"

# 简洁格式
curl -s "wttr.in/Shanghai?lang=zh&format=3"

# 当前天气
curl -s "wttr.in/Shanghai?lang=zh&format=%l:+%c+%t+%h+%w"
```

## 触发词

- "掌天瓶"
- "天气"
- "天气预报"
- "今天天气"
