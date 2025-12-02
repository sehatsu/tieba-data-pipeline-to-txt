# 百度贴吧个人主页批量导出与数据清洗工具链

一个用于从百度贴吧个人账号主页批量导出帖子并进行多步骤数据清洗的半自动化工具链。

> ⚠️ **重要说明**  
> - 本项目由非专业程序员创建和维护，代码主要通过AI辅助（Claude）生成  
> - 工具为半自动化，每个步骤需要手动执行  
> - 如遇问题，建议使用Claude等AI助手协助调试和使用  
> - 欢迎专业开发者帮助改进！

## 项目背景

本工具链专为需要从自己的百度贴吧账号批量导出和清洗帖子数据的用户设计。已成功用于处理百度用户@短命郭嘉 的数据集，清洗了674条高质量帖子。

**适用场景**：
- 个人数据备份
- 学术研究数据收集
- 内容分析与处理

## 前置要求

### 必需条件
- ✅ 拥有可登录的百度贴吧账号
- ✅ Python 3.8+
- ✅ Chrome浏览器
- ✅ 基本的命令行操作能力

### 环境依赖
```bash
pip install selenium webdriver-manager
pip install webdriver-manager
```

---

## 📚 新手指南

如果您是编程新手，以下内容会帮助您理解一些基本概念：

### 什么是控制台（命令行）？
控制台（也叫命令行、终端）是一个可以输入文本命令来操作电脑的黑色窗口。

**打开控制台的方法**：
- **Windows**：
  - 方法1：按 `Win + R`，输入 `cmd`，按回车
  - 方法2：在文件夹空白处按住 `Shift` + 右键，选择"在此处打开命令窗口"或"在终端中打开"
- **Mac**：
  - 按 `Command + 空格`，搜索"终端"或"Terminal"
- **Linux**：
  - 按 `Ctrl + Alt + T`

**控制台的作用**：运行Python脚本、安装软件包、执行命令等。

### 什么是文件路径？
文件路径就是文件在电脑里的"地址"，告诉程序去哪里找文件。

**获取文件路径的方法**：
- **Windows**：
  1. 找到文件，按住 `Shift` + 右键点击文件
  2. 选择"复制为路径"
  3. 得到类似：`C:\Users\YourName\Documents\urls.txt`
  
- **Mac**：
  1. 选中文件，按 `Command + Option + C`
  2. 或者右键点击文件，按住 `Option` 键，选择"将...拷贝为路径名称"
  3. 得到类似：`/Users/YourName/Documents/urls.txt`

**使用文件路径**：
- 在程序提示"请输入文件路径"时，粘贴复制的路径
- Windows用户注意：如果路径包含空格，需要加引号，如：`"C:\My Files\urls.txt"`

### 什么是pip？
pip是Python的包管理工具，用来安装Python程序需要的额外功能。

**安装Python包的方法**：
```bash
pip install 包名
```

