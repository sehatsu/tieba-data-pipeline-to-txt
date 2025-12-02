#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT文件批量清理工具
功能：
1. 删除以"描述:"开头的行
2. 合并连续的"|"行为单行
3. 合并连续的空行为单行
4. 批量处理指定目录下的所有TXT文件
"""

import os
import glob


def clean_txt_file(content):
    """
    清理TXT文件内容
    
    参数:
        content: 文件内容（字符串列表）
    
    返回:
        清理后的内容（字符串列表）
    """
    cleaned_lines = []
    prev_line_type = None  # 用于跟踪前一行的类型：'pipe'（|行）、'empty'（空行）、'normal'（普通行）
    
    for line in content:
        # 检查是否是以"描述:"开头的行
        if line.strip().startswith("描述:"):
            continue  # 跳过此行
        
        # 判断当前行的类型
        current_line_type = None
        if line.strip() == "|":
            current_line_type = 'pipe'
        elif line.strip() == "":
            current_line_type = 'empty'
        else:
            current_line_type = 'normal'
        
        # 根据规则决定是否保留此行
        if current_line_type == 'pipe':
            # 如果前一行也是'pipe'，跳过当前行
            if prev_line_type == 'pipe':
                continue
            else:
                cleaned_lines.append(line)
                prev_line_type = 'pipe'
        elif current_line_type == 'empty':
            # 如果前一行也是'empty'，跳过当前行
            if prev_line_type == 'empty':
                continue
            else:
                cleaned_lines.append(line)
                prev_line_type = 'empty'
        else:
            # 普通行，直接保留
            cleaned_lines.append(line)
            prev_line_type = 'normal'
    
    return cleaned_lines


def process_txt_files(input_dir, output_dir):
    """
    批量处理TXT文件
    
    参数:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
    """
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"错误：输入目录不存在：{input_dir}")
        return
    
    # 如果输出目录不存在，创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录：{output_dir}")
    
    # 查找所有TXT文件
    txt_files = glob.glob(os.path.join(input_dir, "*.txt"))
    
    if not txt_files:
        print(f"在 {input_dir} 中没有找到TXT文件")
        return
    
    print(f"\n找到 {len(txt_files)} 个TXT文件")
    print("=" * 60)
    
    # 处理每个文件
    success_count = 0
    for txt_file in txt_files:
        try:
            filename = os.path.basename(txt_file)
            print(f"\n正在处理：{filename}")
            
            # 读取文件
            with open(txt_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            original_lines = len(lines)
            print(f"  原始行数：{original_lines}")
            
            # 清理内容
            cleaned_lines = clean_txt_file(lines)
            cleaned_count = len(cleaned_lines)
            print(f"  清理后行数：{cleaned_count}")
            print(f"  删除行数：{original_lines - cleaned_count}")
            
            # 写入输出文件
            output_file = os.path.join(output_dir, filename)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)
            
            print(f"  ✓ 已保存到：{output_file}")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ 处理失败：{str(e)}")
    
    print("\n" + "=" * 60)
    print(f"处理完成！成功处理 {success_count}/{len(txt_files)} 个文件")


def main():
    """
    主函数
    """
    print("=" * 60)
    print("TXT文件批量清理工具")
    print("=" * 60)
    print("\n功能说明：")
    print("  1. 删除以'描述:'开头的行")
    print("  2. 合并连续的'|'行为单行")
    print("  3. 合并连续的空行为单行")
    print("  4. 批量处理目录下所有TXT文件")
    print("\n" + "=" * 60)
    
    # 获取输入目录
    while True:
        input_dir = input("\n请输入TXT文件所在目录路径：").strip()
        
        # 移除可能的引号
        input_dir = input_dir.strip('"').strip("'")
        
        if os.path.exists(input_dir):
            if os.path.isdir(input_dir):
                break
            else:
                print("错误：输入的路径不是一个目录，请重新输入")
        else:
            print("错误：目录不存在，请重新输入")
    
    # 获取输出目录
    output_dir = input("\n请输入处理结果输出目录路径：").strip()
    output_dir = output_dir.strip('"').strip("'")
    
    # 确认信息
    print("\n" + "=" * 60)
    print("配置信息：")
    print(f"  输入目录：{input_dir}")
    print(f"  输出目录：{output_dir}")
    print("=" * 60)
    
    confirm = input("\n确认开始处理？(y/n): ").strip().lower()
    if confirm == 'y' or confirm == 'yes':
        print("\n开始处理...\n")
        process_txt_files(input_dir, output_dir)
    else:
        print("\n已取消操作")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断")
    except Exception as e:
        print(f"\n发生错误：{str(e)}")
    finally:
        input("\n按回车键退出...")
