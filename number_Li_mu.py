import os
import csv

# 获取文件夹路径
current_folder = os.path.dirname(os.path.abspath(__file__))
main_folder = current_folder
output_file_path = os.path.join(current_folder, 'number_Li_mu.csv')

# 创建或打开csv文件以附加模式写入
with open(output_file_path, mode='a', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['温度', '配位数'])
    
    # 遍历主文件夹中的所有文件夹
    for folder in os.listdir(main_folder):
        folder_path = os.path.join(main_folder, folder)
        
        if os.path.isdir(folder_path):  # 确保当前路径是文件夹
            rdf_file = os.path.join(folder_path, 'rdf_Li_mu.xvg')
            cn_file = os.path.join(folder_path, 'cn_Li_mu.xvg')
            
            data_rdf = []  
            data_cn = []   
            
            with open(rdf_file, 'r') as rdf:
                lines = rdf.readlines()
                for line in lines:
                    if not line.startswith('#') and not line.startswith('@'):
                        values = line.strip().split()
                        if len(values) == 2:
                            data_rdf.append([float(values[0]), float(values[1])])
            
            with open(cn_file, 'r') as cn:
                lines = cn.readlines()
                for line in lines:
                    if not line.startswith('#') and not line.startswith('@'):
                        values = line.strip().split()
                        if len(values) == 2:
                            data_cn.append([float(values[0]), float(values[1])])
            
            # 查找第二列的最大值后第一个最小值对应的第一列的值
            max_value = max(row[1] for row in data_rdf)
            max_index = next(i for i, row in enumerate(data_rdf) if row[1] == max_value)
            min_value = min(row[1] for row in data_rdf[max_index + 1:])
            min_index = next(i for i, row in enumerate(data_rdf[max_index + 1:]) if row[1] == min_value)
    
            result = data_rdf[max_index + 1 + min_index][0]
    
            # 查找配位数
            target_value = result
            index = min(range(len(data_cn)), key=lambda i: abs(data_cn[i][0] - target_value))
            corresponding_value = data_cn[index][1]

            writer.writerow([folder, corresponding_value])  # 写入文件夹名称和对应的配位数
            print(f"已将温度：{folder} 的配位数值写入")

print(f"已完成所有操作，并将所有结果写入 {output_file_path}")
