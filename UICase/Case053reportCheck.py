#coding=utf-8
__author__ = 'woody'
from Methods.WebDriverTools import WebDriverTools
from Methods.MemcacheTools import MemcacheTools
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import datetime, time, string, random
from Methods.LoginTools import LoginTools
from config import app
from selenium.webdriver.common.keys import Keys
import unittest, os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium import webdriver



projects = (
            (376,'青山湖',['运营报表'],'.reportListName','new'),
            (316,'企业天地',['运行报告','运营报表'],'.reportListName','new'),
            (15,'华东电网',['报表管理'],'.reportListName','new'),
            (293,'Liverpool',['Operation Reports'],'.reportListName','new'),
            (28,'中区广场',['运营报表'],'.reportListName','new'),
            (18,'香港华润',['运营报表'],'#reportNavList','old'),
            (281,'西克裕灌',['运营报表'],'.reportListName','new'),

)


downloadDir = app.config.get('DOWNLOAD_DIR')
TIMEOUT = 360
class Case053(unittest.TestCase):
    testCaseID = 'Case053'
    projectName= '早班巡查项目4'
    buzName = '检查报表内容以及是否能下载'
    start = 0.0
    now = 'None'
    startTime = ""
    url = 'http://' + app.config['SERVERIP']
    errors = []
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)


    def Test(self):
        self.errors = []
        a = WebDriverTools()
        driver = self.driver
        time.sleep(4)
        for key in projects:
            self.enterItem(driver, key[0], key[1], self.errors)
            WebDriverTools.enterPage(driver, key[2], key[3], key[1], timeout=180)
            time.sleep(5)
            if key[4] == 'old':
                self.checkOld(driver, key[1])
            else:
                self.checkNew(driver, key[1])
        #抛出异常
        self.raiseError(self.errors)



    def enterItem(self, driver, locationId, projectName, errors):
        driver.find_element_by_id("navHomeLogo").click()
        time.sleep(1)
        WebDriverTools.enterProject(driver, locationId, projectName, errors)
        time.sleep(3)

    def checkOld(self, driver, projectName):
        a = WebDriverTools()
        time.sleep(2)
        reports = driver.find_elements_by_css_selector("li[class~='list-group-item']")
        if reports == []:
            a.get_pic(driver, self.testCaseID)
            self.errors.append("进入%s项目找不到左侧报表栏!" % projectName)
        for i in range(len(reports)):
            driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].click()
            time.sleep(6)
            WebDriverTools.waitElementNotFound(driver, '.spinnerMask', self.testCaseID)
            r = driver.find_elements_by_css_selector("li[class~='list-group-item']")[i]
            contents = driver.find_elements_by_css_selector('#report-unit-1 .report-unit .summary')
            if contents != []:
                textEle = driver.find_element_by_css_selector('.step-play-list')
                WebDriverTools.checkNull(textEle, self.errors, [projectName, driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text], '内容')
                print('%s项目->%s报表存在!' % (projectName, driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text))
                if not i:
                    self.downloadPDF(driver, downloadDir, projectName,
                                     driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text, 'old')
                    self.downloadWORD(driver, downloadDir, projectName,
                                     driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text)
            else:
                reportName = driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text
                if ("月" in reportName or "onth" in reportName or reportName == 'Diagnosis Report' or reportName == '诊断报表') and int(datetime.datetime.now().day) <= 5:
                    print("5号之前月报还没生成!")
                else:
                    WebDriverTools.get_pic(driver, self.testCaseID)
                    self.errors.append('%s项目->%s报表内容为空!' % (projectName, reportName))
            '''txt = driver.find_elements_by_css_selector('#report-unit-1 .report-unit .summary')
            if len(txt) > 0:
                pass
            else:

                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                errors.append('%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text))
                #assert 0,'%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text)'''


        time.sleep(2)


    def checkNew(self, driver, projectName):
        a = WebDriverTools()
        time.sleep(5)
        reports = driver.find_elements_by_css_selector(".reportListName")
        if reports == []:
            a.get_pic(driver, self.testCaseID)
            self.errors.append("进入%s项目找不到左侧报表栏!" % projectName)
        for i in range(len(reports)):
            WebDriverTools.waitElementNotFound(driver, '.spinnerMask', self.testCaseID, timeout=TIMEOUT)
            driver.find_elements_by_css_selector(".reportListName")[i].click()
            #WebDriverTools.waitSpinner(driver, projectName + "报表--%s" % driver.find_elements_by_css_selector('.reportListName a')[i].text, timeout=180)
            try:
                WebDriverTools.waitElementNotFound(driver, '.spinnerMask', self.testCaseID, timeout=TIMEOUT)
            except Exception as e:
                WebDriverTools.get_pic(driver, self.testCaseID)
                self.errors.append(projectName + "报表--%s" % driver.find_elements_by_css_selector('.reportListName a')[i].text + '加载超时, 超过%s秒' % TIMEOUT)
            time.sleep(1.5)
            contents = driver.find_elements_by_css_selector('.report-container-wrap.report-module-text')
            if contents != []:
                textEle = driver.find_element_by_css_selector(".center.report-wrap.gray-scollbar")
                WebDriverTools.checkNull(textEle, self.errors, [projectName, driver.find_elements_by_css_selector('.reportListName a')[i].text], '内容')
                print('%s项目->%s报表存在!' % (projectName, driver.find_elements_by_css_selector('.reportListName a')[i].text))
                if not i:
                    self.downloadPDF(driver, downloadDir, projectName,
                                     driver.find_elements_by_css_selector('.reportListName a')[i].text, 'new')
            else:
                reportName = driver.find_elements_by_css_selector('.reportListName a')[i].text
                if ("月" in reportName or "onth" in reportName or reportName == 'Diagnosis Report' or reportName == '诊断报表') and int(datetime.datetime.now().day) <= 5:
                    print("5号之前月报还没生成!")
                else:
                    WebDriverTools.get_pic(driver, self.testCaseID)
                    self.errors.append('%s项目->%s报表内容为空!' % (projectName, reportName))
            '''txt = driver.find_elements_by_css_selector('#report-unit-1 .report-unit .summary')
            if len(txt) > 0:
                pass
            else:

                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                errors.append('%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text))
                #assert 0,'%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text)'''


        time.sleep(2)


    def downloadPDF(self, driver, dir, project, report, mode):
        status = False
        time.sleep(2)
        #点击下载PDF按钮
        try:
            if mode == 'old':
                driver.find_element_by_id("exportPDF").click()
            else:
                driver.find_element_by_css_selector(".pdfDownCtn.in").click()
            time.sleep(10)
        except Exception as e:
            print(e.__str__())
            WebDriverTools.get_pic(driver, self.testCaseID)
            self.errors.append("%s项目->%s报表下载PDF失败!<br>" % (project, report))
        for root,dirs,files in os.walk(dir):
            for file in files:
                if report in file and '.pdf' in file:
                    status = True
                    break
        if not status:
            print("下载PDF失败!")
            self.errors.append("%s项目->%s报表下载PDF失败!因为下载目录中未包含%s文件!" % (project, report, report))
        else:
            print("下载PDF成功!")




    def downloadWORD(self,driver,dir,project,report):
        status = False
        time.sleep(2)
        #点击下载word按钮
        try:
            driver.find_element_by_id("exportWord").click()
            time.sleep(10)
        except Exception as e:
            print(e.__str__())
            WebDriverTools.get_pic(driver, self.testCaseID)
            self.errors.append("%s项目->%s报表下载PDF失败!<br>" % (project,report))
        for root,dirs,files in os.walk(dir):
            for file in files:
                if report in file and '.doc' in file:
                    status = True
                    break
        if not status:
            print("下载WORD失败!")
            self.errors.append("%s项目->%s报表下载WORD失败!因为下载目录中未包含%s文件!" % (project, report, report))
        else:
            print("下载WORD成功!")





    def raiseError(self,error):
        if error != []:
            assert 0,"<br>".join(error)




    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.errors!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.driver.quit()
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Case053('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
