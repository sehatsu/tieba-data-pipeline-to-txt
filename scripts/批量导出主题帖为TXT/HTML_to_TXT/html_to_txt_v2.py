#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML到TXT转换脚本
用于将百度贴吧的HTML文件解析为纯文本文件
"""

import os
import sys
import re
from pathlib import Path
import argparse
import traceback


def pause():
    """暂停以便查看输出"""
    print("\n" + "=" * 60)
    input("按回车键退出...")


def check_dependencies():
    """检查必要的依赖"""
    try:
        from bs4 import BeautifulSoup
        return True
    except ImportError:
        print("错误: 缺少必要的库 'beautifulsoup4'")
        print("\n请在命令行中运行以下命令安装:")
        print("pip install beautifulsoup4 lxml")
        print("\n或者:")
        print("pip install beautifulsoup4 lxml --break-system-packages")
        return False


def clean_text(text):
    """清理文本内容"""
    if not text:
        return ""
    
    # 去除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 去除首尾空白
    text = text.strip()
    return text


def extract_post_content(soup):
    """提取帖子内容"""
    content_parts = []
    
    # 尝试提取帖子标题
    title = soup.find('title')
    if title:
        content_parts.append(f"标题: {clean_text(title.get_text())}\n")
        content_parts.append("=" * 60 + "\n\n")
    
    # 尝试提取meta描述
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        content_parts.append(f"描述: {clean_text(meta_desc.get('content'))}\n\n")
    
    # 提取主要内容区域
    # 百度贴吧的帖子内容通常在特定的div中
    main_content = soup.find_all(['div', 'p', 'span'], class_=re.compile(r'(content|post|reply|text)'))
    
    if main_content:
        content_parts.append("主要内容:\n")
        content_parts.append("-" * 60 + "\n")
        for element in main_content:
            text = clean_text(element.get_text())
            if text and len(text) > 10:  # 过滤太短的文本
                content_parts.append(f"{text}\n\n")
    
    # 如果没有找到特定内容，提取body中的所有文本
    if len(content_parts) <= 3:
        body = soup.find('body')
        if body:
            # 移除script和style标签
            for script in body(['script', 'style', 'meta', 'link']):
                script.decompose()
            
            text = clean_text(body.get_text())
            if text:
                content_parts.append("完整文本内容:\n")
                content_parts.append("-" * 60 + "\n")
                content_parts.append(f"{text}\n")
    
    return ''.join(content_parts)


def is_404_page(soup):
    """检测是否为404页面"""
    title = soup.find('title')
    if title and '404' in title.get_text():
        return True
    
    # 检查页面内容是否包含删除提示
    text = soup.get_text()
    if '该贴已被删除' in text or '贴子已被系统删除' in text:
        return True
    
    return False


def parse_html_file(html_path, output_dir):
    """解析单个HTML文件并保存为txt"""
    try:
        from bs4 import BeautifulSoup
        
        # 读取HTML文件
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        
        # 如果UTF-8失败，尝试GBK编码（百度贴吧可能使用GBK）
        if not html_content or len(html_content) < 100:
            with open(html_path, 'r', encoding='gbk', errors='ignore') as f:
                html_content = f.read()
        
        # 解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 检查是否为404页面
        if is_404_page(soup):
            print(f"⚠️  跳过404页面: {html_path.name}")
            return False
        
        # 提取内容
        content = extract_post_content(soup)
        
        if not content or len(content) < 50:
            print(f"⚠️  内容过短，跳过: {html_path.name}")
            return False
        
        # 生成输出文件名
        output_filename = html_path.stem + '.txt'
        output_path = output_dir / output_filename
        
        # 保存为txt文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 成功转换: {html_path.name} -> {output_filename}")
        return True
        
    except Exception as e:
        print(f"✗ 转换失败 {html_path.name}: {str(e)}")
        return None


def batch_convert(input_dir, output_dir):
    """批量转换HTML文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 检查输入目录是否存在
    if not input_path.exists():
        print(f"错误: 输入目录不存在: {input_dir}")
        return
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 获取所有HTML文件
    html_files = list(input_path.glob('*.html'))
    
    if not html_files:
        print(f"错误: 在 {input_dir} 中没有找到HTML文件")
        return
    
    print(f"\n找到 {len(html_files)} 个HTML文件")
    print(f"输入目录: {input_path.absolute()}")
    print(f"输出目录: {output_path.absolute()}\n")
    print("=" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        print(f"[{i}/{len(html_files)}] ", end='')
        result = parse_html_file(html_file, output_path)
        
        if result:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1
    
    # 输出统计信息
    print("\n" + "=" * 60)
    print(f"\n转换完成!")
    print(f"  ✓ 成功: {success_count} 个文件")
    print(f"  ⚠ 跳过: {skip_count} 个文件 (404页面或内容过短)")
    print(f"  ✗ 失败: {error_count} 个文件")
    print(f"\n输出目录: {output_path.absolute()}\n")


def get_script_directory():
    """获取脚本所在目录"""
    if getattr(sys, 'frozen', False):
        # 如果是打包的exe
        return Path(sys.executable).parent
    else:
        # 如果是普通的.py文件
        return Path(__file__).parent


def main():
    try:
        # 检查依赖
        if not check_dependencies():
            pause()
            sys.exit(1)
        
        print("=" * 60)
        print("HTML到TXT批量转换工具")
        print("=" * 60)
        
        # 获取脚本所在目录
        script_dir = get_script_directory()
        
        # 如果是通过双击运行（没有命令行参数），使用交互式模式
        if len(sys.argv) == 1:
            print("\n交互式模式\n")
            
            # 询问输入目录
            print("请输入HTML文件所在目录:")
            print(f"(直接按回车使用当前目录: {script_dir})")
            input_dir = input("> ").strip()
            
            if not input_dir:
                input_dir = script_dir
            
            input_path = Path(input_dir)
            if not input_path.exists():
                print(f"\n错误: 目录不存在: {input_dir}")
                pause()
                sys.exit(1)
            
            # 询问输出目录
            print("\n请输入输出目录:")
            default_output = script_dir / "txt_files"
            print(f"(直接按回车使用: {default_output})")
            output_dir = input("> ").strip()
            
            if not output_dir:
                output_dir = default_output
            
            print("\n开始转换...\n")
            batch_convert(str(input_path), str(output_dir))
            
        else:
            # 命令行模式
            parser = argparse.ArgumentParser(
                description='将HTML文件批量转换为TXT文件',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog='''
使用示例:
  # 转换指定目录下的所有HTML文件
  python html_to_txt.py -i ./html_files -o ./txt_files
  
  # 或使用默认路径
  python html_to_txt.py
                '''
            )
            
            parser.add_argument(
                '-i', '--input',
                default=str(script_dir),
                help='输入目录路径 (默认: 脚本所在目录)'
            )
            
            parser.add_argument(
                '-o', '--output',
                default=str(script_dir / 'txt_files'),
                help='输出目录路径 (默认: 脚本所在目录/txt_files)'
            )
            
            args = parser.parse_args()
            batch_convert(args.input, args.output)
        
        pause()
        
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        pause()
        sys.exit(0)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("发生错误:")
        print("=" * 60)
        print(f"\n{str(e)}\n")
        print("详细错误信息:")
        traceback.print_exc()
        pause()
        sys.exit(1)


if __name__ == '__main__':
    main()
