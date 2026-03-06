#!/usr/bin/env python3
"""
Kindle 2027 植物风格月历生成器
功能：自动检查并安装依赖，生成适用于 Kindle 向左旋转 90 度观看的 PDF、横向 PDF 以及 PNG 屏幕保护图片
"""

import sys
import subprocess
import os
import zipfile
import calendar
import io

# 1. 自动安装缺失的依赖包
def install_package(package):
    """尝试安装指定的 Python 包"""
    try:
        __import__(package)
        print(f"✓ 模块 '{package}' 已安装。")
        return True
    except ImportError:
        print(f"⚠ 正在安装模块 '{package}'...")
        try:
            # 使用国内镜像源加速安装
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✓ 模块 '{package}' 安装成功。")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ 模块 '{package}' 安装失败，请手动执行：pip install {package}")
            return False

# 检查并安装 Pillow (PIL) 和 reportlab
required_packages = ["Pillow", "reportlab"]
for pkg in required_packages:
    install_package(pkg)

# 2. 导入所需库（此时应已安装）
try:
    from PIL import Image, ImageDraw, ImageFont
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import landscape
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.colors import HexColor
    print("✓ 所有依赖库导入成功。")
except ImportError as e:
    print(f"✗ 导入库时出错: {e}")
    print("请手动安装所需库：pip install Pillow reportlab")
    sys.exit(1)

# 3. 主程序
def main():
    # 输出目录（改为当前脚本所在目录下的子目录，兼容 Windows）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir_png = os.path.join(base_dir, "kindle_2027_botanical_monthly_png")
    out_dir_pdf = os.path.join(base_dir, "kindle_2027_botanical_monthly_pdf")
    os.makedirs(out_dir_png, exist_ok=True)
    os.makedirs(out_dir_pdf, exist_ok=True)

    # 尝试加载更大字体（跨平台字体路径）
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",          # Windows
        "C:/Windows/Fonts/arialbd.ttf",        # Windows Bold
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",   # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Arial.ttf",     # macOS
        "/System/Library/Fonts/Arial Bold.ttf"
    ]
    
    font_title = None
    font_text = None
    font_small = None
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 28)
                font_text = ImageFont.truetype(path, 20)
                font_small = ImageFont.truetype(path, 16)
                print(f"✓ 使用字体: {path}")
                break
            except:
                continue
    
    if font_title is None:
        # 回退到默认字体（大小固定，无法放大，但可用）
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
        print("⚠ 未找到系统 TrueType 字体，使用默认位图字体（字体大小可能较小）。")

    # 生成 12 个月的 PNG 图片（800×600，适合 Kindle 屏幕保护）
    png_paths = []
    for month in range(1, 13):
        width, height = 800, 600
        img = Image.new("L", (width, height), 255)  # 白色背景
        draw = ImageDraw.Draw(img)
        
        # 月份标题
        month_name = calendar.month_name[month] + " 2027"
        bbox = draw.textbbox((0, 0), month_name, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) / 2, 30), month_name, fill=0, font=font_title)
        
        # 获取该月日历
        cal = calendar.monthcalendar(2027, month)
        
        # 日历表格参数（放大单元格）
        start_x = 80
        start_y = 100
        cell_w = 90
        cell_h = 60
        
        # 星期标题
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for i, d in enumerate(days):
            draw.text((start_x + i * cell_w, start_y), d, fill=0, font=font_text)
        
        # 日期
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    # 周末用粗体
                    if c >= 5:
                        draw.text((start_x + c * cell_w, start_y + 45 + r * cell_h), 
                                 str(day), fill=0, font=font_text)
                    else:
                        draw.text((start_x + c * cell_w, start_y + 45 + r * cell_h), 
                                 str(day), fill=0, font=font_text)
        
        # 植物风格装饰
        cx = width // 2
        base_y = height - 80
        for i in range(-8, 9):
            x = cx + i * 20
            draw.line((cx, base_y, x, base_y - 80), fill=0, width=2)
            draw.ellipse((x - 6, base_y - 84, x + 6, base_y - 72), outline=0, width=2)
        
        # 保存图片
        path = os.path.join(out_dir_png, f"2027_{month:02d}.png")
        img.save(path)
        png_paths.append(path)
        print(f"生成 PNG: {path}")

    # 将 PNG 图片打包为 ZIP
    zip_path = os.path.join(base_dir, "kindle_2027_botanical_monthly_screensavers.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for p in png_paths:
            z.write(p, os.path.basename(p))
    print(f"打包 ZIP: {zip_path}")

    # 生成横向 PDF（800×600，适合直接观看）
    landscape_pdf_path = os.path.join(base_dir, "kindle_2027_botanical_monthly_landscape.pdf")
    if png_paths:
        images = [Image.open(p) for p in png_paths]
        images[0].save(
            landscape_pdf_path,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=images[1:]
        )
        print(f"生成横向 PDF: {landscape_pdf_path}")

    # 生成适合 Kindle 向左旋转 90 度观看的 PDF（600×800，文字放大）
    # 使用 reportlab 生成纯文本 PDF，确保清晰度
    pdf_path = os.path.join(base_dir, "kindle_2027_botanical_monthly_rotated.pdf")
    
    # 页面大小（600×800 点，对应 600×800 像素，旋转后可视区域）
    from reportlab.lib.pagesizes import portrait
    from reportlab.lib.units import mm
    page_width = 600
    page_height = 800
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(page_width, page_height),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # 自定义样式 - 标题（放大）
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=HexColor('#2E5A1C')
    )
    
    # 自定义样式 - 日期（放大）
    day_style = ParagraphStyle(
        'Day',
        parent=styles['Normal'],
        fontSize=18,
        alignment=TA_CENTER
    )
    
    # 生成每个月的页面
    for month in range(1, 13):
        if month > 1:
            story.append(PageBreak())
        
        month_name = calendar.month_name[month] + " 2027"
        story.append(Paragraph(month_name, title_style))
        story.append(Spacer(1, 20))
        
        cal = calendar.monthcalendar(2027, month)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        # 星期标题
        day_row = "&nbsp;&nbsp;".join([f"<b>{d}</b>" for d in days])
        story.append(Paragraph(day_row, day_style))
        story.append(Spacer(1, 10))
        
        # 日期
        for week in cal:
            week_text = ""
            for i, day in enumerate(week):
                if day == 0:
                    week_text += "&nbsp;&nbsp;&nbsp;"
                else:
                    week_text += f"{day:2d}"
                if i < 6:
                    week_text += "&nbsp;&nbsp;&nbsp;"
            story.append(Paragraph(week_text, day_style))
            story.append(Spacer(1, 8))
        
        # 装饰文字
        story.append(Spacer(1, 20))
        botanical_decor = "~ ~ ~  ❀  ~ ~ ~  2027  ~ ~ ~  ❀  ~ ~ ~"
        story.append(Paragraph(f'<para alignment="center">{botanical_decor}</para>', day_style))
    
    doc.build(story)
    print(f"生成旋转 PDF: {pdf_path}")
    
    print("\n" + "="*50)
    print("所有文件生成完成！")
    print(f"1. 屏幕保护 PNG 图片包: {zip_path}")
    print(f"2. 横向 PDF (800×600): {landscape_pdf_path}")
    print(f"3. 旋转 PDF (600×800，适合 Kindle 向左旋转 90 度): {pdf_path}")
    print("="*50)

if __name__ == "__main__":
    main()
