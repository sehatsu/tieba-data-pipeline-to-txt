#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT文件批量处理脚本
功能：
1. 查找指定目录下的所有TXT文件
2. 处理相邻的竖线行和空行
3. 压缩连续空行
"""

import os
import re
from pathlib import Path


def is_pipe_only_line(line):
    """检查一行是否仅包含竖线字符"""
    stripped = line.strip()
    return len(stripped) > 0 and all(c == '|' for c in stripped)


def is_empty_or_whitespace(line):
    """检查一行是否为空行或仅包含空白字符（全角或半角空格）"""
    # 去掉换行符后检查
    stripped = line.rstrip('\n\r')
    # 检查是否为空或仅包含空白字符（包括全角空格\u3000和半角空格）
    return len(stripped) == 0 or all(c in ' \t\u3000' for c in stripped)


def process_adjacent_lines(lines):
    """
    处理相邻两行的情况：
    - 如果一行仅包含竖线，另一行是空行或空白
    - 将这两行替换为一个空行
    """
    if len(lines) <= 1:
        return lines
    
    result = []
    i = 0
    
    while i < len(lines):
        if i + 1 < len(lines):
            current_line = lines[i]
            next_line = lines[i + 1]
            
            # 检查相邻两行的组合情况
            current_is_pipe = is_pipe_only_line(current_line)
            current_is_empty = is_empty_or_whitespace(current_line)
            next_is_pipe = is_pipe_only_line(next_line)
            next_is_empty = is_empty_or_whitespace(next_line)
            
            # 情况1: 当前行是竖线，下一行是空白
            # 情况2: 当前行是空白,下一行是竖线
            if (current_is_pipe and next_is_empty) or (current_is_empty and next_is_pipe):
                result.append('\n')  # 替换为一个空行
                i += 2  # 跳过这两行
                continue
        
        # 如果不符合条件，保留当前行
        result.append(lines[i])
        i += 1
    
    return result


def compress_empty_lines(lines):
    """
    将连续的3行或更多空行压缩为2个空行
    """
    if len(lines) == 0:
        return lines
    
    result = []
    empty_count = 0
    
    for line in lines:
        if is_empty_or_whitespace(line):
            empty_count += 1
        else:
            # 遇到非空行，处理之前的空行
            if empty_count >= 3:
                # 添加2个空行
                result.extend(['\n', '\n'])
            else:
                # 保留原有的空行
                result.extend(['\n'] * empty_count)
            
            empty_count = 0
            result.append(line)
    
    # 处理文件末尾的空行
    if empty_count >= 3:
        result.extend(['\n', '\n'])
    else:
        result.extend(['\n'] * empty_count)
    
    return result


def process_file(input_path, output_path):
    """处理单个TXT文件"""
    try:
        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 步骤1: 处理相邻的竖线行和空行
        lines = process_adjacent_lines(lines)
        
        # 步骤2: 压缩连续空行
        lines = compress_empty_lines(lines)
        
        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return True, None
    
    except Exception as e:
        return False, str(e)


def find_txt_files(directory):
    """查找目录下所有TXT文件"""
    txt_files = []
    path = Path(directory)
    
    if not path.exists():
        return []
    
    # 递归查找所有.txt文件
    for file_path in path.rglob('*.txt'):
        if file_path.is_file():
            txt_files.append(file_path)
    
    return txt_files


def main():
    """主函数"""
    print("=" * 60)
    print("TXT文件批量处理工具")
    print("=" * 60)
    print()
    
    # 获取输入路径
    while True:
        input_dir = input("请输入TXT文件所在的目录路径: ").strip()
        if not input_dir:
            print("错误：路径不能为空，请重新输入！")
            continue
        
        if not os.path.exists(input_dir):
            print(f"错误：路径 '{input_dir}' 不存在，请重新输入！")
            continue
        
        if not os.path.isdir(input_dir):
            print(f"错误：'{input_dir}' 不是一个目录，请重新输入！")
            continue
        
        break
    
    # 查找TXT文件
    print(f"\n正在查找 '{input_dir}' 目录下的TXT文件...")
    txt_files = find_txt_files(input_dir)
    
    if not txt_files:
        print("未找到任何TXT文件！")
        return
    
    print(f"找到 {len(txt_files)} 个TXT文件。")
    print()
    
    # 获取输出路径
    while True:
        output_dir = input("请输入处理结果的输出目录路径: ").strip()
        if not output_dir:
            print("错误：路径不能为空，请重新输入！")
            continue
        
        break
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n输出目录: {output_dir}")
    print()
    
    # 处理文件
    print("开始处理文件...")
    print("-" * 60)
    
    success_count = 0
    fail_count = 0
    
    for i, input_file in enumerate(txt_files, 1):
        # 构建输出文件路径，保持相对路径结构
        relative_path = input_file.relative_to(input_dir)
        output_file = Path(output_dir) / relative_path
        
        # 创建输出文件的父目录
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[{i}/{len(txt_files)}] 处理: {relative_path}")
        
        success, error = process_file(input_file, output_file)
        
        if success:
            print(f"    ✓ 成功")
            success_count += 1
        else:
            print(f"    ✗ 失败: {error}")
            fail_count += 1
    
    # 显示统计结果
    print("-" * 60)
    print(f"\n处理完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")
    print(f"总计: {len(txt_files)} 个文件")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断。")
    except Exception as e:
        print(f"\n发生错误: {e}")
    
    input("\n按回车键退出...")
