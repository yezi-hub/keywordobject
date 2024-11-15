#data需要是一个二维列表
# with open("test.html",encoding="utf-8") as fp:
#     html = fp.read().strip()


def generate_html_report(*data):
    template = """  
    <table>  
    <thead>  
        <tr>  
            {head_row}  
        </tr>  
    </thead>  
    <tbody>  
        {table_rows}  
    </tbody>  
    </table>   
    <br><br>  
    """
    content = ""

    for table_data in data:
        if not table_data:
            continue  # 跳过空的表格数据

        head_row = table_data[0]
        print("表头：", head_row)

        # 生成表头
        head_cells = "".join(f"<th>{cell}</th>" for cell in head_row)

        # 生成其他行
        other_rows = ""
        for row_data in table_data[1:]:
            # 生成每行的单元格
            row_cells = "".join(f"<td>{cell}</td>" for cell in row_data)
            other_rows += f"<tr>{row_cells}</tr>\n"

            # 格式化整个表格
        table = template.format(head_row=head_cells, table_rows=other_rows)
        content += table

    return content





if __name__ == "__main__":
    from util.excel_util import  Excel
    from config.var_config import test_data_file_path
    test_report_wb = Excel(test_data_file_path)
    test_report_wb.set_sheet("测试结果")
    test_report_data = test_report_wb.get_all_rows_values()
    for i in range(len(test_report_data)):
        for j in range(len(test_report_data[i])):
            if test_report_data[i][j] is None:
                test_report_data[i][j]=""
    print("test_data:",test_report_data)
    content = generate_html_report(test_report_data,test_report_data)

    with open("test.html",encoding="utf-8") as fp:
        html = fp.read().strip()

    with open("e:\\report.html", "a+", encoding="utf-8") as fp:
        if "<style>" in fp.read():
            fp.write("\n"+content)
        else:
            fp.write(html + content)