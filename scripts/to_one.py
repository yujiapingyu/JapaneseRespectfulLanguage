import os

# 文件夹路径
folder = './日语敬语'
# 需要拼接的文件名，按顺序
filenames = ['尊敬語', '謙譲語', '其他']
indexs = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
# 输出文件路径
output_file = folder + '/日语敬语汇总.md'

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write('# 日语敬语汇总\n\n')
    for i, fname in enumerate(filenames):
        file_path = os.path.join(folder, f'{fname}.md')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(f'## {indexs[i]}、{fname}\n\n')
                outfile.write(infile.read())
                outfile.write('\n\n')
        else:
            print(f'文件未找到: {file_path}')