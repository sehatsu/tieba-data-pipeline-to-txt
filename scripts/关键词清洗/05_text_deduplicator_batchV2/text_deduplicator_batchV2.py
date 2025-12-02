#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贴吧文本批量去重工具 - 相邻行智能去重版
功能：
1. 删除指定字符（|、全角空格、半角空格、�）
2. 检查相邻的非空行是否存在字符相同且排序相同的文本（跳过空行检测）
3. 若发现包含关系，删除较短的那行（转换为空行）
4. 支持批量处理整个目录
注：检测时会跳过原文件中的空行，只比较非空行之间的关系，但保留所有空行
"""

import os
import sys
from pathlib import Path


def clean_line(line):
    """
    步骤1：删除指定字符
    删除字符：| 　(全角空格) (半角空格) �
    """
    chars_to_remove = ['|', '　', ' ', '�']
    cleaned = line
    for char in chars_to_remove:
        cleaned = cleaned.replace(char, '')
    return cleaned


def is_subsequence(shorter, longer):
    """
    检查shorter的所有字符是否按顺序出现在longer中
    这是"交叉对比"的实现：检查字符相同且排序相同
    """
    if not shorter:  # 空字符串
        return True
    
    shorter_idx = 0
    longer_idx = 0
    
    while shorter_idx < len(shorter) and longer_idx < len(longer):
        if shorter[shorter_idx] == longer[longer_idx]:
            shorter_idx += 1
        longer_idx += 1
    
    return shorter_idx == len(shorter)


def should_delete_line(line1, line2):
    """
    步骤2-3：检查两行是否存在包含关系
    返回：
        - 1: 删除第一行
        - 2: 删除第二行  
        - 0: 都不删除
    """
    # 先清理两行
    clean1 = clean_line(line1)
    clean2 = clean_line(line2)
    
    # 跳过空行
    if not clean1.strip() or not clean2.strip():
        return 0
    
    # 如果两行完全相同，删除任意一行（这里删除第二行）
    if clean1 == clean2:
        return 2
    
    # 判断包含关系
    len1 = len(clean1)
    len2 = len(clean2)
    
    if len1 < len2:
        # line1较短，检查line1是否是line2的子序列
        if is_subsequence(clean1, clean2):
            return 1  # 删除较短的line1
    else:
        # line2较短，检查line2是否是line1的子序列
        if is_subsequence(clean2, clean1):
            return 2  # 删除较短的line2
    
    return 0


def process_file(input_path, output_path, show_details=False):
    """
    主处理函数
    """
    try:
        # 读取所有行
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if show_details:
            print(f"  → 读取文件... ✓ (共 {len(lines)} 行)")
        
        # 标记要删除的行（转为空行）
        lines_to_keep = [True] * len(lines)
        deleted_count = 0
        
        # 找出所有非空行的索引（跳过空行检测）
        if show_details:
            print(f"  → 分析相邻的非空行...")
        
        non_empty_indices = []
        for i, line in enumerate(lines):
            cleaned = clean_line(line.rstrip('\n'))
            if cleaned.strip():  # 非空行
                non_empty_indices.append(i)
        
        if show_details:
            print(f"  → 找到 {len(non_empty_indices)} 个非空行")
        
        # 检查相邻的非空行（跳过文件中的空行）
        for i in range(len(non_empty_indices) - 1):
            idx1 = non_empty_indices[i]
            idx2 = non_empty_indices[i + 1]
            
            # 跳过已经被标记删除的行
            if not lines_to_keep[idx1] or not lines_to_keep[idx2]:
                continue
            
            line1 = lines[idx1].rstrip('\n')
            line2 = lines[idx2].rstrip('\n')
            
            result = should_delete_line(line1, line2)
            
            if result == 1:
                lines_to_keep[idx1] = False
                deleted_count += 1
            elif result == 2:
                lines_to_keep[idx2] = False
                deleted_count += 1
        
        if show_details:
            print(f"  → 发现 {deleted_count} 行重复内容")
        
        # 生成输出内容（被删除的行变为空行）
        output_lines = []
        for i, line in enumerate(lines):
            if lines_to_keep[i]:
                output_lines.append(line)
            else:
                output_lines.append('\n')  # 空行
        
        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)
        
        if show_details:
            print(f"  → 写入输出文件... ✓")
        
        return {
            'success': True,
            'original': len(lines),
            'deleted': deleted_count,
            'kept': len(lines) - deleted_count
        }
        
    except PermissionError as e:
        return {
            'success': False,
            'error': f'权限错误: {e}'
        }
    except FileNotFoundError as e:
        return {
            'success': False,
            'error': f'文件未找到: {e}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'处理失败: {e}'
        }


def get_txt_files(directory):
    """
    获取目录下所有的TXT文件
    """
    txt_files = []
    try:
        for file in Path(directory).rglob('*.txt'):
            if file.is_file():
                # 检查文件是否可读
                if os.access(file, os.R_OK):
                    txt_files.append(file)
                else:
                    print(f"  ⚠ 跳过无读取权限的文件: {file.name}")
    except PermissionError as e:
        print(f"  ⚠ 扫描目录时遇到权限错误: {e}")
    return txt_files


def main():
    """
    主函数：交互式输入
    """
    print("\n" + "=" * 60)
    print(" " * 10 + "贴吧文本批量去重工具 - 相邻行智能版")
    print("=" * 60)
    print("\n功能说明：")
    print("  1. 删除字符：| 　(全角空格) (半角空格) �")
    print("  2. 检查相邻的非空行是否存在包含关系（字符相同且排序相同）")
    print("  3. 删除较短的行（转换为空行）")
    print("  4. 支持批量处理整个目录")
    print("  注：检测时跳过原文件中的空行，只比较非空行之间的关系")
    print("=" * 60 + "\n")
    
    # 获取输入路径
    while True:
        input_path = input("请输入TXT文件所在的目录路径（或单个文件路径）：").strip()
        
        if not input_path:
            print("❌ 路径不能为空，请重新输入。\n")
            continue
        
        # 去除可能的引号
        input_path = input_path.strip('"').strip("'")
        
        if not os.path.exists(input_path):
            print(f"❌ 路径不存在：{input_path}\n")
            continue
        
        # 检查读取权限
        if os.path.isfile(input_path):
            if not os.access(input_path, os.R_OK):
                print(f"❌ 文件没有读取权限：{input_path}\n")
                continue
        else:
            if not os.access(input_path, os.R_OK):
                print(f"❌ 目录没有读取权限：{input_path}\n")
                continue
        
        break
    
    # 获取输出路径
    while True:
        output_path = input("请输入处理结果的输出目录路径：").strip()
        
        if not output_path:
            print("❌ 路径不能为空，请重新输入。\n")
            continue
        
        # 去除可能的引号
        output_path = output_path.strip('"').strip("'")
        
        # 如果输出目录不存在，询问是否创建
        if not os.path.exists(output_path):
            create = input(f"输出目录不存在，是否创建？(y/n): ").strip().lower()
            if create == 'y':
                try:
                    os.makedirs(output_path, exist_ok=True)
                    print(f"✓ 已创建目录：{output_path}\n")
                    break
                except PermissionError:
                    print(f"❌ 创建目录失败：没有权限\n")
                    continue
                except Exception as e:
                    print(f"❌ 创建目录失败：{e}\n")
                    continue
            else:
                continue
        else:
            # 检查写入权限
            if not os.access(output_path, os.W_OK):
                print(f"❌ 输出目录没有写入权限：{output_path}\n")
                continue
            break
    
    print()
    print("=" * 60)
    
    # 判断输入是文件还是目录
    if os.path.isfile(input_path):
        # 处理单个文件
        files_to_process = [Path(input_path)]
        print(f"检测到单个文件：{input_path}")
    else:
        # 处理目录下所有TXT文件
        print(f"正在扫描目录：{input_path}")
        files_to_process = get_txt_files(input_path)
        print(f"找到 {len(files_to_process)} 个可读取的TXT文件")
    
    if not files_to_process:
        print("❌ 没有找到可处理的TXT文件，程序退出。")
        input("\n按回车键退出...")
        return
    
    print()
    confirm = input("是否开始处理？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消处理。")
        input("\n按回车键退出...")
        return
    
    print()
    print("开始处理文件...")
    print("=" * 60)
    
    # 处理每个文件
    success_count = 0
    fail_count = 0
    total_deleted = 0
    failed_files = []
    
    for i, file_path in enumerate(files_to_process, 1):
        # 构建输出文件路径
        output_file = Path(output_path) / f"dedup_{file_path.name}"
        
        print(f"\n[{i}/{len(files_to_process)}] {file_path.name}")
        
        # 决定是否显示详细信息
        show_details = len(files_to_process) <= 10  # 文件少于10个时显示详细信息
        
        result = process_file(file_path, output_file, show_details)
        
        if result['success']:
            print(f"  ✓ 处理成功")
            print(f"    原始: {result['original']:,} 行")
            print(f"    删除: {result['deleted']:,} 行 ({result['deleted']/result['original']*100:.1f}%)")
            print(f"    保留: {result['kept']:,} 行")
            success_count += 1
            total_deleted += result['deleted']
        else:
            print(f"  ✗ 处理失败")
            print(f"    原因: {result['error']}")
            fail_count += 1
            failed_files.append((file_path.name, result['error']))
    
    # 打印总结
    print()
    print("=" * 60)
    print("处理完成！")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")
    print(f"总共删除: {total_deleted:,} 行重复内容")
    
    if failed_files:
        print()
        print("失败文件详情：")
        for filename, error in failed_files:
            print(f"  - {filename}")
            print(f"    {error}")
    
    print("=" * 60)
    
    # 等待用户按键
    input("\n按回车键退出...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断。")
        input("\n按回车键退出...")
    except Exception as e:
        print(f"\n\n发生未预期的错误：{e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
