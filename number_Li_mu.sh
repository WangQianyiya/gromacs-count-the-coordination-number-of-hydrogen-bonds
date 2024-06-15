#!/bin/bash

output_file="Li_mu.csv"

echo "wd,pws" >"$output_file"

for folder in *; do
    if [ -d "$folder" ]; then
        rdf_file="$folder/rdf_Li_mu.xvg"
        cn_file="$folder/cn_Li_mu.xvg"

        if [ -f "$rdf_file" ] && [ -f "$cn_file" ]; then
            data_rdf=()
            while IFS= read -r line || [[ -n "$line" ]]; do
                if [[ ! $line == \#* && ! $line == @* ]]; then
                    values=($line)
                    if [ ${#values[@]} -eq 2 ]; then
                        data_rdf+=("${values[0]},${values[1]}")
                    fi
                fi
            done <"$rdf_file"

            data_cn=()
            while IFS= read -r line || [[ -n "$line" ]]; do
                if [[ ! $line == \#* && ! $line == @* ]]; then
                    values=($line)
                    if [ ${#values[@]} -eq 2 ]; then
                        data_cn+=("${values[0]},${values[1]}")
                    fi
                fi
            done <"$cn_file"
            max_value=$(printf '%s\n' "${data_rdf[@]}" | awk -F',' '{print $2}' | sort -n | tail -1)
            max_index=$(printf '%s\n' "${data_rdf[@]}" | awk -F',' -v max="$max_value" '$2 == max {print NR-1}')
            min_value=$(printf '%s\n' "${data_rdf[@]:$((max_index + 1))}" | awk -F',' '{print $2}' | sort -n | head -1)
            min_index=$(printf '%s\n' "${data_rdf[@]:$((max_index + 1))}" | awk -F',' -v min="$min_value" '$2 == min {print NR-1}' | head -n 1)
            result=$(echo "${data_rdf[$((max_index + 1 + min_index))]}" | cut -d ',' -f 1)
            target_value="$result"
            index=$(printf '%s\n' "${data_cn[@]}" | awk -F',' -v target="$target_value" '{diff = $1 - target; if (diff < 0) diff = -diff; print diff, NR-1}' | sort -n | head -1 | awk '{print $2}')
            corresponding_value=$(echo "${data_cn[$index]}" | awk -F',' '{print $2}')

            echo "$folder,$corresponding_value" >>"$output_file"
            echo "wd: $folder  pws is writer"
        else
            echo "Jump：$folder，because rdf_Li_mu.xvg or cn_Li_mu.xvg is not find"
        fi
    fi
done

echo "over,and writer in: $output_file"
