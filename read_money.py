import os
import requests
from notion_client import Client
from pprint import pprint
from tabulate import tabulate
from calendar import isleap
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

def get_page():
    # 利用notion api查询数据库数据
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    # 2023-01
    database_id = 'e905dcdab9f5435a8c82a6143e63b0b5'
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

def get_ori_data(my_page):
    # 得到原始数据
    ori_data_list = []
    for page in my_page['results']:
        this_dict = page['properties']
        date_number = this_dict['Number']['title'][0]['text']['content']
        date, number = date_number.split('-')
        content = this_dict['Content']['select']['name']
        cost = this_dict['Cost']['number']
        ori_data_list.append([date, number, content, cost])
    return ori_data_list

def plt_bar(ori_data_list, output_path='2.png'):
    # 画柱状图
    day_num = get_day_num()
    date_list = [f'{year}{month:02}{day:02}' for day in range(1, day_num+1)]
    show_date_list = [day for day in range(1, day_num+1)]

    date_dict = {date:0 for date in date_list}
    for ori_data in ori_data_list:
        date, number, content, cost = ori_data
        date_dict[date] += cost
    cost_list = [date_dict[date] for date in date_list]

    plt.figure(figsize=(12, 6))
    rects = plt.bar(show_date_list, cost_list, color='red')
    plt.title(f'每日开销走势图', fontsize=20)
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, height, height, ha='center', va='bottom')
        rect.set_edgecolor('white')
    plt.savefig(output_path)
    plt.clf()
    print(f'Bar picture has been saved to path:{output_path}.')

def get_table_pie(ori_data_list, output_path='1.png'):
    # 统计分类表格
    content_dict = {}
    count_dict = {}
    for ori_data in ori_data_list:
        date, number, content, cost = ori_data
        if content in content_dict:
            content_dict[content] += cost
            count_dict[content] += 1
        else:
            content_dict[content] = cost
            count_dict[content] = 1
    total_print_list = [['内容', '总开销', '比例', '天数', '平均开销']]
    total_cost = sum(content_dict.values())
    for content in content_dict:
        cost = content_dict[content]
        count = count_dict[content]
        avg_cost = cost/count
        ratio = f'{cost / total_cost:.2%}'
        total_print_list.append([content, cost, ratio, count, avg_cost])
    print(tabulate(total_print_list))
    print(f'一月总开销：{total_cost}')

    # 画饼图
    content_list, cost_list = [], []
    for content in content_dict:
        cost = content_dict[content]
        content_list.append(content)
        cost_list.append(cost)
    my_dpi = 96
    plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)
    plt.pie(x=cost_list, labels=content_list, autopct='%.2f%%')
    plt.title(f'开销分类占比图', fontsize=20)
    plt.savefig(output_path)
    plt.clf()
    print(f'Pie picture has been saved to path:{output_path}.')

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

def main():
    my_page = get_page()
    ori_data_list = get_ori_data(my_page)
    get_table_pie(ori_data_list)
    plt_bar(ori_data_list)


if __name__=='__main__':
    year, month = 2023, 1
    database_id = '60b84003c1454835b590a53a85a76dd4'
    main()
    print('Done.')
