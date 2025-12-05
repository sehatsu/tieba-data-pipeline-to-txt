#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贴吧文本批量清理脚本
功能：批量替换TXT文件中的格式文本为"|"字符
作者：Claude
"""

import os
import re
from pathlib import Path

def create_replacement_patterns():
    """
    创建替换模式列表
    返回: 正则表达式模式列表
    """
    # 基础关键词列表 (精确匹配) - 根据用户提供的列表
    exact_keywords = [
        # 贴吧基础UI元素
        "日一二三四五六",
        "吧主推荐",
        ">0<",
        "加载中...",
        "我也说一句",
        "http://tieba.baidu.com",
        "发贴请遵守贴吧协议及“七条底线”",
        "收起回复",
        "开通SVIP免",
        "贴吧热议榜",
        "©2025 Baidu贴吧协议",
        "隐私政策",
        "吧主制度",
        "意见反馈",
        "网络谣言警示",
        "本吧因你更精彩，明天继续来努力！",
        "<返回",
        "百度小说人气榜",
        "其他分类榜",
        "热推榜",
        "萍踪侠影 作者：梁羽生",
        "极品家丁 作者：禹岩",
        "临高启明 作者：吹牛者",
        "夜天子 作者：月关",
        "择天记 作者：猫腻",
        "分类：其他分类",
        "|>>",
        "剑来 作者：烽火戏诸侯",
        "分类：奇幻玄幻",
        "执魔 作者：我是墨水",
        "红楼梦 作者：曹雪芹",
        "分类：古典文学",
        "萍踪侠影 作者：梁羽生",
        "诛仙 作者：萧鼎",
        "凡人修仙传 作者：忘语",
        "完美世界 作者：辰东",
        "雪中悍刀行 作者：烽火戏诸侯",
        "吞噬星空 作者：我吃西红柿",
        "红楼 作者：未设置",
        "本作品吧",
        "作者：刘慈欣",
        "给本吧投票",
        "皇冠身份发贴红色标题显示红名签到六倍经验",
        "更多定制特权",
        "兑换本吧会员",
        "吧主申请名人堂，解锁更多会员特权",
        "本吧专属印记",
        "定制名片背景名人自动顶贴定制头像边框",
        "收起特权",
        "兑换本吧会员",
        "贴吧页面",
        "违规贴吧举报反馈通道",
        "贴吧违规信息处理公示",
        "跳到 页 确定",
        "开通超级会员发贴6倍经验",
        "想用@提到谁？添加什么话题?",
        "签到排名：今日本吧第个签到，",
        "一键签到成为超级会员，使用一键签到",
        "一键签到",
        "看贴 图片 | 视频 游戏",
        "贴子管理 |",
        "想用@提到谁？",
        "添加什么话题?",
        "使用云相册收藏工具，批量收藏精美图片！立即安装",
        "系统繁忙，请稍后再试！",
        "抱歉，您没有权限进行该项操作",
        "下一页 尾页",
        "可签7级以上的吧50个",
        "看贴 图片",
        "游戏 1 2",
        "我在贴吧 短命郭嘉 0",
        "扫二维码下载贴吧客户端下载贴吧APP看高清直播",
        "变身嫁人",
        "作者：未设置",
        "分类：都市言情",
        "水浒 作者：施耐庵",
        "封神原著 作者：许仲琳",
        "|！",
        "快试试吧，可以对自己使用挽尊卡咯~",
        "游戏！",
        "贴吧投诉",
        "、视频！",
        "视频！",
        "分享到:",
        "分享到：",
        "<|",
        "收起回复",
        "发贴请遵守贴吧协议及“七条底线”贴吧投诉",
        "|隐私政策|吧主制度|意见反馈|网络谣言警示",
        "|>>",
        "- ",
        "1 2 ",
        "◆◆",
        "游戏 ",

        # 广告相关
        "广告",
        "不感兴趣",
        "开通SVIP免广告",
        "光速出刀，刀刀烈火，亿万爆率，小怪爆极品！",
        "全新魔幻页游-抢先版全新魔幻打金，在线即玩，快来体验！",
        " 全新魔幻页游-抢先版【装备全靠打】",
        
        # 楼层管理
        "隐藏此楼查看此楼",
        "该楼层疑似违规已被系统折叠",
        "禁言",
        "|解禁",
        "|删除",
        "只看楼主收藏 回复",
        "删除 |",
        "只看楼主收藏回复",
        
        # 会员功能
        "皇冠身份发贴红色标题显示红名签到六倍经验兑换本吧会员赠送补签卡1张，获得[经验书购买权]",
        "赠送补签卡1张，获得[经验书购买权]",
        
        # 个人信息
        "[管理]",
        "[获取]",
        "我的本吧信息",
        "本吧牛人排行榜",
        "查看我的印记",
        
        # 社交分享
        "百度贴吧微信新浪微博QQ空间复制链接",
        
        # 客户端下载
        "扫二维码下载贴吧客户端下载贴吧APP看高清直播、视频！",
        
        # 页脚信息
        "贴吧页面意见反馈违规贴吧举报反馈通道贴吧违规信息处理公示",
        
        # 发帖相关
        "发表回复",
        "发贴请遵守贴吧协议及\"七条底线\"贴吧投诉",
        "停止浮动",
        "内 容:",
        "使用签名档",
        "查看全部",
        "发 表",
        "保存至快速回贴",
        "退 出",
        
        # APP通知
        "发布成功去贴吧APP订阅抽奖结果通知扫码进入贴吧APP···········开奖后第一时间站内信通知···········中奖结果全员公示",
        "去贴吧APP订阅抽奖结果通知",
        "扫码进入贴吧APP···········开奖后第一时间站内信通知···········中奖结果全员公示",
        "开奖后第一时间站内信通知",
    ]
    
    # 包含数字的模式 (需要正则表达式) - X表示任意数字
    number_patterns = [
        # 签到系统
        r"签到排名：今日本吧第\d+个签到，本吧因你更精彩，明天继续来努力！",
        r"签到排名：今日本吧第\d+个签到，",
        r"本吧排名：\d+",
        r"本吧签到人数：\d+",
        r"一键签到可签7级以上的吧50个一键签到",
        r"本月漏签\d+次！",
        r"\d+成为超级会员，赠送8张补签卡如何使用？",
        r"点击日历上漏签日期，即可进行补签。",
        r"连续签到：天",
        r"累计签到：天",
        r"\d+超级会员单次开通12个月以上，赠送连续签到卡3张使用连续签到卡",
        r"\d{2}月\d{2}日漏签\d+天",  # 匹配日期漏签格式
        
        # 广告文本 (具体的广告内容)
        r"倪大红传奇-每天送10W充值卡\d+新养老传奇，上线送10W真充卡，零氪玩到退休！",
        r"全新魔幻页游-抢先版【高爆率专服】上线送\d+套时装，送满级VIP，\d+倍高爆地图秒开！",
        r" \d+Shy哥嘴硬王者,输T1赖运气\d+",
        r"\d+清者自清血洗弹幕!ELK离队引群嘲\d+",
        r"收到：\d+ \d+ \d+ ↑",
        r"收到：\d+ \d+ \d+ ↓",
        r"收到：\d+ \d+ ↑",
        r"收到：\d+ \d+ ↓",
        r"当前票数：\d+",
        r"\d+回复贴，共\d+页",
        r"本吧排行： 第\d+名",
        r"收到：\d+ \d+ \d+",
        r"收到：\d+ \d+ \d+",
        r"收到：\d+ \d+",
        r"收到：\d+ \d+",
        r"关注：\d+贴子：\d+",
        r"人气总榜 \d+",
        r"收到：\d+ ",
     
        
        
        # IP属地信息
        r"IP属地:[^\s|]+",
        
        
        # 热议榜 (匹配 "数字+文字+数字" 的格式)
        r"\d+[\u4e00-\u9fa5,，.。!！\s]{5,60}\d{5,}",
    ]
    
    # 合并所有模式
    all_patterns = []
    
    # 添加精确匹配的关键词
    for keyword in exact_keywords:
        all_patterns.append(re.escape(keyword))
    
    # 添加包含数字的模式
    all_patterns.extend(number_patterns)
    
    return all_patterns

def clean_text(text, patterns):
    """
    清理文本中的格式内容
    
    参数:
        text: 原始文本
        patterns: 替换模式列表
    返回:
        清理后的文本
    """
    cleaned_text = text
    
    # 逐个应用替换模式
    for pattern in patterns:
        cleaned_text = re.sub(pattern, '|', cleaned_text)
    
    # 清理连续的竖线（可选，保持整洁）
    cleaned_text = re.sub(r'\|+', '|', cleaned_text)
    
    return cleaned_text

def process_files(input_dir, output_dir):
    """
    批量处理文件
    
    参数:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 检查输入目录是否存在
    if not input_path.exists():
        print(f"❌ 错误: 输入目录不存在: {input_dir}")
        return
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 获取替换模式
    patterns = create_replacement_patterns()
    print(f"✓ 已加载 {len(patterns)} 个替换规则")
    
    # 获取所有txt文件
    txt_files = list(input_path.glob("*.txt"))
    
    if not txt_files:
        print(f"❌ 在目录 {input_dir} 中未找到任何txt文件")
        return
    
    print(f"✓ 找到 {len(txt_files)} 个txt文件")
    print("=" * 60)
    
    # 处理每个文件
    success_count = 0
    error_count = 0
    
    for i, file_path in enumerate(txt_files, 1):
        try:
            print(f"[{i}/{len(txt_files)}] 正在处理: {file_path.name}")
            
            # 读取文件
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 清理文本
            cleaned_content = clean_text(content, patterns)
            
            # 保存到输出目录
            output_file = output_path / file_path.name
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"    ✓ 已保存到: {output_file}")
            success_count += 1
            
        except Exception as e:
            print(f"    ❌ 处理失败: {e}")
            error_count += 1
    
    # 显示统计信息
    print("=" * 60)
    print(f"处理完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {error_count} 个文件")
    print(f"输出目录: {output_dir}")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("贴吧文本批量清理工具")
    print("=" * 60)
    print()
    
    # 获取输入目录
    while True:
        input_dir = input("请输入TXT文件所在目录的路径: ").strip()
        if input_dir:
            # 支持引号路径
            input_dir = input_dir.strip('"').strip("'")
            break
        print("❌ 路径不能为空，请重新输入")
    
    print()
    
    # 获取输出目录
    while True:
        output_dir = input("请输入清理后文件的输出目录路径: ").strip()
        if output_dir:
            # 支持引号路径
            output_dir = output_dir.strip('"').strip("'")
            break
        print("❌ 路径不能为空，请重新输入")
    
    print()
    print("=" * 60)
    
    # 确认信息
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print()
    
    confirm = input("确认开始处理? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消操作")
        return
    
    print()
    
    # 处理文件
    process_files(input_dir, output_dir)
    
    print()
    input("按回车键退出...")

if __name__ == "__main__":
    main()
