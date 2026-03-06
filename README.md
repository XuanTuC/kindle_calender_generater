# kindle_calender_generater

这是一个专为 Kindle 设备设计的 2027 年月历生成工具，可自动生成三种格式的月历文件，特别针对 Kindle 向左旋转 90 度的使用场景优化，并放大字体以提高可读性。

功能特性

• 🌿 植物风格设计：简洁优雅的植物风格装饰，适合 Kindle 电子墨水屏显示

• 📱 多格式输出：一次性生成 PNG 图片包、横向 PDF 和旋转版 PDF

• 🔄 Kindle 旋转优化：专为 Kindle 向左旋转 90 度的使用场景设计

• 🔍 字体放大：所有格式均放大字体，提高在 Kindle 上的可读性

• 🎨 周末高亮：周末日期使用不同样式标识

• 📦 自动化依赖安装：运行脚本自动检查并安装所需 Python 库

• 💻 跨平台兼容：支持 Windows、macOS 和 Linux 系统

生成的文件

脚本运行后会生成以下文件：

1. 屏幕保护 PNG 图片包 (kindle_2027_botanical_monthly_screensavers.zip)
   • 包含 12 个月的 PNG 图片 (800×600 像素)

   • 可直接用作 Kindle 屏幕保护程序

2. 横向 PDF 文件 (kindle_2027_botanical_monthly_landscape.pdf)
   • 800×600 尺寸

   • 适合直接在 Kindle 上横向查看

3. 旋转版 PDF 文件 (kindle_2027_botanical_monthly_rotated.pdf)
   • 600×800 尺寸

   • 专为 Kindle 向左旋转 90 度设计

   • 字体进一步放大，便于阅读

快速开始

前提条件

• Python 3.6 或更高版本

• 网络连接（用于自动下载依赖）

安装运行

1. 下载脚本
   git clone https://github.com/XuanTuC/kindle_calender_generater.git
   cd kindle_calender_generater
   

2. 运行脚本
   python kindle-calendar-generator.py
   

脚本会自动检查并安装所需的依赖包（Pillow 和 reportlab），然后开始生成月历文件。

使用方法

将文件传输到 Kindle

1. 通过 USB 连接：
   • 将 Kindle 通过 USB 连接到电脑

   • 将生成的 PDF 文件复制到 Kindle 的 documents 文件夹

   • 安全弹出设备，在 Kindle 的图书馆中查看

2. 通过邮件发送（仅限支持个人文档服务的 Kindle）：
   • 将 PDF 文件发送到您的 Kindle 邮箱地址

   • 主题可留空或写 "convert" 以启用亚马逊的格式转换

Kindle 设置建议

1. 旋转版 PDF 使用：
   • 打开旋转版 PDF 文件 (kindle_2027_botanical_monthly_rotated.pdf)

   • 点击屏幕右上角的 Aa 图标

   • 选择「布局」→「横向」或使用旋转功能

   • 调整缩放级别以获得最佳显示效果

2. 屏幕保护程序设置：
   • 解压 PNG 图片包

   • 将图片传输到 Kindle

   • 在 Kindle 设置中，选择「设备选项」→「高级选项」→「屏幕保护程序」

   • 选择喜欢的月历图片作为屏幕保护

自定义选项

如需修改脚本以适应您的需求，可调整以下参数：

在 generate.py 中修改：

1. 年份修改：
   # 将 2027 改为其他年份
   month_name = calendar.month_name[month] + " 2028"  # 改为 2028
   

2. 字体大小调整：
   # PNG 图片字体大小
   font_title = ImageFont.truetype(path, 28)  # 标题字体大小
   font_text = ImageFont.truetype(path, 20)   # 正文字体大小
   
   # PDF 字体大小
   fontSize=24,  # 标题字体大小
   fontSize=18,  # 日期字体大小
   

3. 颜色调整：
   # 修改植物风格装饰颜色
   textColor=HexColor('#2E5A1C')  # 深绿色
   

项目结构


kindle-botanical-calendar/
├── generate.py              # 主脚本文件
├── README.md                # 本说明文件
├── kindle_2027_botanical_monthly_screensavers.zip
├── kindle_2027_botanical_monthly_landscape.pdf
└── kindle_2027_botanical_monthly_rotated.pdf


常见问题

1. 运行时提示 "No module named 'PIL'"

脚本已包含自动安装依赖功能。如果仍出现此错误，请手动安装：
pip install Pillow reportlab


2. 生成的图片字体太小

脚本会尝试使用系统 TrueType 字体。如果系统中没有可用字体，会回退到位图字体。建议在 Windows 上确保 Arial 字体可用，或在代码中指定其他字体路径。

3. Kindle 上显示不清晰

• 确保使用旋转版 PDF 并正确设置横向显示

• 在 Kindle 上调整对比度设置

• 确保图片分辨率为 800×600（Kindle 分辨率）

4. 想生成其他年份的月历

修改脚本中所有出现 "2027" 的地方为您想要的年份，然后重新运行脚本。

技术细节

• 分辨率适配：800×600 像素适配大部分 Kindle 型号

• 字体处理：自动检测系统字体，回退到默认字体

• 依赖管理：自动安装 Pillow 和 reportlab 库

• 跨平台：兼容 Windows、macOS 和 Linux

贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目：

1. Fork 本项目
2. 创建功能分支 (git checkout -b feature/AmazingFeature)
3. 提交更改 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 开启 Pull Request

许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

致谢

• 感谢 Amazon Kindle 提供的优秀阅读体验

• 使用 Pillow 和 reportlab 库进行图像和 PDF 处理

• 植物设计灵感来自自然主题的日历设计

支持

如有问题或建议，请：
1. 查看 #常见问题 部分
2. 在 GitHub 提交 https://github.com/yourusername/kindle-botanical-calendar/issues
3. 通过电子邮件联系开发者

希望这个工具能帮助您在 Kindle 上更好地管理时间！📅✨
