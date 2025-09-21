import pypandoc
from pathlib import Path
import sys
import re

# 简单的用法: python scripts/markdown2pdf.py [输入Markdown文件(可选，默认 README.md)] [输出文件 (可选, 默认 output.pdf)]

input_md = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('README.md')
output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.pdf'

if not input_md.exists():
    print(f"找不到输入文件: {input_md}")
    sys.exit(1)

markdown_text = input_md.read_text(encoding='utf-8')

# 处理表格单元内的换行: Pandoc 一般会识别 <br>，但某些情况下（版本/扩展差异）会被忽略。
# 策略：
# 1. 确保使用 raw_html 扩展开启（在 format 中指定）。
# 2. 作为兜底，将表格行中竖线之间的 <br> 标记替换为显式 LaTeX 换行符 \\ (不影响普通段落)。

def replace_br_in_table(line: str) -> str:
    if '|' not in line or line.strip().startswith('| ---'):
        return line
    # 仅替换表格数据单元中的 <br> 或 <br/> 或 <br /> 为 LaTeX 换行命令。
    return re.sub(r'<br\s*/?>', r' \\\\ ', line)

processed_lines = []
in_table_block = False
for raw_line in markdown_text.splitlines():
    line = raw_line
    if '|' in line:
        in_table_block = True
        line = replace_br_in_table(line)
    else:
        in_table_block = False
    processed_lines.append(line)

markdown_text = '\n'.join(processed_lines)

# 说明: 如果 blockquote 仍然显示为 '>'，可以先输出中间 LaTeX 结果调试。
debug_latex = False  # 需要查看中间结果时改为 True

if debug_latex:
    latex_code = pypandoc.convert_text(
        markdown_text,
        'latex',
        format='gfm+raw_html',  # 开启 raw_html 以识别 <br>
        extra_args=[
            '--standalone',
            '--include-in-header=quote.sty'
        ]
    )
    Path('debug.tex').write_text(latex_code, encoding='utf-8')
    print('已生成 debug.tex 供检查。')

pypandoc.convert_text(
    markdown_text,
    'pdf',
    format='gfm+raw_html',  # gfm + raw_html 支持 <br>
    outputfile=output_file,
    extra_args=[
        '--standalone',
        '--pdf-engine=xelatex',
        '-V', 'mainfont=PingFang SC',
        # 统一页面边距，避免左边过宽或内容看起来溢出右侧
        '-V', 'geometry:top=20mm,left=18mm,right=18mm,bottom=22mm',
        '--include-in-header=quote.sty'
    ]
)

print("PDF 已生成:", output_file)