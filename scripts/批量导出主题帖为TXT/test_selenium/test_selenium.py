#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selenium 测试脚本
验证安装是否成功
"""

def test_selenium():
    print("="*60)
    print("Selenium 安装测试")
    print("="*60)
    print()
    
    # 测试1: 检查selenium包
    print("【测试1】检查selenium包...")
    try:
        import selenium
        print(f"✓ selenium版本: {selenium.__version__}")
    except ImportError:
        print("❌ selenium未安装")
        print("请运行: pip install selenium")
        return False
    
    print()
    
    # 测试2: 检查webdriver-manager
    print("【测试2】检查webdriver-manager（可选）...")
    try:
        import webdriver_manager
        print(f"✓ webdriver-manager已安装")
    except ImportError:
        print("⚠️  webdriver-manager未安装（可选）")
        print("推荐安装: pip install webdriver-manager")
    
    print()
    
    # 测试3: 启动浏览器
    print("【测试3】启动Chrome浏览器...")
    print("（浏览器会自动打开，然后自动关闭）")
    print()
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # 尝试使用webdriver-manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ 使用webdriver-manager启动成功")
        except:
            # 使用本地驱动
            driver = webdriver.Chrome(options=chrome_options)
            print("✓ 使用本地ChromeDriver启动成功")
        
        # 访问百度测试
        print("正在访问百度...")
        driver.get("https://www.baidu.com")
        
        import time
        time.sleep(2)
        
        # 获取标题
        title = driver.title
        print(f"✓ 页面标题: {title}")
        
        # 关闭浏览器
        driver.quit()
        print("✓ 浏览器已关闭")
        
        print()
        print("="*60)
        print("✓ 所有测试通过！Selenium安装成功！")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()
        print("可能的原因：")
        print("1. 未安装ChromeDriver")
        print("2. ChromeDriver版本与Chrome不匹配")
        print("3. Chrome浏览器未安装")
        print()
        print("解决方法：")
        print("1. 安装webdriver-manager: pip install webdriver-manager")
        print("2. 或手动下载ChromeDriver（参考 Selenium安装指南.md）")
        print()
        return False


if __name__ == "__main__":
    test_selenium()
    print()
    input("按回车退出...")
