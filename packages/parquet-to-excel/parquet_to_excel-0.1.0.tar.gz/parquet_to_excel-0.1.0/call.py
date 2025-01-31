from parquet_to_excel import parquet_file_to_xlsx, parquet_files_to_xlsx

# parquet_file_to_xlsx(r"D:\Projects\RustTool\data\.duck\qy_tempdata\qid=142\part0.parquet", r"D:\Felix\Desktop\out1.xlsx", "data", "")
# parquet_file_to_xlsx(r"D:\Projects\RustTool\data\.duck\qy_tempdata\qid=142\part0.parquet", r"D:\Felix\Desktop\out2.xlsx", "", "scfs")
parquet_files_to_xlsx(r"C:\Users\admin\Downloads\253_BI销售执行情况表查询", r"D:\Felix\Desktop\out1.xlsx", "data", "")
parquet_files_to_xlsx(r"C:\Users\admin\Downloads\253_BI销售执行情况表查询", r"D:\Felix\Desktop\out2.xlsx", "", "scfs")