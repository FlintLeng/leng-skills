#!/usr/bin/env python3
"""
大衍诀 - 全球经济金融简报
数据源: NASDAQ API + akshare
获取全球重大经济金融新闻、白银现货、纳斯达克、英伟达、特斯拉实时数据
"""

import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

def safe_import(module_name: str, package: str = None) -> Optional[Any]:
    """安全导入模块，失败返回None"""
    try:
        if package:
            module = __import__(package, fromlist=[module_name])
            return getattr(module, module_name)
        return __import__(module_name)
    except Exception as e:
        print(f"[WARN] 无法导入 {module_name}: {e}", file=sys.stderr)
        return None

ak = safe_import('akshare')

# NASDAQ API 配置
NASDAQ_API_BASE = "https://api.nasdaq.com/api"

def fetch_url(url: str, headers: dict = None) -> Optional[dict]:
    """安全的 URL 请求"""
    try:
        req = urllib.request.Request(url)
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        if headers:
            default_headers.update(headers)
        for key, value in default_headers.items():
            req.add_header(key, value)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"[ERROR] 请求失败 {url}: {e}", file=sys.stderr)
        return None

def get_news() -> Dict[str, Any]:
    """获取全球重大经济金融新闻"""
    result = {
        "success": False,
        "source": None,
        "news": [],
        "error": None
    }
    
    if ak is not None:
        try:
            news_df = ak.stock_news_em(symbol="财经")
            if news_df is not None and len(news_df) > 0:
                news_list = []
                for _, row in news_df.head(10).iterrows():
                    news_list.append({
                        "title": row.get('新闻标题', ''),
                        "time": row.get('发布时间', ''),
                        "source": row.get('新闻来源', '')
                    })
                result["success"] = True
                result["source"] = "akshare"
                result["news"] = news_list
                return result
        except Exception as e:
            result["error"] = f"akshare: {e}"
    
    result["error"] = result.get("error") or "无法获取新闻数据"
    return result

def get_nasdaq_quote(symbol: str) -> Dict[str, Any]:
    """通过 NASDAQ API 获取股票报价"""
    result = {
        "success": False,
        "symbol": symbol,
        "price": None,
        "change_percent": None,
        "high": None,
        "low": None,
        "error": None
    }
    
    url = f"{NASDAQ_API_BASE}/quote/{symbol}/info?assetclass=stocks"
    
    data = fetch_url(url)
    if data and data.get('data'):
        try:
            quote_data = data['data']
            primary = quote_data.get('primaryData', {})
            
            # 解析价格
            price_str = primary.get('lastSalePrice', '0')
            price = float(price_str.replace('$', '').replace(',', ''))
            
            # 解析涨跌幅
            change_str = primary.get('percentageChange', '0%')
            change_percent = float(change_str.replace('%', '').replace('+', ''))
            
            # 解析最高价和最低价
            high_str = primary.get('high', '')
            low_str = primary.get('low', '')
            
            high = float(high_str.replace('$', '').replace(',', '')) if high_str and high_str not in ['N/A', ''] else None
            low = float(low_str.replace('$', '').replace(',', '')) if low_str and low_str not in ['N/A', ''] else None
            
            result.update({
                "success": True,
                "source": "NASDAQ API",
                "price": round(price, 2),
                "change_percent": round(change_percent, 2),
                "high": round(high, 2) if high else None,
                "low": round(low, 2) if low else None
            })
            return result
        except Exception as e:
            result["error"] = f"解析数据失败: {e}"
    else:
        result["error"] = "无法获取 NASDAQ 数据"
    
    return result

def get_nasdaq_chart(symbol: str) -> Dict[str, Any]:
    """通过 NASDAQ API 获取日内图表数据（包含最高最低价）"""
    result = {
        "high": None,
        "low": None
    }
    
    try:
        url = f"{NASDAQ_API_BASE}/quote/{symbol}/chart?assetclass=stocks"
        data = fetch_url(url)
        
        if data and data.get('data') and data['data'].get('chart'):
            chart_data = data['data']['chart']
            if isinstance(chart_data, list) and len(chart_data) > 0:
                highs = [float(d.get('high', 0)) for d in chart_data if d.get('high')]
                lows = [float(d.get('low', 0)) for d in chart_data if d.get('low')]
                
                if highs:
                    result["high"] = round(max(highs), 2)
                if lows:
                    result["low"] = round(min(lows), 2)
    except Exception as e:
        pass
    
    return result

