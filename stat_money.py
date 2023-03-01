import os
import requests
import pickle
from notion_client import Client
from pprint import pprint
from tabulate import tabulate
from calendar import isleap
import matplotlib.pyplot as plt
from notion_client.helpers import iterate_paginated_api
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

en_to_zh = {'Eating':'餐饮', 
            'Commute':'交通',
            'DailyGoods':'日用品',
            'DailyExpenses':'日常消耗',
            'VirtualRecharge':'虚拟充值',
            'ElectricProducts':'电子产品',
            'Medicinal':'医药',
           }
def get_page():
    # 利用notion api查询数据库数据
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    block_list = []
    for block in iterate_paginated_api(notion.databases.query, database_id=database_id):
        block_list.append(block)
    return block_list    

def get_ori_data_from_list(block_list):
    # 得到原始数据
    ori_data_list = []
    for my_page in block_list:
        for page in my_page:
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
    cost_list = [round(date_dict[date], 2) for date in date_list]

    plt.figure(figsize=(12, 6))
    rects = plt.bar(show_date_list, cost_list, color='red')
    plt.title(f'{year}年{month}月开销走势图', fontsize=20)
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
    #total_print_list = [['内容', '总开销', '比例', '天数', '平均开销']]
    total_print_list = [['Content', 'Total', 'Ratio', 'Days', 'Average Cost']]
    total_cost = sum(content_dict.values())
    for content in content_dict:
        cost = content_dict[content]
        count = count_dict[content]
        avg_cost = cost/count
        ratio = f'{cost / total_cost:.2%}'
        total_print_list.append([content, f'{cost:.2f}', ratio, count, f'{avg_cost:.2f}'])
    print(tabulate(total_print_list, headers='firstrow', tablefmt='grid'))
    print(f'一月总开销：{total_cost}')

    # 画饼图
    content_list, cost_list = [], []
    for content in content_dict:
        cost = content_dict[content]
        zh_content = en_to_zh[content]
        content_list.append(zh_content)
        cost_list.append(round(cost, 2))
    my_dpi = 96
    plt.figure(figsize=(720/my_dpi, 720/my_dpi), dpi=my_dpi)
    patches, texts = plt.pie(cost_list, labels=content_list, pctdistance=1.2)
    for t in texts:
        t.set_size(12)
    total_cost = sum(cost_list)
    cost_percent_list = [f'{cost/total_cost:.2%}' for cost in cost_list]
    labels = [f'{i} {j} ({v}元)' for i,j,v in zip(content_list, cost_percent_list, cost_list)]
    patches, labels, dummy = zip(*sorted(zip(patches, labels, cost_list), key=lambda x:x[2], reverse=True))
    plt.legend(patches, labels, loc='best', fontsize=8)
    plt.title(f'{year}年{month}月开销分类占比图', fontsize=28)
    plt.tight_layout()
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
    pickle_filepath = f'./money/{year}_{month}_block_list.pickle'
    if os.path.exists(pickle_filepath):
        pickle_file = open(pickle_filepath, 'rb')
        block_list = pickle.load(pickle_file)
        pickle_file.close()
        print(f'load block_list from {pickle_filepath}')
    else:
        block_list = get_page()
        pic = open(pickle_filepath, 'wb')
        pickle.dump(block_list, pic)
        pic.close()
        print(f'load from url')
        print(f'save block_list to {pickle_filepath}')
    ori_data_list = get_ori_data_from_list(block_list)
    with open(f'./money/{year}_{month}_content.txt', 'w') as fw:
        for ori_data in ori_data_list:
            for data in ori_data:
                fw.write(str(data))
                fw.write(' ')
            fw.write('\n')
    get_table_pie(ori_data_list, f'./money/{year}_{month}_pie.png')
    plt_bar(ori_data_list, f'./money/{year}_{month}_bar.png')


if __name__=='__main__':
    #year, month = 2023, 1
    #database_id = 'e905dcdab9f5435a8c82a6143e63b0b5'
    year, month = 2023, 2
    database_id = '8ca148df9e6e48d3baa6e09b59d6e957'
    main()
    print('Done.')
