__author__ = 'sophia'
from Methods.LoginTools import LoginTools
from Methods.OtherTools import OtherTools
from Methods.MemcacheTools import MemcacheTools
import unittest
import datetime, time
from Methods.WebDriverTools import WebDriverTools
from config import app
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys

class Case047(unittest.TestCase):
    testCaseID = 'Case047'
    projectName = "无"
    buzName = '数据分析图表分享链接'
    now = 'None'
    errors = []
    url = "http://%s" % app.config['SERVERIP']
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID, {'start':self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)
        self.tools = WebDriverTools()

    def Test(self):
        driver = self.driver
        self.errors = []
        self.tools.enterModuleByUserMenu(driver,'btnDataAnalys','数据分析','#divAnlsDatasourcePane')
        self.check(driver)

    def check(self,driver):
        WebDriverWait(driver, 20).until(lambda x: x.find_element_by_css_selector('.breadcrumb'))
        sleep(5)
        driver.find_element_by_css_selector(".breadcrumb>li>a").click()
        sleep(5)
        WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_css_selector('.wsCtn'))
        Workspace = driver.find_elements_by_css_selector(".wsCtn")
        for ele in Workspace:
            if ele.find_element_by_css_selector("span[class='name']").text == "自动化测试专用(勿删)":
                #进入该工作空间
                ele.click()
                break
        WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_css_selector('.slider-cb'))
        driver.find_elements_by_css_selector('.slider-cb')[0].click()
        driver.find_element_by_css_selector('#btnShareTo').click()
        sleep(4)
        driver.find_element_by_css_selector('#ulTools>span').click()
        WebDriverTools.waitElement(driver, '#divShareIframe', self.testCaseID,timeout=20)
        name=driver.find_element_by_css_selector('#divShareIframe >iframe')
        driver.switch_to.frame(name)
        try:
            WebDriverWait(driver, 20).until_not(lambda x: x.find_element_by_css_selector('.loadingMask'))
        except Exception as e:
            print(e.__str__())
            assert 0,'数据分析分享图表一直在加载'
        driver.find_element_by_css_selector('#lkCopyLink').click()
        sleep(2)
        driver.find_element_by_css_selector('.infoBox-footer>button').click()
        driver.get("http://%s" % app.config['SERVERIP'])
        driver.find_element_by_tag_name('input').send_keys(Keys.CONTROL+"v")
        link=driver.execute_script("a=$(\'input\').val();return a")
        driver.get(link)
        sleep(4)
        try:
            result=driver.find_element_by_css_selector('#lkCopyLink').text
            if(result=='复制链接'):
                print('数据分析分享报表链接成功')
        except Exception as e:
            print(e.__str__())
            assert 0,'数据分析分享报表链接错误'

    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.errors!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        self.driver.quit()
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Case047('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    sleep(5)