def get_nasdaq_index() -> Dict[str, Any]:
    """获取纳斯达克综合指数"""
    result = {
        "success": False,
        "symbol": "^IXIC",
        "name": "纳斯达克综合指数",
        "price": None,
        "change_percent": None,
        "high": None,
        "low": None,
        "error": None
    }
    
    # 尝试获取 NASDAQ 综合指数
    url = f"{NASDAQ_API_BASE}/quote/ndx/info?assetclass=index"
    data = fetch_url(url)
    
    if data and data.get('data'):
        try:
            quote_data = data['data']
            primary = quote_data.get('primaryData', {})
            
            price_str = primary.get('lastSalePrice', '0')
            price = float(price_str.replace('$', '').replace(',', ''))
            
            change_str = primary.get('percentageChange', '0%')
            change_percent = float(change_str.replace('%', '').replace('+', ''))
            
            high_str = primary.get('high', '')
            low_str = primary.get('low', '')
            
            high = float(high_str.replace('$', '').replace(',', '')) if high_str and high_str not in ['N/A', ''] else None
            low = float(low_str.replace('$', '').replace(',', '')) if low_str and low_str not in ['N/A', ''] else None
            
            result.update({
                "success": True,
                "source": "NASDAQ API",
                "price": round(price, 2),
                "change_percent": round(change_percent, 2),
                "high": high,
                "low": low
            })
            return result
        except Exception as e:
            result["error"] = f"解析数据失败: {e}"
    else:
        result["error"] = "无法获取纳斯达克指数数据"
    
    return result

def get_silver_price() -> Dict[str, Any]:
    """获取白银现货价格"""
    result = {
        "success": False,
        "symbol": "XAGUSD",
        "name": "白银现货",
        "price": None,
        "change_percent": None,
        "high": None,
        "low": None,
        "error": None
    }
    
    # 方法1: 使用 akshare 获取沪银主力合约 (AG0)
    if ak is not None:
        try:
            df = ak.futures_main_sina(symbol='AG0')
            if df is not None and len(df) > 0:
                latest = df.iloc[-1]
                price = float(latest['收盘价'])
                high = float(latest['最高价'])
                low = float(latest['最低价'])
                
                # 计算涨跌幅 (与前一天收盘价比较)
                if len(df) > 1:
                    prev_close = float(df.iloc[-2]['收盘价'])
                    change_percent = ((price - prev_close) / prev_close) * 100
                else:
                    change_percent = 0
                
                result.update({
                    "success": True,
                    "source": "akshare-沪银主力",
                    "price": round(price, 2),
                    "change_percent": round(change_percent, 2),
                    "high": round(high, 2),
                    "low": round(low, 2)
                })
                return result
        except Exception as e:
            print(f"[WARN] akshare 沪银主力获取失败: {e}", file=sys.stderr)
    
    # 方法2: 使用白银 ETF SLV 作为参考
    slv_result = get_nasdaq_quote("SLV")
    if slv_result["success"]:
        # SLV 价格大约是白银价格的 1/10 左右
        silver_price = slv_result["price"] * 10  # 粗略换算
        
        result.update({
            "success": True,
            "source": "NASDAQ-SLV ETF (参考)",
            "price": round(silver_price, 2),
            "change_percent": slv_result["change_percent"],
            "high": round(slv_result["high"] * 10, 2) if slv_result.get("high") else None,
            "low": round(slv_result["low"] * 10, 2) if slv_result.get("low") else None
        })
        return result
    
    result["error"] = result.get("error") or "无法获取白银数据"
    return result

def get_nvidia() -> Dict[str, Any]:
    """获取英伟达股票数据"""
    result = get_nasdaq_quote("NVDA")
    result["name"] = "英伟达"
    
    # 尝试获取日内高低价
    if result["success"] and (result["high"] is None or result["low"] is None):
        chart = get_nasdaq_chart("NVDA")
        if chart["high"]:
            result["high"] = chart["high"]
        if chart["low"]:
            result["low"] = chart["low"]
    
    return result

def get_tesla() -> Dict[str, Any]:
    """获取特斯拉股票数据"""
    result = get_nasdaq_quote("TSLA")
    result["name"] = "特斯拉"
    
    # 尝试获取日内高低价
    if result["success"] and (result["high"] is None or result["low"] is None):
        chart = get_nasdaq_chart("TSLA")
        if chart["high"]:
            result["high"] = chart["high"]
        if chart["low"]:
            result["low"] = chart["low"]
    
    return result

