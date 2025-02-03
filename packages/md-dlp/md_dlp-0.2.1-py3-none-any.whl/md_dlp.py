#!/usr/bin/env python3

import argparse
import requests
import re
import os

def extract_content(raw_content):
    """提取标题和内容"""
    # 提取标题
    title_match = re.search(r'Title: (.*?)$', raw_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else 'Untitled'

    # 提取源 URL
    url_match = re.search(r'URL Source: (.*?)$', raw_content, re.MULTILINE)
    source = url_match.group(1).strip() if url_match else ''

    # 提取正文内容
    content_match = re.search(r'Markdown Content:\n(.*)', raw_content, re.DOTALL)
    content = content_match.group(1).strip() if content_match else raw_content

    return title, source, content

def format_markdown(title, source, content):
    """格式化为标准 markdown"""
    return f"""---
title: {title}
source: {source}
---

{content}
"""

def fetch_and_save(url, output_dir='.'):
    """
    从给定URL获取内容并保存为标准格式的markdown文件
    
    Args:
        url: 要获取的URL
        output_dir: 输出目录路径，默认为当前目录
    """
    # 添加基础URL前缀
    base_url = "https://r.jina.ai/"
    full_url = base_url + url

    try:
        # 获取内容
        response = requests.get(full_url)
        response.raise_for_status()
        raw_content = response.text

        # 解析内容
        title, source, content = extract_content(raw_content)

        # 格式化为标准 markdown
        md_content = format_markdown(title, source, content)

        # 生成安全的文件名
        safe_title = re.sub(r'[/\\:*?"<>|]', '_', title)
        filename = f"{safe_title}.md"

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 构建完整的文件路径
        filepath = os.path.join(output_dir, filename)

        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Content saved to: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Download content and save as standard markdown file'
    )
    parser.add_argument('-o', '--out',
                       default='.',
                       help='Output directory (default: current directory)')
    parser.add_argument('url',
                       help='URL to fetch')

    args = parser.parse_args()
    fetch_and_save(args.url, args.out)

if __name__ == "__main__":
    main()
