import re, os

import pdfplumber
from PIL import Image

from PyQt5.QtCore import QSettings, QDate

from utils import is_valid_date, is_numeric


def extract_figure_from_amm(file_path, ata):
    def is_figure_page(p):
        fig_judge_area = [0, 660, page.width, page.height]
        crop_page = p.crop(fig_judge_area)
        for line in crop_page.extract_text_lines():
            result = re.match(r"Figure(?P<figure_no>\d{3})/(?P<no>\d{2}-\d{2}-\d{2}-\d{3}-\d{3}-H\d{2}.*)", line['text'])
            if result:
                return True, f"Figure_{result.group('figure_no')}_{result.group('no')}"
        return False

    def is_task_start(p):
        matches = p.search('TASK(?P<task_no>\d{2}-\d{2}-\d{2}-\d{3}-\d{3}-H\d{2})')
        for match in matches:
            if match['x0'] < 84:
                return True, match['text'][4:]
        return False

    tasks = []
    task = {'task_no': "",
            'page_no': "",
            'figure': []}
    save_dir = f"C:\\Users\drlin\\OneDrive - Cathay Pacific Airways Limited\\Manhour\\AMM TASK FIGURE\\{ata}"
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            print(f"处理页面：{page.page_number}")
            # 判断是不是图片页面
            r = is_figure_page(page)
            if not r:  # 若不是图片
                r = is_task_start(page)
                if r:
                    if task['task_no']:
                        tasks.append(task)
                    task = {'task_no': r[1],
                            'page_no': page.page_number,
                            'figure': []}
            else:  # 保存页码
                task['figure'].append([page.page_number, r[1]])

        # 保存图片页面为图片
        for task in tasks:
            print(task)
            for page_no, figure_no in task['figure']:
                # 渲染页面为图像
                image = pdf.pages[page_no - 1].to_image(resolution=300)

                # 将图像保存为文件
                if not os.path.exists(f'{save_dir}\\{task["task_no"]}'):
                    os.makedirs(f'{save_dir}\\{task["task_no"]}')
                save_name = f'{save_dir}\\{task["task_no"]}\\{figure_no}'
                image.save(save_name + '.png', 'PNG')

                # 将图像转换为JPEG格式
                png_image = Image.open(save_name + '.png')
                jpg_image = png_image.convert('RGB')
                # 保存图像为JPEG格式
                jpg_image.save(save_name + '.jpg', 'JPEG')
                # 关闭图像
                png_image.close()
                jpg_image.close()
                os.remove(save_name + '.png')


if __name__ == '__main__':
    for x in range(70, 81):
        try:
            filename = f"sample/{x}_H__099.pdf"
            extract_figure_from_amm(filename, x)
        except:
            pass
