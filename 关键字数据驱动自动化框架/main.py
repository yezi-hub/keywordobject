from key_word.key_word import *
from util.excel_util import Excel
from config.var_config import *
from util.time_util import get_chinese_time
from util.capture_pic import capture_pic
from util.gen_html_report import generate_html_report
from util.dir_util import create_date_hour_dir
from util.ini_file_parser import IniFileParser
import os

def gen_html_report(html_report_file_path,test_report_data):
    for i in range(len(test_report_data)):
        for j in range(len(test_report_data[i])):
            if test_report_data[i][j] is None:
                test_report_data[i][j]=""
    content = generate_html_report(test_report_data)
    with open(template_file_path, encoding="utf-8") as fp:
        html = fp.read().strip()

    with open(html_report_file_path, "a+", encoding="utf-8") as fp:
        if "<style>" in fp.read():
            fp.write("\n" + content)
        else:
            fp.write(html + content)

#test_data_execel_wb:excel的文件对象
#test_step_sheet_name:测试步骤的 sheet 名称
def execute_test_case_by_sheet_name(test_data_execel_wb,test_step_sheet_name):
    if not test_data_execel_wb:
        print("要操作的excel文件对象不存在！")
        raise Exception("要操作的excel文件对象不存在！")
    #sheet名称在exel文件中是否存在
    if test_step_sheet_name not in test_data_execel_wb.get_sheet_names():
        print("sheet名称:%s 在excel文件:%s 中不存在！" %(test_step_sheet_name,test_data_execel_wb.get_file_path()))
        raise Exception("sheet名称:%s 在excel文件:%s 中不存在！" %(test_step_sheet_name,test_data_execel_wb.get_file_path()))

    test_case_result = "成功"
    test_case_exception_info = ""
    pic_path = ""
    test_data_execel_wb.set_sheet(test_step_sheet_name)
    all_test_steps = test_data_execel_wb.get_all_rows_values()
    test_step_header = all_test_steps[0]  # 获取到测试步骤sheet的表头
    for test_no in range(1, len(all_test_steps)):
        # print(test_step)
        step_function_name = all_test_steps[test_no][test_step_keyword_col_no]
        xpath = all_test_steps[test_no][test_step_position_element_col_no]
        try:
            if xpath and "||" in xpath:
                section_name = xpath.strip().split("||")[0]
                option_name = xpath.strip().split("||")[1]
                ini_parser = IniFileParser(ini_file_path)
                xpath = ini_parser.get_option_value(section_name,option_name)
                if not xpath:
                    print("元素定位表达式：%s没有在配置文件中读到对应值：" %all_test_steps[test_no][test_step_position_element_col_no])
        except Exception as e:
            print("从配置文件读取 %s 元素定位表达式时出现异常" %(all_test_steps[test_no][test_step_position_element_col_no],e))
        value = all_test_steps[test_no][test_step_element_value_col_no]
        executed_time = get_chinese_time()
        all_test_steps[test_no][test_step_executed_time_col_no] = executed_time
        # print(step_function_name,xpath,value)
        if not xpath and not value:
            command = step_function_name + "()"
        elif xpath and not value:
            command = step_function_name + "('%s')" % xpath
        elif not xpath and value:
            command = step_function_name + "('%s')" % value
        else:
            command = step_function_name + "('%s','%s')" % (xpath, value)
        print(command)
        try:
            if "open_browser" in command:
                driver = eval(command)
            elif "key_word" in command.lower():
                sheet_name = value
                if sheet_name in test_data_execel_wb.get_sheet_names():
                    driver, test_case_result, test_case_exception_info, pic_path = execute_test_case_by_sheet_name(
                        test_data_execel_wb, sheet_name)
            else:
                eval(command)
            test_step_executed_result = "成功"
        except Exception as e:
            exception_info = traceback.format_exc()
            print("执行command: %s 命令的时候，出现异常，异常信息：%s \n %s" % (command, e, exception_info))
            exception_info = "执行command: %s 命令的时候，出现异常，异常信息：%s \n %s" % (command, e, exception_info)
            test_step_executed_result = "失败"
            all_test_steps[test_no][test_step_exception_info_col_no] = exception_info
            test_case_exception_info = exception_info
            test_case_result = "失败"
            if not isinstance(driver, str):
                pic_path = capture_pic(driver)
                all_test_steps[test_no][test_step_capture_pic_path_col_no] = pic_path
        all_test_steps[test_no][test_step_test_result_col_no] = test_step_executed_result
    #test_case_data[6] = test_case_result
    #test_case_data[7] = test_case_exception_info

    test_data_execel_wb.set_sheet("测试结果")
    #test_data_wb.write_a_line(test_case_header, fill="green")
    #test_data_wb.write_a_line(test_case_data)
    #test_data_wb.write_a_line([""])
    test_data_execel_wb.write_lines(all_test_steps, header_color="green")
    global html_report_file_path
    gen_html_report(html_report_file_path,all_test_steps)
    return driver,test_case_result,test_case_exception_info,pic_path

def execute_test_case_by_file(test_data_file_path):

    hour_dir = create_date_hour_dir(report_dir_path)
    time_file_path = get_chinese_time() + ".html"
    global html_report_file_path
    html_report_file_path = os.path.join(hour_dir, time_file_path)
    test_data_wb = Excel(test_data_file_path)
    test_data_wb.set_sheet("测试用例")
    driver = ""
    test_case_datas = test_data_wb.get_all_rows_values()
    # for test_case_data  in test_case_datas:
    #    print(test_case_data)
    test_case_header = test_case_datas[0]
    # 记录测试用例是否成功的标志
    # for test_case_data in test_case_datas[1:]:
    for i in range(1, len(test_case_datas)):
        test_case_result = "成功"
        # 获得当前用例的执行时间
        test_case_executed_time = get_chinese_time()
        test_case_datas[i][test_case_executed_time_col_no] = test_case_executed_time
        test_case_exception_info = ""
        if "y" in test_case_datas[i][test_case_executed_flag_col_no].lower():
            test_case_step_sheet_name = test_case_datas[i][test_case_sheet_name_col_no]
            driver, test_case_result, test_case_exception_info, pic_path = execute_test_case_by_sheet_name(test_data_wb,
                                                                                                           test_case_step_sheet_name)
            test_case_datas[i][test_case_test_result_col_no] = test_case_result
            test_case_datas[i][test_case_exception_info_col_no] = test_case_exception_info
            test_case_datas[i][test_case_capture_pic_path_col_no] = pic_path
            test_data_wb.set_sheet("测试结果")
            test_data_wb.write_a_line(test_case_header, fill="green")
            test_data_wb.write_a_line(test_case_datas[i])
            gen_html_report(html_report_file_path, test_case_datas)

    success_case_count = 0
    fail_case_count = 0
    case_count = 0
    for test_case_data in test_case_datas:
        if "成功" in test_case_data[test_case_test_result_col_no]:
            success_case_count += 1
        elif "失败" in test_case_data[test_case_test_result_col_no]:
            fail_case_count += 1

    case_count = success_case_count + fail_case_count
    test_data_wb.set_sheet("测试结果")
    test_data_wb.write_a_line(
        [f"用例总数:{case_count}", f"成功用例总数：{success_case_count}", f"失败用例总数：{fail_case_count}"],
        fill="blue")

    test_data_wb.save()

for i in os.listdir(test_data_dir_path):
    test_data_file_path = os.path.join(test_data_dir_path,i)
    execute_test_case_by_file(test_data_file_path)






