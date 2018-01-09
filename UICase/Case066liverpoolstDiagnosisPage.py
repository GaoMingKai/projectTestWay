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
from selenium.webdriver.common.action_chains import ActionChains
class Case066(unittest.TestCase):
    testCaseID = 'Case066'
    projectName = "175LiverpoolStreet"
    buzName = '检查Diagnosis页面是否正常'
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    project = (293,'175LiverpoolStreet')
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
        self.tools.enterProject(driver, self.project[0], self.project[1], self.errors)
        sleep(3)
        self.checkDiagnosis(driver)
        OtherTools.raiseError(self.errors)

    #检查Operation Summary目录下的页面
    def checkDiagnosis(self,driver):
        page=['Diagnosis']
        self.tools.enterPage(driver,page,'#floorCt', self.projectName)
        self.tools.checkNavigation(driver,self.errors,page,4)
        driver.find_element_by_css_selector('#btnNoticeHistory').click()
        sleep(3)
        historyLog=driver.find_element_by_css_selector('#historyLog')
        self.tools.checkNull(historyLog,self.errors,page,'历史日志')
        historyLog.find_element_by_css_selector('div > button').click()
        # sleep(3)
        # driver.find_element_by_css_selector('#btnNoticeConfig').click()
        # sleep(3)
        # diagnosisConfig=driver.find_element_by_css_selector('#diagnosisConfig')
        # self.tools.checkNull(diagnosisConfig,self.errors,page,'配置')
        # diagnosisConfig.find_element_by_css_selector('div > button').click()


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
    suite.addTest(Case066('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)