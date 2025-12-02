#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贴吧HTML批量下载器 - 简化版
解决登录和配置冲突问题
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pathlib import Path
import json

class SimpleTiebaDownloader:
    def __init__(self, output_dir="downloaded_html"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.progress_file = self.output_dir / "progress.json"
        self.downloaded = self.load_progress()
        self.driver = None
    
    def load_progress(self):
        """加载进度"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()
    
    def save_progress(self):
        """保存进度"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(list(self.downloaded), f)
    
    def setup_driver(self):
        """设置浏览器 - 使用独立的新实例"""
        print("正在启动浏览器...")
        
        chrome_options = Options()
        
        # 关键设置：避免与现有Chrome冲突
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 设置窗口大小
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 不使用现有配置，避免冲突
        chrome_options.add_argument("--disable-extensions")
        
        try:
            # 优先使用 webdriver-manager
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✓ 使用 webdriver-manager 启动成功")
            except ImportError:
                # 使用本地驱动
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✓ 使用本地驱动启动成功")
            
            print("✓ 浏览器已启动")
            
            # 设置超时
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            return True
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            print()
            print("解决方法：")
            print("1. 关闭所有Chrome窗口")
            print("2. 确保已安装: pip install webdriver-manager")
            print("3. 重新运行脚本")
            return False
    
    def wait_for_login(self):
        """等待用户手动登录"""
        print()
        print("="*60)
        print("【第一步：登录贴吧】")
        print("="*60)
        print()
        print("请在打开的浏览器中登录百度贴吧：")
        print("1. 点击右上角「登录」")
        print("2. 输入账号密码登录")
        print("3. 登录成功后，回到这里")
        print()
        
        input("登录完成后，按回车继续...")
        print()
        print("✓ 开始下载...")
        print()
    
    def download_page(self, url):
        """下载单个页面"""
        try:
            print(f"  访问中...", end='', flush=True)
            self.driver.get(url)
            
            # 等待页面加载
            time.sleep(2)
            
            # 检查是否需要登录
            if "登录" in self.driver.page_source and "请登录后继续操作" in self.driver.page_source:
                print(" 需要登录！")
                return False
            
            # 等待主要内容
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "l_post"))
                )
            except:
                pass
            
            # 保存HTML
            html = self.driver.page_source
            post_id = url.split('/p/')[-1].split('?')[0]
            
            html_file = self.output_dir / f"{post_id}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # 记录进度
            self.downloaded.add(url)
            self.save_progress()
            
            print(" ✓", flush=True)
            return True
            
        except Exception as e:
            print(f" ❌ {e}", flush=True)
            return False
    
    def run(self, urls_file, delay=3):
        """主运行函数"""
        # 读取URL
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        print(f"✓ 找到 {len(urls)} 个URL")
        
        # 过滤已下载
        remaining = [url for url in urls if url not in self.downloaded]
        
        if not remaining:
            print("✓ 所有页面已下载！")
            return
        
        print(f"✓ 已完成 {len(urls) - len(remaining)} 个")
        print(f"✓ 还需下载 {len(remaining)} 个")
        print()
        
        # 启动浏览器
        if not self.setup_driver():
            return
        
        try:
            # 先访问百度，等待登录
            print("正在打开百度贴吧...")
            self.driver.get("https://tieba.baidu.com")
            time.sleep(2)
            
            # 等待用户登录
            self.wait_for_login()
            
            # 开始下载
            print("="*60)
            print(f"开始下载 {len(remaining)} 个页面")
            print(f"预计时间: {len(remaining) * delay / 60:.1f} 分钟")
            print("="*60)
            print()
            
            success = 0
            failed = 0
            
            for i, url in enumerate(remaining, 1):
                print(f"[{i}/{len(remaining)}] {url}", end='')
                
                if self.download_page(url):
                    success += 1
                else:
                    failed += 1
                
                # 显示进度
                if i % 10 == 0:
                    print()
                    print(f"  进度: {i}/{len(remaining)}, 成功: {success}, 失败: {failed}")
                    print()
                
                # 延迟
                time.sleep(delay)
            
            print()
            print("="*60)
            print("✓ 下载完成！")
            print(f"  成功: {success}")
            print(f"  失败: {failed}")
            print(f"  保存位置: {self.output_dir.absolute()}")
            print("="*60)
            
        except KeyboardInterrupt:
            print()
            print("⚠️  用户中断")
            print("进度已保存，下次运行将继续")
        
        finally:
            if self.driver:
                self.driver.quit()


def main():
    print("="*60)
    print("贴吧HTML批量下载器 - 简化版")
    print("="*60)
    print()
    
    if not Path("urls.txt").exists():
        print("❌ 找不到 urls.txt")
        input("按回车退出...")
        return
    
    # 设置参数
    output_dir = input("保存位置（直接回车: downloaded_html）: ").strip() or "downloaded_html"
    delay = input("间隔秒数（直接回车: 3秒）: ").strip()
    delay = float(delay) if delay else 3.0
    
    print()
    print(f"✓ 保存到: {output_dir}/")
    print(f"✓ 间隔: {delay} 秒")
    print()
    
    confirm = input("确认开始？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    print()
    
    # 开始
    downloader = SimpleTiebaDownloader(output_dir=output_dir)
    downloader.run("urls.txt", delay=delay)
    
    print()
    input("按回车退出...")


if __name__ == "__main__":
    main()