def format_table(data: List[Dict]) -> str:
    """格式化表格输出"""
    header = "| 品种 | 实时价格 | 当日涨跌幅 | 当日最高 | 当日最低 | 状态 |"
    separator = "|------|----------|------------|----------|----------|------|"
    
    rows = []
    for item in data:
        status = "✅" if item.get("success") else "❌"
        price = item.get("price", "-") if item.get("price") is not None else "-"
        change = f"{item.get('change_percent', '-')}%" if item.get("change_percent") is not None else "-"
        high = item.get("high", "-") if item.get("high") is not None else "-"
        low = item.get("low", "-") if item.get("low") is not None else "-"
        
        rows.append(f"| {item['name']} | {price} | {change} | {high} | {low} | {status} |")
    
    return "\n".join([header, separator] + rows)

def main():
    """主函数"""
    print("=" * 60)
    print("🔮 大衍诀 - 全球经济金融简报")
    print("=" * 60)
    print(f"📅 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    execution_log = []
    
    # 1. 获取新闻
    print("📰 正在获取全球财经新闻...")
    news_result = get_news()
    execution_log.append({
        "step": "获取财经新闻",
        "success": news_result["success"],
        "source": news_result.get("source"),
        "error": news_result.get("error")
    })
    
    # 2. 获取白银价格
    print("🥈 正在获取白银现货价格...")
    silver_result = get_silver_price()
    execution_log.append({
        "step": "获取白银现货",
        "success": silver_result["success"],
        "source": silver_result.get("source"),
        "error": silver_result.get("error")
    })
    time.sleep(0.5)
    
    # 3. 获取纳斯达克指数
    print("📈 正在获取纳斯达克指数...")
    nasdaq_result = get_nasdaq_index()
    execution_log.append({
        "step": "获取纳斯达克指数",
        "success": nasdaq_result["success"],
        "source": nasdaq_result.get("source"),
        "error": nasdaq_result.get("error")
    })
    time.sleep(0.5)
    
    # 4. 获取英伟达
    print("🟢 正在获取英伟达股价...")
    nvidia_result = get_nvidia()
    execution_log.append({
        "step": "获取英伟达股价",
        "success": nvidia_result["success"],
        "source": nvidia_result.get("source"),
        "error": nvidia_result.get("error")
    })
    time.sleep(0.5)
    
    # 5. 获取特斯拉
    print("🔴 正在获取特斯拉股价...")
    tesla_result = get_tesla()
    execution_log.append({
        "step": "获取特斯拉股价",
        "success": tesla_result["success"],
        "source": tesla_result.get("source"),
        "error": tesla_result.get("error")
    })
    
    print()
    print("=" * 60)
    print("📊 行情数据汇总")
    print("=" * 60)
    
    # 输出表格
    market_data = [silver_result, nasdaq_result, nvidia_result, tesla_result]
    print(format_table(market_data))
    
    print()
    print("=" * 60)
    print("📰 财经新闻摘要")
    print("=" * 60)
    
    if news_result["success"] and news_result["news"]:
        for i, news in enumerate(news_result["news"][:5], 1):
            print(f"{i}. [{news.get('time', '')}] {news.get('title', '')}")
    else:
        print("暂无新闻数据")
    
    print()
    print("=" * 60)
    print("📋 执行详情")
    print("=" * 60)
    
    success_count = sum(1 for log in execution_log if log["success"])
    print(f"成功率: {success_count}/{len(execution_log)}")
    
    for log in execution_log:
        status = "✅" if log["success"] else "❌"
        source = f" [{log.get('source')}]" if log.get("source") and log["success"] else ""
        error_info = f" - {log.get('error')}" if log.get("error") and not log["success"] else ""
        print(f"  {status} {log['step']}{source}{error_info}")
    
    # 输出 JSON 结果
    result = {
        "timestamp": datetime.now().isoformat(),
        "news": news_result,
        "market": {
            "silver": silver_result,
            "nasdaq": nasdaq_result,
            "nvidia": nvidia_result,
            "tesla": tesla_result
        },
        "execution_log": execution_log,
        "success_rate": f"{success_count}/{len(execution_log)}"
    }
    
    print()
    print("=" * 60)
    print("📦 JSON 输出")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result

if __name__ == "__main__":
    main()
