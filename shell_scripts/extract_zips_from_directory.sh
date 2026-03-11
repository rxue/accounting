bank_statements_dir=${1:-~/Documents/outlierx/tiliote}
mkdir -p ${bank_statements_dir}/extracted
for file in ${bank_statements_dir}/*.zip; do
    unzip -n "$file" -d ${bank_statements_dir}/extracted
done

