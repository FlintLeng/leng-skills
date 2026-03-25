#!/usr/bin/env python3
"""
风雷翅 - 飞书文档创建脚本
用于创建旅游攻略文档并写入飞书
"""

import argparse
import json
import os
import sys
import time
from typing import Optional, List, Dict, Any

try:
    import requests
except ImportError:
    print("错误: 请安装 requests 库: pip install requests")
    sys.exit(1)

# 飞书应用配置
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "cli_a93bb96dc8399cb2")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "J06ZwafYisdz3LJQIfRFMQztvjTSDjkT")
USER_OPEN_ID = os.environ.get("FEISHU_USER_OPEN_ID", "ou_85c6f41a2b841a35e049770984c555aa")


class FeishuDocClient:
    """飞书文档客户端"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or FEISHU_APP_ID
        self.app_secret = app_secret or FEISHU_APP_SECRET
        self.token = None
        self.token_expires = 0
    
    def get_tenant_access_token(self) -> str:
        """获取 tenant_access_token"""
        if self.token and time.time() < self.token_expires:
            return self.token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            result = response.json()
            if result.get("code") == 0:
                self.token = result.get("tenant_access_token")
                self.token_expires = time.time() + 7000
                return self.token
            else:
                raise Exception(f"获取token失败: {result.get('msg', result)}")
        except Exception as e:
            raise Exception(f"获取token异常: {e}")
    
    def create_document(self, title: str, owner_open_id: str = None) -> Dict[str, Any]:
        """创建飞书文档"""
        token = self.get_tenant_access_token()
        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "title": title,
            "owner_open_id": owner_open_id or USER_OPEN_ID
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            result = response.json()
            if result.get("code") == 0:
                return {
                    "success": True,
                    "doc_token": result["data"]["document"]["document_id"],
                    "title": result["data"]["document"]["title"]
                }
            else:
                return {
                    "success": False,
                    "error": result.get("msg", str(result))
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_text_block(self, text: str) -> Dict[str, Any]:
        """创建文本块"""
        return {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": text}}],
                "style": {}
            }
        }
    
    def create_heading_block(self, text: str, level: int = 1) -> Dict[str, Any]:
        """创建标题块"""
        block_type = {1: 3, 2: 4, 3: 5}.get(level, 3)
        heading_key = {1: "heading1", 2: "heading2", 3: "heading3"}.get(level, "heading1")
        return {
            "block_type": block_type,
            heading_key: {
                "elements": [{"text_run": {"content": text}}]
            }
        }
    
    def create_bullet_block(self, text: str) -> Dict[str, Any]:
        """创建无序列表块"""
        return {
            "block_type": 12,
            "bullet": {
                "elements": [{"text_run": {"content": text}}]
            }
        }
    
    def parse_markdown_to_blocks(self, markdown: str) -> List[Dict[str, Any]]:
        """解析 Markdown 为文档块"""
        blocks = []
        lines = markdown.split("\n")
        
        for line in lines:
            line = line.rstrip()
            if not line:
                continue
            
            # 标题
            if line.startswith("# "):
                blocks.append(self.create_heading_block(line[2:], 1))
            elif line.startswith("## "):
                blocks.append(self.create_heading_block(line[3:], 2))
            elif line.startswith("### "):
                blocks.append(self.create_heading_block(line[4:], 3))
            elif line.startswith("#### "):
                blocks.append(self.create_heading_block(line[5:], 3))
            # 列表项
            elif line.startswith("- ") or line.startswith("* "):
                blocks.append(self.create_bullet_block(line[2:]))
            elif line.strip() and line[0].isdigit() and ". " in line:
                text = line.split(". ", 1)[-1] if ". " in line else line
                blocks.append(self.create_bullet_block(text))
            # 普通文本
            elif line.strip() and not line.startswith("---") and not line.startswith("|"):
                blocks.append(self.create_text_block(line))
        
        return blocks
    
    def insert_blocks(self, doc_token: str, blocks: List[Dict[str, Any]], batch_size: int = 20) -> Dict[str, Any]:
        """插入文档块"""
        token = self.get_tenant_access_token()
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        total_batches = (len(blocks) + batch_size - 1) // batch_size
        success_count = 0
        errors = []
        
        for i in range(0, len(blocks), batch_size):
            batch = blocks[i:i + batch_size]
            data = {
                "children": batch,
                "index": i
            }
            
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                result = response.json()
                if result.get("code") == 0:
                    success_count += 1
                else:
                    errors.append(f"批次 {i // batch_size + 1}: {result.get('msg', result)}")
                time.sleep(0.3)
            except Exception as e:
                errors.append(f"批次 {i // batch_size + 1}: {str(e)}")
        
        return {
            "success": success_count == total_batches,
            "total_batches": total_batches,
            "success_count": success_count,
            "errors": errors
        }
    
    def add_permission(self, doc_token: str, user_open_id: str = None, perm: str = "full_access") -> Dict[str, Any]:
        """添加文档权限"""
        token = self.get_tenant_access_token()
        url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_token}/members"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        params = {"type": "docx"}
        data = {
            "member_type": "openid",
            "member_id": user_open_id or USER_OPEN_ID,
            "perm": perm
        }
        
        try:
            response = requests.post(url, headers=headers, params=params, json=data, timeout=30)
            result = response.json()
            if result.get("code") == 0:
                return {"success": True, "perm": perm}
            else:
                return {"success": False, "error": result.get("msg", str(result))}
        except Exception as e:
            return {"success": False, "error": str(e)}


def create_travel_guide(city: str, content: str, user_open_id: str = None) -> Dict[str, Any]:
    """
    创建旅游攻略文档
    
    Args:
        city: 城市名称
        content: Markdown 格式的攻略内容
        user_open_id: 用户 open_id
    
    Returns:
        包含执行结果的字典
    """
    result = {
        "success": False,
        "city": city,
        "doc_token": None,
        "doc_url": None,
        "errors": []
    }
    
    client = FeishuDocClient()
    
    # 1. 创建文档
    from datetime import datetime
    title = f"{city}旅游攻略 - {datetime.now().strftime('%Y年%m月')}"
    print(f"正在创建文档: {title}")
    doc_result = client.create_document(title, user_open_id)
    
    if not doc_result.get("success"):
        result["errors"].append(f"创建文档失败: {doc_result.get('error')}")
        return result
    
    doc_token = doc_result["doc_token"]
    result["doc_token"] = doc_token
    result["doc_url"] = f"https://feishu.cn/docx/{doc_token}"
    print(f"文档创建成功: {result['doc_url']}")
    
    # 2. 解析内容
    print("正在解析内容...")
    blocks = client.parse_markdown_to_blocks(content)
    print(f"解析完成，共 {len(blocks)} 个文档块")
    
    # 3. 写入内容
    print("正在写入内容...")
    insert_result = client.insert_blocks(doc_token, blocks)
    if not insert_result.get("success"):
        result["errors"].append(f"部分内容写入失败: {insert_result.get('errors')}")
    print(f"内容写入完成: {insert_result['success_count']}/{insert_result['total_batches']} 批次成功")
    
    # 4. 添加权限
    print("正在添加文档权限...")
    perm_result = client.add_permission(doc_token, user_open_id)
    if not perm_result.get("success"):
        result["errors"].append(f"添加权限失败: {perm_result.get('error')}")
    else:
        print("权限添加成功")
    
    result["success"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description="创建旅游攻略文档")
    parser.add_argument("--city", required=True, help="城市名称")
    parser.add_argument("--content", help="Markdown 内容（或从 stdin 读取）")
    parser.add_argument("--file", help="Markdown 文件路径")
    parser.add_argument("--user-open-id", help="用户 open_id")
    args = parser.parse_args()
    
    # 获取内容
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        content = sys.stdin.read()
    
    # 创建文档
    result = create_travel_guide(
        city=args.city,
        content=content,
        user_open_id=args.user_open_id
    )
    
    # 输出结果
    print("\n" + "=" * 50)
    if result["success"]:
        print(f"✅ {result['city']}旅游攻略创建成功!")
        print(f"📄 文档链接: {result['doc_url']}")
    else:
        print("❌ 文档创建失败!")
        for error in result["errors"]:
            print(f"   - {error}")
    
    print("\n" + json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
