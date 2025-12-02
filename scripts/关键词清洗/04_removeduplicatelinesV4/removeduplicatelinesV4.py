#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本文件处理工具
功能：
1. 删除每行首尾的特定字符（|、全角空格、半角空格、方框）
2. 检查相邻非空行是否完全相同（跳过空行检测）
3. 将相邻重复行的第二行替换为空行
4. 批量处理多个TXT文件
"""

import os
import glob
from pathlib import Path


def clean_line(line):
    """
    清理行首尾的特定字符
    
    参数:
        line: 要清理的行
    
    返回:
        清理后的行
    """
    # 定义要删除的字符
    # | : 竖线
    # 　 : 全角空格 (U+3000)
    #   : 半角空格
    # □ : 方框 (U+25A1)
    # ■ : 实心方框 (U+25A0)
    # ◻ : 白色方框 (U+25FB)
    # ◼ : 黑色方框 (U+25FC)
    chars_to_remove = '|　 □■◻◼'
    
    # 去除首尾的特定字符
    cleaned_line = line.strip(chars_to_remove)
    
    return cleaned_line


def process_file(input_file, output_file):
    """
    处理单个文件
    
    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径
    
    返回:
        处理统计信息
    """
    try:
        # 读取文件
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        processed_lines = []
        previous_cleaned_line = None
        duplicate_count = 0
        
        for i, line in enumerate(lines):
            # 保留原始换行符
            has_newline = line.endswith('\n')
            line_without_newline = line.rstrip('\n\r')
            
            # 清理行
            cleaned_line = clean_line(line_without_newline)
            
            # 如果是空行，直接保留，不参与重复检测
            if not cleaned_line:
                # 空行：直接输出，不更新previous_cleaned_line
                processed_lines.append('\n' if has_newline else '')
                continue  # 跳过后续的重复检测逻辑
            
            # 非空行：进行重复检测
            if previous_cleaned_line is not None and cleaned_line == previous_cleaned_line:
                # 如果与前一个非空行相同，将当前行替换为空行
                processed_lines.append('\n' if has_newline else '')
                duplicate_count += 1
            else:
                # 否则保留清理后的行
                if has_newline:
                    processed_lines.append(cleaned_line + '\n')
                else:
                    processed_lines.append(cleaned_line)
            
            # 更新前一个非空行的内容（用于下次比较）
            previous_cleaned_line = cleaned_line
        
        # 写入输出文件
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)
        
        return {
            'success': True,
            'total_lines': len(lines),
            'duplicates_removed': duplicate_count
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_txt_files(input_path):
    """
    获取指定路径下的所有TXT文件
    
    参数:
        input_path: 输入路径（文件或文件夹）
    
    返回:
        TXT文件列表
    """
    if os.path.isfile(input_path):
        # 如果是单个文件
        if input_path.lower().endswith('.txt'):
            return [input_path]
        else:
            return []
    elif os.path.isdir(input_path):
        # 如果是文件夹，查找所有TXT文件
        pattern = os.path.join(input_path, '*.txt')
        return glob.glob(pattern)
    else:
        return []


def main():
    """
    主函数 - 交互式界面
    """
    print("=" * 60)
    print("文本文件处理工具 V4".center(50))
    print("=" * 60)
    print("\n功能说明:")
    print("1. 删除每行首尾的特定字符 (|、全角空格、半角空格、方框)")
    print("2. 检测相邻的完全相同的非空行（跳过空行）")
    print("3. 将重复行的第二行替换为空行")
    print("4. 保留文件中的所有空行")
    print("5. 支持批量处理多个TXT文件")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 60)
        
        # 获取输入路径
        input_path = input("\n请输入TXT文件或文件夹路径 (输入 'q' 退出): ").strip()
        
        if input_path.lower() == 'q':
            print("\n感谢使用，再见！")
            break
        
        # 去除可能的引号
        input_path = input_path.strip('"\'')
        
        # 检查路径是否存在
        if not os.path.exists(input_path):
            print(f"\n❌ 错误: 路径不存在: {input_path}")
            continue
        
        # 获取要处理的文件列表
        txt_files = get_txt_files(input_path)
        
        if not txt_files:
            print(f"\n❌ 错误: 在指定路径中未找到TXT文件")
            continue
        
        print(f"\n✓ 找到 {len(txt_files)} 个TXT文件")
        for i, file in enumerate(txt_files, 1):
            print(f"  {i}. {os.path.basename(file)}")
        
        # 获取输出路径
        output_path = input("\n请输入输出文件夹路径: ").strip()
        output_path = output_path.strip('"\'')
        
        # 确认处理
        print(f"\n准备处理:")
        print(f"  输入: {input_path}")
        print(f"  输出: {output_path}")
        print(f"  文件数量: {len(txt_files)}")
        
        confirm = input("\n是否开始处理? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\n已取消处理")
            continue
        
        # 开始处理
        print("\n" + "=" * 60)
        print("开始处理文件...")
        print("=" * 60)
        
        success_count = 0
        fail_count = 0
        total_duplicates = 0
        
        for i, input_file in enumerate(txt_files, 1):
            filename = os.path.basename(input_file)
            print(f"\n[{i}/{len(txt_files)}] 处理: {filename}")
            
            # 生成输出文件路径
            output_file = os.path.join(output_path, filename)
            
            # 处理文件
            result = process_file(input_file, output_file)
            
            if result['success']:
                print(f"  ✓ 成功!")
                print(f"    总行数: {result['total_lines']}")
                print(f"    重复行数: {result['duplicates_removed']}")
                print(f"    输出位置: {output_file}")
                success_count += 1
                total_duplicates += result['duplicates_removed']
            else:
                print(f"  ❌ 失败: {result['error']}")
                fail_count += 1
        
        # 显示总结
        print("\n" + "=" * 60)
        print("处理完成!")
        print("=" * 60)
        print(f"成功: {success_count} 个文件")
        print(f"失败: {fail_count} 个文件")
        print(f"共处理重复行: {total_duplicates} 行")
        print("=" * 60)
        
        # 询问是否继续
        continue_process = input("\n是否继续处理其他文件? (y/n): ").strip().lower()
        if continue_process != 'y':
            print("\n感谢使用，再见！")
            break


if __name__ == "__main__":
    main()
