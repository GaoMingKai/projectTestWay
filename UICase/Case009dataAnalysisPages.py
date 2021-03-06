__author__ = 'wuranxu'
from Methods.WebDriverTools import WebDriverTools
from Methods.MemcacheTools import MemcacheTools
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import datetime, time
from Methods.LoginTools import LoginTools
from config import app
import unittest



#该case用来验证数据分析各个页面是否丢失


class Case009(unittest.TestCase):
    url = "http://%s" % app.config['SERVERIP']
    testCaseID = 'Case009'
    projectName = '上海华为项目'
    buzName = '测试数据分析各个界面的内容是否丢失'
    start = 0.0
    now = 'None'
    startTime = ""

    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)

    def click_image(self):
        driver = self.driver
        #driver.implicitly_wait(8)
        #e元素为第一个图的标题，默认为untitled
        e = driver.find_element_by_css_selector("#divWSPane>div>h4.divPageTitle")
        #将鼠标移动到e元素上方30px的地方并点击，达到进入该图表的功能
        ActionChains(driver).move_to_element_with_offset(e,0,30).click().perform()


    def Test(self):
        a = WebDriverTools()
        driver = self.driver
        #driver.implicitly_wait(5)
        time.sleep(4)
        #从上海华为项目进入数据分析界面并计算加载时间
        if driver.find_element_by_css_selector(".glyphicon.glyphicon-list").is_displayed():
            try:
                WebDriverTools.enterProject(driver, 72, self.projectName)
                WebDriverTools.enterModuleByUserMenu(driver, 'btnDataAnalys', '数据分析', '.breadcrumb')
                time.sleep(1)
            except NoSuchElementException:
                WebDriverTools.get_pic(driver, self.testCaseID)
                assert 0,"登录后没有进入导航模式,地图加载失败!"
        else:
            WebDriverTools.enterProject(driver, '#project-72-shhuawei-undefined', self.projectName)
            WebDriverTools.enterModuleByUserMenu(driver, 'btnDataAnalys', '数据分析', '.breadcrumb')
            time.sleep(1)
        time.sleep(5)
        '''#获取缩略图的数量
        pic = driver.find_elements_by_css_selector("#divWSPane .effect")
        pic_len = len(pic)
        #获取图表的数量
        pic_main = driver.find_elements_by_css_selector("#anlsPane .effect")
        pic_main_len = len(pic_main)
        #进行对比
        if pic_len == pic_main_len - 1:
            print("数据分析界面->左侧缩略图和页面中间的图表数量一致!")
        else:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"数据分析界面->左侧缩略图和页面中间的图表数量不一致,请检测图标是否有丢失!(可能是添加按钮)"'''
        #获取界面左上方的目录名
        dir_name = driver.find_element_by_class_name("dropdownWS").text
        #获取界面中间目录名
        dir_name2 = driver.find_element_by_css_selector(".breadcrumb li:nth-child(2)").text
        if dir_name == dir_name2:
            print(dir_name2)
        else:
            WebDriverTools.get_pic(driver, self.testCaseID)
            assert 0,"\'工作集\'后的目录名与左侧缩略图上方的目录名显示不一致!缩略图目录名为: {} 工作集后的目录名为: {}".format(dir_name, dir_name2)
        #获取界面右侧数据源数量
        time.sleep(5)
        #2017-03-22版本取消了我的功能,没有数据组了
        # b = driver.find_elements_by_css_selector("#treeMine li")
        # mount = len(b)
        # if mount:
        #     print('数据分析界面->右侧数据源->数据组的数量为%d个!' % mount)
        # else:
        #     driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
        #     assert 0,"数据分析界面->右侧数据源->数据组的数量空,Unassigned数据组丢失!"
        #测试左右两侧折叠按钮是否生效
        lefton = 'sideTrans leftCtOpen'
        leftoff = 'sideTrans leftCtClose'
        righton = 'sideTrans rightCtOpen'
        rightoff = 'sideTrans rightCtClose'
        e1 = driver.find_element_by_id("leftCt")
        e2 = driver.find_element_by_id("rightCt")
        try:
            if e1.get_attribute("class") != lefton:
                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                assert 0,"数据分析界面->左侧折叠缩略图按钮默认应为展开状态!"
            else:
                e1.click()
                time.sleep(2)
                if e1.get_attribute("class") != leftoff:
                    driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                    assert 0,'数据分析界面->点击左侧折叠缩略图按钮后未变为折叠状态!'
                e1.click()
                time.sleep(2)
                if e1.get_attribute("class") != lefton:
                    driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                    assert 0,'数据分析界面->点击左侧折叠缩略图按钮后未变为展开状态!'
        except Exception:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"数据分析界面->左侧折叠缩略图按钮点击无效(无法折叠或展开)!"
        time.sleep(2)
        try:
            if e2.get_attribute("class") != righton:
                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                assert 0,"数据分析界面->右侧折叠数据源按钮默认应为展开状态!"
            else:
                e2.click()
                time.sleep(2)
                if e2.get_attribute("class") != rightoff:
                    driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                    assert 0,'数据分析界面->点击右侧折叠数据源按钮后未变为折叠状态!'
                e2.click()
                time.sleep(2)
                if e2.get_attribute("class") != righton:
                    driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                    assert 0,'数据分析界面->点击右侧折叠数据源按钮后未变为展开状态!'
        except Exception:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"数据分析界面->右侧折叠数据源按钮点击无效(无法折叠或展开)!"







        #点击进入工作集页面，进行测试
        driver.find_element_by_css_selector(".breadcrumb>li>a").click()
        Workplace = len(driver.find_elements_by_css_selector(".wsCtn"))
        if Workplace:
            print("数据分析->工作集->工作空间数量为%d个!" % Workplace)
        else:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"数据分析->工作集->工作空间数量为0,请检查!"
        #进入上海华为数据分析工作空间
        time.sleep(2)
        #获取工作空间的个数
        Workspace = driver.find_elements_by_css_selector(".wsCtn")
        #遍历找到自动化测试专用的工作空间

        for ele in Workspace:
            if ele.find_element_by_css_selector("span[class='name']").text == "自动化测试专用(勿删)":
                #进入该工作空间
                ele.click()
                break

        pic = driver.find_elements_by_css_selector("#divWSPane .effect")
        pic_len = len(pic)
        #获取图表的数量
        pic_main = driver.find_elements_by_css_selector("#anlsPane .effect")
        pic_main_len = len(pic_main)
        #进行对比
        if pic_len == pic_main_len - 1:
            print("数据分析界面->工作集->上海华为数据分析->左侧缩略图和页面中间的图表数量一致!")
        else:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"数据分析界面->工作集->上海华为数据分析->左侧缩略图和页面中间的图表数量不一致,请检测图标是否有丢失!"
        #点击左侧图表缩略图的第一个
        self.click_image()
        a.waitSpinner(driver,"数据分析->工作集->自动化测试专用(勿删)->左侧工作slider")
        #查看界面内容是否丢失
        time.sleep(1)
        L,L2 = [],[]
        L = driver.find_elements_by_tag_name("canvas")
        for e in range(0,len(L)):
            width = L[e].get_attribute("width")
            height = L[e].get_attribute("height")
            print("数据分析->工作空间->上海华为数据分析->图表宽度为%s" % width)
            print("数据分析->工作空间->上海华为数据分析->图表高度为%s" % height)
            if int(width) > 600 and int(height) > 600:
                pass
            else:
                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                assert 0,"数据分析->工作空间->上海华为数据分析->图表尺寸显示不正常(图表宽高度与默认值不相等)"
            print("数据分析->工作空间->图表尺寸显示正常!")

        #点击全选按钮
        time.sleep(1)
        driver.find_element_by_css_selector(".breadcrumb li:nth-child(2) a").click()
        driver.find_element_by_id("btnSelectAll").click()
        driver.find_element_by_id("btnShareTo").click()
        time.sleep(5)
        element = driver.find_elements_by_css_selector(".nav.nav-list.accordion-group .rows div")
        if len(element) > 0:
            for i in range(0,len(element)):
                print(element[i].text)
        else:
            WebDriverTools.get_pic(driver, self.testCaseID)
            assert 0,"数据分析->分享图表界面左侧的图形模块数量为0!"
        L = driver.find_elements_by_css_selector(".springConfigMask div")
        if len(L) > 0:
            for i in range(0,len(L)):
                print(L[i].get_attribute("class"))
        else:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"分享界面->编辑图表标题,WIKI id等控件没有找到!"
        try:
            driver.execute_script("$('#ulTools span').click()")
        except:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"数据分析->工作集->选中工作空间->进入分享界面,未找到分享报表的确认按钮!"
        #a.find_spinner(driver,cur_time=time.time(),project="分享界面->点击ok按钮后进入分享记录界面",timeout='23')
        time.sleep(6)
        driver.find_element_by_css_selector(".modal-content>div>button>span").click()
        time.sleep(1.2)
        N = driver.find_elements_by_css_selector(".divShareLog .row.rowShareLogContent")
        if len(N):
            print("该用户的分享记录为%d条!" % len(N))
        else:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"分享界面->点击sure按钮分享图表->进入分享记录页面时分享记录为空!"
        ActionChains(driver).move_to_element(driver.find_element_by_css_selector(".divShareLog>div")).perform()
        driver.find_element_by_css_selector(".divShareLog>div .shareOperate span:nth-child(3)").click()
        time.sleep(2)
        #driver.switch_to_alert().accept()

        try:
            sure = [x for x in driver.find_elements_by_css_selector(".btn.btn-info.alert-button") if x.text == '确认']
            sure[0].click()
            #driver.find_elements_by_css_selector(".btn.btn-info.alert-button")[0].click()
        except Exception as e:
            assert 0,"数据分析--进入我的分享--删除分享记录时没有弹出是否删除该分享记录的提示窗口"

        #a.find_spinner(driver,time.time(),'分享报表后预览该报表','23')
        time.sleep(2)
        N2 = driver.find_elements_by_css_selector(".divShareLog .row.rowShareLogContent")
        if len(N2) == len(N) - 1:
            print("删除分享记录成功!分享记录为%d条." % len(N2))
        else:
            driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,'数据分析->选择图表->分享图表->删除该分享记录失败!'








    def tearDown(self):
        self.driver.quit()
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Case009('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)