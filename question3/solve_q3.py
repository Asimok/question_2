# 问题三求解

import os

if __name__ == "__main__":
    path_data_cleansing = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/附件4数据预处理/'
    path_data_evaluate = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/'
    os.system('python3 ' + path_data_cleansing + "data_cleansing_fj4.py")  # 附件4数据预处理

    os.system('python3 ' + path_data_evaluate + "及时性/promptness.py")  # 求解及时性
    os.system('python3 ' + path_data_evaluate + "可解释性/interpretability.py")  # 求解可解释性
    os.system('python3 ' + path_data_evaluate + "完整性/integrity.py")  # 求解完整性
    os.system('python3 ' + path_data_evaluate + "相关性/correlation.py")  # 求解相关性

    os.system('python3 ' + path_data_evaluate + "评价方案/correlation.py")  # 导出评价方案
