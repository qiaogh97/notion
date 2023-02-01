import os
import requests
from notion_client import Client
from pprint import pprint
from tabulate import tabulate
from calendar import isleap
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

def str2time(time_str):
    # 1h20m -> 80
    time = 0
    cur = ''
    for t in time_str:
        if t == 'h':
            cur = int(cur)
            time += cur * 60
            cur = ''
        elif t == 'm':
            cur = int(cur)
            time += cur
            cur = ''
        else:
            cur += t
    return time

def time2str(time):
    # 343 -> 5h43m
    h = int(time/60)
    m = time % 60
    if h == 0:
        return f'{m}m'
    elif m==0:
        return f'{h}h'
    elif h==0 and m==0:
        return '0m'
    else:
        return f'{h}h{m}m'

def get_page():
    # 利用notion api查询数据库数据
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    my_page = notion.databases.query(
        **{
            "database_id": database_id,
            #"filter": {
                #"property": "Landmark",
                #"rich_text": {
                    #"contains": "Bridge",
                #},
            #},
        }
    )
    return my_page

def get_table(ori_data_list):
    # 得到表格统计数据
    content_dict = {}
    count_dict = {}
    for ori_data in ori_data_list:
        date, number, time, content = ori_data
        if content in content_dict:
            content_dict[content] += time
            count_dict[content] += 1
        else:
            content_dict[content] = time
            count_dict[content] = 1
    total_print_list = [['内容', '总时间', '天数', '平均时间']]
    for content in content_dict:
        time = content_dict[content]
        time_str = time2str(time)
        count = count_dict[content]
        avg_time = int(time/count)
        avg_time_str = time2str(avg_time)
        total_print_list.append([content, time_str, count, avg_time_str])
    print(tabulate(total_print_list))

def get_ori_data(my_page):
    # 得到原始数据
    ori_data_list = []
    for page in my_page['results']:
        this_dict = page['properties']
        date_number = this_dict['Number']['title'][0]['text']['content']
        date, number = date_number.split('-')
        content = this_dict['Content']['select']['name']
        time_str = this_dict['Cost']['rich_text'][0]['text']['content']
        time = str2time(time_str)
        ori_data_list.append([date, number, time, content])
    return ori_data_list

def get_day_num():
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month==2:
        if isleap(year):
            return 29
        else:
            return 28
    else:
        return 30

def plt_bar(ori_data_list, cur_content='睡觉', output_path=None):
    # 画单个内容走势图
    if output_path is None:
        output_path = f'{cur_content}.png'
    day_num = get_day_num()
    date_list = [f'{year}{month:02}{day:02}' for day in range(1, day_num+1)]
    show_date_list = [day for day in range(1, day_num+1)]
    date_dict = {date:0 for date in date_list}
    for ori_data in ori_data_list:
        date, number, time, content = ori_data
        if content == cur_content:
            assert date_dict[date] == 0
            date_dict[date] = time
    time_list = [date_dict[date] for date in date_list]
    plt.figure(figsize=(12, 6))
    rects = plt.bar(show_date_list, time_list, color='red')
    plt.title(f'{cur_content}耗时走势图', fontsize=20)
    for rect in rects:
        height = rect.get_height()
        time_str = time2str(height)
        plt.text(rect.get_x() + rect.get_width()/2, height, time_str, ha='center', va='bottom')
        rect.set_edgecolor('white')
    plt.savefig(output_path)
    plt.clf()
    print(f'{cur_content} picture has been saved to path:{output_path}.')

def plt_pie(ori_data_list, output_path='3.png'):
    # 画饼图
    content_dict = {}
    for ori_data in ori_data_list:
        date, number, time, content = ori_data
        if '-' in content:
            continue
        if content in content_dict:
            content_dict[content] += time
        else:
            content_dict[content] = time

    content_list, time_list = [], []
    for content in content_dict:
        time = content_dict[content]
        content_list.append(content)
        time_list.append(time)
    my_dpi = 96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)
    plt.pie(x=time_list, labels=content_list, autopct='%.2f%%')
    plt.title(f'月级总时间分类占比图', fontsize=20)
    plt.savefig(output_path)
    plt.clf()
    print(f'Pie picture has been saved to path:{output_path}.')

def main():
    my_page = get_page()
    ori_data_list = get_ori_data(my_page)

    get_table(ori_data_list)
    plt_bar(ori_data_list, '睡觉')
    plt_bar(ori_data_list, '工作')
    plt_bar(ori_data_list, '通勤')
    plt_bar(ori_data_list, '吃饭')
    plt_bar(ori_data_list, '洗漱')
    plt_bar(ori_data_list, '计划')
    plt_bar(ori_data_list, '读书')
    plt_pie(ori_data_list)

if __name__=='__main__':
    year, month = 2023, 1
    database_id = '60b84003c1454835b590a53a85a76dd4'
    main()
    print('Done.')
