#!/bin/bash

# 计算平均值的函数
calculate_average() {
    file_path="$1"
    # 从第几行开始读取数据
    data_start=$(grep -n -vE '^\s*#|^\s*$' "$file_path" | head -n 1 | cut -d: -f1)
    # 计算平均值
    average=$(awk -v data_start="$data_start" 'NR > data_start { sum += $2; count++ } END { print sum / count }' "$file_path")
    echo "$average"
}

# 获取当前脚本所在目录
current_directory=$(dirname "$(readlink -f "$0")")

# 获取大文件夹路径（当前目录）
main_folder="$current_directory"

# 构建保存结果的 CSV 文件路径
output_file="$current_directory/hbnum.csv"

# 写入 CSV 文件头部
echo "T,File,Average" >"$output_file"

# 遍历大文件夹中的子文件夹
for foldername in "$main_folder"/*; do
    if [ -d "$foldername" ]; then
        cd "$foldername" || exit

        # 用于存储每个文件的平均值
        file_averages=()

        # 计算每个文件的平均值，并将结果写入 CSV 文件
        for file_name in "$foldername"/hbnum_*.xvg; do
            if [ -f "$file_name" ]; then
                avg=$(calculate_average "$file_name")
                file_averages+=("$file_name,$avg")
            fi
        done

        # 写入当前子文件夹的结果到 CSV 文件
        for result in "${file_averages[@]}"; do
            echo "$foldername,$result" >>"$output_file"
        done

        # 返回到脚本文件所在目录
        cd "$current_directory" || exit
    fi
done

echo "结果已经保存到 $output_file 文件中。"
