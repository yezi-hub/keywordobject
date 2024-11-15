from selenium import webdriver

def get_element(driver,xpath):
    try:
        # 设置隐式等待时间为 10 秒
        driver.implicitly_wait(6)
        element = driver.find_element_by_xpath(xpath)
        return element
    except Exception as e:
        print(e)
        return None

def get_elements(driver,xpath):
    try:
        # 设置隐式等待时间为 10 秒
        driver.implicitly_wait(6)
        elements = driver.find_elements_by_xpath(xpath)
        return elements
    except Exception as e:
        print(e)
        return None

if __name__ =="__main__":
    driver = webdriver.Chrome(executable_path="e:\\chromedriver.exe")
    driver.get("https://www.sogou.com")
    print(get_element(driver,"//input[@id='query']"))
    print(get_elements(driver, "//a"))
    driver.close()