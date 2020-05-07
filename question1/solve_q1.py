# 问题一求解

import os

if __name__ == "__main__":
    path_data_cleansing = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question1/附件2数据预处理/'
    path_model = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question1/model/'
    os.system('python3 ' + path_data_cleansing + "data_cleansing_fj2.py")  # 附件2数据预处理
    os.system('python3 ' + path_data_cleansing + "resize_dataset.py")  # 分割  训练集 验证集 测试集
    os.system('python3 ' + path_model + "run.py")  # 模型训练
    os.system('python3 ' + path_model + "model_predict.py")  # 模型预测
