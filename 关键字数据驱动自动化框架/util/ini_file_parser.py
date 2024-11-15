import configparser
import os

class IniFileParser:

    def __init__(self,ini_file_path):
        if not os.path.exists(ini_file_path):
            print("ini文件 %s 的路径不存在！" %ini_file_path)
            self.ini_file_path = None
            return
        self.ini_file_path = ini_file_path
        # 创建一个配置解析器
        self.config = configparser.ConfigParser()
        # 读取 UTF-8 编码的 INI 文件
        with open(self.ini_file_path, 'r', encoding='utf-8') as config_file:
            self.config.read_file(config_file)



    #获取当前类中存储的ini文件的方法
    def get_ini_file_path(self):
        return self.ini_file_path

    def set_ini_file_path(self,ini_file_path):
        if not os.path.exists(ini_file_path):
            print("ini文件 %s 的路径不存在！" %ini_file_path)
            self.ini_file_path = None
            return
        self.ini_file_path = ini_file_path
        self.config.read(ini_file_path)#读取配置文件的配置信息

    def get_option_value(self,section_name,option_name):
        if self.config.has_option(section_name, option_name):
            return self.config[section_name][option_name]
        return None

if __name__ == "__main__":
    ini_parser = IniFileParser("e:\\pytest.ini")
    print(ini_parser.get_option_value("pytest","python_files"))