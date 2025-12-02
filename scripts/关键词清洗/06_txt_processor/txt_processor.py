#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT文本批量处理脚本
功能: 将文本中的"竖线+空格"按规则转换为换行符
"""

import os
import re
from pathlib import Path


def count_pipe_space(text):
    """统计文本中"| "(竖线+空格)的总数"""
    return text.count('| ')


def process_text(text):
    """
    按照以下逻辑处理文本:
    1. 将连续超过3个的"| "减半
    2. 将"| | | "转换为换行
    3. 将"| | "转换为换行
    4. 将"| "转换为换行
    """
    original_count = count_pipe_space(text)
    
    # 步骤1: 将连续超过3个的"| "数量减半
    # 使用正则表达式找到所有连续的"| "(4个或以上)
    def reduce_pipe_space(match):
        matched_str = match.group(0)
        # 计算有多少个"| "
        count = len(matched_str) // 2  # 每个"| "是2个字符
        if count > 3:
            # 减半(向下取整)
            new_count = count // 2
            return '| ' * new_count
        return matched_str
    
    # 找到所有连续的"| "并减半(4个或以上)
    text = re.sub(r'(?:\| ){4,}', reduce_pipe_space, text)
    
    # 步骤2-4: 按顺序将"| "转换为换行
    # 先处理三个"| | | "
    text = text.replace('| | | ', '\n')
    
    # 再处理两个"| | "
    text = text.replace('| | ', '\n')
    
    # 最后处理单个"| "
    text = text.replace('| ', '\n')
    
    # 统计换行符数量
    newline_count = text.count('\n')
    
    return text, original_count, newline_count


def process_file(input_path, output_path):
    """处理单个文件"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        processed_content, pipe_space_count, newline_count = process_text(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        return True, pipe_space_count, newline_count
    except Exception as e:
        return False, 0, 0, str(e)


def main():
    print("=" * 60)
    print("TXT文本批量处理工具")
    print("功能: 将'竖线+空格'(| )转换为换行符")
    print("=" * 60)
    print()
    
    # 获取输入路径
    while True:
        input_path = input("请输入TXT文件所在的文件夹路径: ").strip()
        if os.path.isdir(input_path):
            break
        else:
            print("错误: 路径不存在或不是文件夹,请重新输入!")
    
    # 获取输出路径
    while True:
        output_path = input("请输入处理结果的输出文件夹路径: ").strip()
        if output_path:
            # 如果输出路径不存在,创建它
            os.makedirs(output_path, exist_ok=True)
            break
        else:
            print("错误: 输出路径不能为空,请重新输入!")
    
    print()
    print("开始处理文件...")
    print("-" * 60)
    
    # 扫描所有TXT文件
    txt_files = list(Path(input_path).glob('*.txt'))
    
    if not txt_files:
        print("错误: 在指定路径中没有找到任何TXT文件!")
        return
    
    print(f"找到 {len(txt_files)} 个TXT文件\n")
    
    # 统计信息
    total_pipe_space = 0
    total_newlines = 0
    success_count = 0
    failed_count = 0
    
    # 处理每个文件
    for txt_file in txt_files:
        filename = txt_file.name
        output_file = os.path.join(output_path, filename)
        
        result = process_file(txt_file, output_file)
        
        if result[0]:
            success_count += 1
            pipe_space_count = result[1]
            newline_count = result[2]
            total_pipe_space += pipe_space_count
            total_newlines += newline_count
            print(f"✓ {filename}")
            print(f"  检测到 {pipe_space_count} 个'| '组合 -> 输出 {newline_count} 个换行符")
        else:
            failed_count += 1
            error_msg = result[3]
            print(f"✗ {filename} - 处理失败: {error_msg}")
    
    # 输出总结
    print()
    print("=" * 60)
    print("处理完成!")
    print("-" * 60)
    print(f"成功处理: {success_count} 个文件")
    print(f"处理失败: {failed_count} 个文件")
    print(f"总共检测到: {total_pipe_space} 个'| '组合")
    print(f"总共输出: {total_newlines} 个换行符")
    print(f"结果已保存到: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
    finally:
        input