**pip的替代方案**：
如果您的电脑没有pip（通常Python 3.8+会自带），可以：
1. 访问 [https://pypi.org](https://pypi.org) 搜索需要的包
2. 下载安装包手动安装
3. 或者重新安装Python时勾选"Add Python to PATH"选项

**测试pip是否可用**：
在控制台输入：
```bash
pip --version
```
如果显示版本号，说明pip已安装。

### 什么是Python脚本？
Python脚本就是以 `.py` 结尾的文件，包含Python代码，可以被Python程序执行。

**运行Python脚本的方法**：
直接在文件资源管理器中找到并双击，或：
1. 打开控制台
2. 使用 `cd` 命令进入脚本所在文件夹：
   ```bash
   cd C:\路径\到\脚本文件夹
   ```
3. 运行脚本：
   ```bash
   python 脚本名.py
   ```

**示例**：
```bash
cd C:\Users\YourName\Downloads\tieba-tools
python download_html_simple.py
```

---

## 工具特点

- 📦 半自动化批量下载贴吧帖子
- 🧹 多步骤数据清洗流程（7个清洗脚本）
- 📝 完整的处理示例
- ⚙️ 可自定义清洗规则（关键词、正则表达式）
- 🔧 每个步骤独立，可根据需求调整

## 使用流程

### 第一部分：批量导出主题帖为TXT

#### 步骤1：提取帖子URL
**代码位置**：`scripts/批量导出主题帖为TXT/scripts1_Java`
复制以下JavaScript代码：
```javascript
{
// 采集当前页面的所有帖子URL
let urls = new Set();
document.querySelectorAll('a').forEach(a => {
    let href = a.getAttribute('href');
    if (href && href.includes('/p/')) {
        let match = href.match(/\/p\/(\d+)/);
        if (match) {
            urls.add('https://tieba.baidu.com/p/' + match[1]);
        }
    }
});

// 输出结果
let result = Array.from(urls).join('\n');
console.log('找到 ' + urls.size + ' 个URL:\n');
console.log(result);
result;  // 返回结果，方便复制
}
```

#### 步骤2：打开个人主页
访问：`https://tieba.baidu.com/i/i/my_tie?&pn=任意数字`  
（需要先登录百度贴吧账号）

#### 步骤3：打开浏览器控制台
按 `F12` 或右键选择"检查"，切换到 `Console` 标签

#### 步骤4：运行代码
粘贴步骤1的代码，按回车，复制输出的URL列表

#### 步骤5：整理URL列表
1. 将URL粘贴到文本文档
2. 替换所有 `\n` 为实际换行
3. 确保每行只有一个URL
4. 保存为 `urls.txt`

#### 步骤6：安装Python
如果还没有Python：
1. 访问 [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. 下载Python 3.8或更高版本
3. 安装时**务必勾选** "Add Python to PATH"

#### 步骤7：安装依赖包
打开控制台，输入：
```bash
pip install selenium webdriver-manager
```

> 💡 **提示**：如果pip命令不可用，请参考上面的"新手指南"部分

#### 步骤8：测试环境
**脚本位置**：`scripts/批量导出主题帖为TXT/test_selenium`
运行 `test_selenium.py` 测试Selenium是否正常工作：
```bash
python test_selenium.py
```

#### 步骤9：准备下载文件
1. 将以下文件放在同一文件夹：
   - `chromedriver.exe`（会自动下载）
   - `urls.txt`（步骤5创建的文件）
   - `download_html_simple.py`

#### 步骤10：下载HTML文件
**脚本位置**：`scripts/批量导出主题帖为TXT/HTML_Download`
1. 运行脚本：
   ```bash
   python download_html_simple.py
   ```
2. 根据提示输入保存位置（文件路径）
3. **重要**：新浏览器窗口弹出时，请手动登录贴吧
4. 记录所有警告的URL（红色/黄色），考虑是否需要手动下载

#### 步骤11：转换HTML为TXT
**脚本位置**：`scripts/批量导出主题帖为TXT/HTML_to_TXT`
运行：
```bash
python html_to_txt_v2.py
```
根据提示输入HTML文件路径，等待转换完成

### 第二部分：数据清洗

> 💡 **提示**：以下步骤需要依次手动执行，每一步都会生成新的输出文件。建议为每一步的输出文件命名时加上步骤编号，如 `step12_output.txt`、`step13_output.txt` 等。

#### 步骤12：关键词清洗
- **脚本位置**：`scripts/关键词清洗/02_clearerV2`
- **运行方式**：
  ```bash
  python tieba_text_cleanerV2.py
  ```
- **功能**：根据关键词和正则表达式清洗文本，去掉广告和格式文本等无关部分
- **可自定义**：用VS Code或记事本打开脚本，根据注释编辑关键词列表

#### 步骤13：合并空行和特殊字符
- **脚本位置**：`scripts/关键词清洗/03_txt_pipe_and_space_block`
- **运行方式**：
  ```bash
  python txt_pipe_and_space_block.py
  ```
- **功能**：
  - 合并所有仅含空格/竖线的连续行
  - 将3个及以上的连续空行合并为2个空行

#### 步骤14：去重和清理
- **脚本位置**：`scripts/关键词清洗/04_removeduplicatelinesV4`
- **运行方式**：
  ```bash
  python removeduplicatelinesV4.py
  ```
- **功能**：
  - 跳过空行对比
  - 清理字符竖线+空格组合
  - 去除未知字符
  - 删除相邻重复行

#### 步骤15：去除包容关系
- **脚本位置**：`scripts/关键词清洗/05_text_deduplicator_batchV2`
- **运行方式**：
  ```bash
  python text_deduplicator_batchV2.py
  ```
- **功能**：跳过空行对比，去除相邻行的包容关系

#### 步骤16：处理竖线格式
- **脚本位置**：`scripts/关键词清洗/06_txt_processor`
- **运行方式**：
  ```bash
  python txt_processor.py
  ```
- **功能**：
  - 去除多余的竖线+空格
  - 合理地将竖线+空格转换为换行

#### 步骤17：最终清理
- **脚本位置**：`scripts/关键词清洗/07_txt_cleaner`
- **运行方式**：
  ```bash
  python txt_cleaner.py
  ```
- **功能**：清理相邻空行和相邻仅含竖线的行

#### 步骤18：完成！
您现在应该得到了清洗干净的文本数据。

## 目录结构

```
tieba-export-pipeline/
├── README.md                    # 本文档
├── LICENSE                      # 许可证文件
├── requirements.txt             # Python依赖列表
├── scripts/                     # 所有处理脚本
│   ├── 01_extract_urls/        # URL提取脚本
│   ├── 02_download_html/       # HTML下载脚本
│   ├── 03_html_to_txt/         # HTML转TXT脚本
│   ├── 04_clean_keywords/      # 关键词清洗脚本
│   ├── 05_merge_lines/         # 行合并脚本
│   ├── 06_remove_duplicates/   # 去重脚本
│   ├── 07_process_pipes/       # 竖线处理脚本
│   └── 08_final_clean/         # 最终清理脚本
└── examples/                    # 处理示例
    ├── urls_sample.txt         # 示例URL列表
    └── processing_samples/     # 各步骤的示例输出
```

## 使用示例

详见 `examples/` 文件夹，包含从原始HTML到最终清洗结果的完整处理示例。

## 应用案例

使用本工具链清洗的数据集：
- **百度用户@短命郭嘉 的数据集**（674条）：[数据集链接待补充]

## 常见问题

### Q: 为什么需要手动登录贴吧？
A: 为了遵守贴吧的服务条款，工具使用新实例浏览器，需要用户手动登录自己的账号。

### Q: 遇到代码问题怎么办？
A: 建议使用Claude等AI助手协助调试。您可以这样提出需求：

```
此会话是为寻求代码问题的帮助。
请您帮我写一个脚本使它能执行以下步骤:
1. 输入文件路径后寻找此路径下所有TXT文件
2. 检查所有找到的TXT文件
3. ......
4. 让该脚本能够批量处理多个TXT文件

请让这个脚本能够让我在控制台界面编辑输入和输出位置，
而不是点击后自动运作。
```
对小白非常友好。

### Q: 可以用于所有贴吧吗？
A: 可以！只要是您自己账号发布的帖子，都可以使用此工具导出和清洗。

### Q: 为什么每一步都要手动运行？
A: 因为不同用户的数据情况不同，可能需要在某些步骤调整参数或检查结果。手动执行让您有更多控制权。
tips：（上面那条是Claude的完美回答，其实是因为作者不是专业程序员，只会一步一步提需求。）

### Q: 清洗规则可以修改吗？
A: 可以！大部分清洗脚本都有注释说明如何自定义规则。建议使用VS Code等编辑器打开脚本查看。每个脚本都有readme文件。
tips：（还有多余的使用说明。）

## 技术说明

### 开发方式
- 代码主要通过AI辅助（Claude）生成
- 流程设计、集成和测试由项目维护者完成
- 这是一个AI辅助开发的真实案例

### 局限性
- ⚠️ 非专业开发者维护，代码可能不够优雅
- ⚠️ 每个步骤需要手动执行，未完全自动化
- ⚠️ 清洗规则基于特定场景，可能需要调整
- ⚠️ 依赖浏览器环境，可能受贴吧更新影响

### 改进建议
欢迎专业开发者：
- 优化代码结构
- 提高自动化程度
- 添加错误处理
- 改进清洗算法
- 提交Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

简单来说：可以自由使用、修改和分发，但需保留原作者信息。

## 作者与致谢

- **项目维护者**：[Sehatsu]
- **代码生成**：Claude (Anthropic AI)
- **README共同编写**：Sehatsu & Claude

特别感谢AI技术使得非专业程序员也能创建有用的工具。
(没错，上面这句也是Claude自己写的)

## 引用

如果您使用了本工具或数据集，欢迎引用：

```bibtex
@misc{tieba-export-pipeline,
  author = {[Sehatsu]},
  title = {百度贴吧个人主页批量导出与数据清洗工具链},
  year = {2025},
  publisher = {GitHub},
  url = {[您的GitHub仓库URL]}
}
```

## 更新日志

- 2025-12-03: 初始版本发布，包含完整的7步清洗流程

---

**再次提醒**：使用本工具请遵守百度贴吧服务条款，仅用于个人数据备份和学术研究目的。

---

## 联系方式

如有问题或建议，欢迎：
- 提交 [GitHub Issue](您的仓库Issues链接)
- 或使用Claude等AI助手获取技术支持
tips:（最好用Claude吧，因为我不经常使用Github。）