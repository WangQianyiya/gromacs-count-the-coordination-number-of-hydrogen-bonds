import os
import csv

def calculate_average(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 找到数据起始行的索引
    data_start = 0
    for idx, line in enumerate(lines):
        if not line.startswith('#') and not line.startswith('@'):
            data_start = idx
            break

    # 将数据转换成适合处理的格式
    values = [list(map(int, line.split()[1:2])) for line in lines[data_start:] if line.strip() and not (line.startswith('#') or line.startswith('@'))]

    # 提取第二列数据（氢键的总数）
    column_2 = [value[0] for value in values]

    # 计算平均值
    average = sum(column_2) / len(column_2)
    return average

# 获取当前代码文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 获取大文件夹路径（当前目录）
main_folder = current_directory

# 构建保存结果的 CSV 文件路径
output_file = os.path.join(current_directory, "hbnum.csv")

# 打开 CSV 文件以写入结果
with open(output_file, mode='w', newline='') as csvfile:
    fieldnames = ['T', 'File', 'Average']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历大文件夹中的子文件夹
    for foldername in os.listdir(main_folder):
        folder_path = os.path.join(main_folder, foldername)
        
        # 检查当前路径是否为文件夹
        if os.path.isdir(folder_path):
            # 进入每个子文件夹
            os.chdir(folder_path)

            # 用于存储每个文件的平均值
            file_averages = []

            # 计算每个文件的平均值，并将结果写入 CSV 文件
            for file_name in os.listdir(folder_path):
                if file_name.startswith("hbnum_") and file_name.endswith(".xvg"):
                    file_path = os.path.join(folder_path, file_name)
                    avg = calculate_average(file_path)
                    file_averages.append({'File': file_name, 'Average': avg})

            # 写入当前子文件夹的结果到 CSV 文件
            for result in file_averages:
                writer.writerow({'T': foldername, 'File': result['File'], 'Average': result['Average']})

            # 返回到代码文件所在目录
            os.chdir(current_directory)

print(f"结果已经保存到 {output_file} 文件中。")
