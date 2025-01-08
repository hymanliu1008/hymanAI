import zipfile  # 读压缩文件夹里面的文件
import csv
import datetime
import os
import sys
from app_usage_count import App_usage_count
from configparser import ConfigParser as NewConfigParser

class LogCheck:
    def __init__(self, open_filename, input_key):
        self.open_filename = open_filename
        self.input_key = input_key

    def result_check(self):
        rar_path = self.open_filename
        rar = zipfile.ZipFile(rar_path)
        result_check_list = []

        for file_name in rar.namelist():
            with rar.open(file_name) as f:
                data = f.readlines()
                for line in data:
                    decoded_line = line.decode()  # 解码行内容
                    if self.input_key in decoded_line:
                        result_check_list.append(f"{file_name}&{decoded_line.strip()}")  # 记录文件名和包含关键字的整行内容

        return result_check_list

if __name__ == '__main__':
    # 读取Key文件
    file_path = os.path.join(sys.path[0], "input", "Key.txt")
    with open(file_path, 'r') as f:
        keys = f.read().splitlines()

    # 打开压缩文件
    open_file = os.path.join(sys.path[0], "input", "data.zip")

    results = []
    for key in keys:
        log_check = LogCheck(open_file, key)
        results.extend(log_check.result_check())

    # 保存结果到CSV文件
    save_path = os.path.join(sys.path[0], "output", f"LKF_loadCheck_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 创建输出目录（如果不存在）

    with open(save_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in results:
            writer.writerow([row])

    # 处理日志记录
    config = NewConfigParser()
    config.read(r'offline_configure.ini')

    tool_project_id = f"{config.get('offline_info', 'tool_id')}_{config.get('offline_info', 'project_ID')}"
    log_name = "_".join([config.get("offline_info", "eid"), config.get("offline_info", "user"), config.get("offline_info", "tool_id")])
    log_outpath = config.get("offline_info", "log_outpath")

    app = App_usage_count(tool_project_id, log_name)
    app.running_count(log_outpath)
