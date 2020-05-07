# 问题二求解

import os

if __name__ == "__main__":
    path_data_cleansing = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/附件3数据预处理/'
    path_data_cluster = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/聚类分析/'
    os.system('python3 ' + path_data_cleansing + "data_cleansing_fj3.py")  # 附件3数据预处理

    os.system('python3 ' + path_data_cleansing + "groupby_user.py")  # 去除30天内同一用户相似度0.75+的留言

    os.system('python3 ' + path_data_cluster + "cluster.py")  # 聚类分析 导出 表2-导出热点问题留言明细表
    os.system('python3 ' + path_data_cluster + "generate_table1.py")  # 导出 表1-热点问题表
