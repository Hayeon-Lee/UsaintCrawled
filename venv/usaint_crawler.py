import os
from ssl import CHANNEL_BINDING_TYPES
import time
from xmlrpc.client import FastParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def Shutdown(_time):
    os.system("shutdown -s -t " + str(_time))

def WaitForClass_CanBeClicked(driver, delaySec, class_name):
    wait = WebDriverWait(driver, delaySec)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))

def WaitForClass_Visible(driver, delaySec, class_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    
def WaitForID_Visible(driver, delaySec, id_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.ID, id_name)))

def WaitForTag_Visible(driver, delaySec, tag_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))

def Login(self, driver, id, password):
    driver.get('https://saint.ssu.ac.kr/irj/portal')
    WaitForClass_CanBeClicked(driver, 10, "btn_login")
    driver.find_element_by_class_name('btn_login').click()

    #id = '20201759'
    #password = 'dlstod!26'

    id = "20201759"
    pw = "dlstod!26"

    driver.find_element_by_xpath('//*[@id="userid"]').send_keys(id)
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)

    driver.find_element_by_xpath('//*[@id="sLogin"]/div/div[1]/form/div/div[2]/a').click()
    #print("로그인 됨")

def FirstPage(self, driver):
    time.sleep(10)

    driver.switch_to.frame('contentAreaFrame')
    driver.switch_to.frame('isolatedWorkArea')
    
    tmp1 = driver.find_element_by_xpath('/html/body/div/div[1]/div[1]')
    tmp2 = driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]')
    tmp3 = driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]')
    tmp4 = driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]/ul')
    
    FirstPage_table = []
    
    #학번
    studentID_1 = tmp4.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]/ul/li[1]')
    studentID_2 = studentID_1.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]/ul/li[1]/dl/dd/a/strong')
    studentID_f = int(float(studentID_2.text))
    FirstPage_table.append(studentID_f)
    
    #학년과 학기
    studentGrade_1 = tmp4.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]/ul/li[4]')
    studentGrade_2 = studentGrade_1.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]/ul/li[4]/dl/dd/a/strong')
    studentGrade_3 = studentGrade_2.text
    studentGrade_4 = studentGrade_3.split(':')
    studentGrade_5 = studentGrade_4[0]
    studentGrade_f = studentGrade_5[0]
    FirstPage_table.append(int(float(studentGrade_f)))
    
    studentSemester_1 = studentGrade_4[1]
    studentSemester_f = studentSemester_1[0]
    FirstPage_table.append(int(float(studentSemester_f)))
    
    #재학 중인지
    studentEnrolled_1 = tmp4. find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]/ul/li[3]')
    studentEnrolled_2 = studentEnrolled_1.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[2]/ul/li[3]/dl/dd/a/strong')
    studentEnrolled_3 = studentEnrolled_2.text
    studentEnrolled_f = False
    if "재학" in studentEnrolled_3 :
        studentEnrolled_f = True
    else:
        studentEnrolled_f = False
    FirstPage_table.append(studentEnrolled_f)
    
    #프레임 다시 돌아가기
    driver.switch_to.default_content()
    return FirstPage_table

def GradeList(self, driver):
    ################ 학사관리 페이지로 이동
    driver.find_element_by_xpath('//*[@id="ddba4fb5fbc996006194d3c0c0aea5c4"]/a').click()
    
    ################ 성적/졸업 페이지로 이동
    driver.find_element_by_xpath('//*[@id="8d3da4feb86b681d72f267880ae8cef5"]/a').click()

    ################ 팝업창 제거하기
    WaitForClass_Visible(driver, 10, 'lsBlockLayer')
    element = driver.find_element_by_class_name('lsBlockLayer')
    driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", element)
    element = driver.find_element_by_id('URLSPW-0')
    driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", element)
    
    driver.switch_to.frame('contentAreaFrame')
    driver.switch_to.frame('isolatedWorkArea')
    
    WaitForClass_Visible(driver, 10, 'urSTSStd') #표 보여질 때까지 기다려
    Lists = driver.find_elements_by_class_name('urSTSStd')
    t1 = Lists[0].find_element_by_xpath('//*[@id="WD38-content"]/table')
    
    #취득학점과 이수학점 구하기
    t2 = t1.find_elements_by_tag_name('tr')
    t3 = []
    for i in range(0, len(t2), 1):
        tmp = t2[i].get_attribute('class')
        if(tmp!=''):
            n = int(t2[i].get_attribute('rr')) #성적이 들어있는 줄만
            if(n>0):
                t3.append(t2[i])
                
    listenList = []
    scoreList = []
    
    for i in range(0, len(t3), 1):
        tmp = t3[i].find_elements_by_tag_name('td') #한 요소씩 넣기
        if "여름" not in tmp[2].text and "겨울" not in tmp[2].text:
            listenList.append(float(tmp[4].text))
            scoreList.append(float(tmp[6].text))
    
    listenList = list(reversed(listenList))#1학년 1학기부터
    scoreList = list(reversed(scoreList))#1학년 1학기부터
    
    GradeList_table = [] #반환값
    GradeList_table.append(listenList)
    GradeList_table.append(scoreList)
    
    #학적부 평점평균 구하기
    tmp1 = driver.find_element_by_xpath('//*[@id="WD11"]/tbody/tr[6]')
    tmp2 = tmp1.find_element_by_xpath('//*[@id="WD0129"]/tbody/tr[2]')
    tmp3 = tmp2.find_element_by_xpath('//*[@id="WD011A"]')
    graduateScore_1 = tmp3.get_attribute('lsdata') #인풋데이터라 이렇게 얻어와야함
    graduateScore_2 = graduateScore_1.split("\'")
    graduateScore_f = float(graduateScore_2[1])
    GradeList_table.append(graduateScore_f)
    
    #프레임 다시 돌아가기
    driver.switch_to.default_content()
    return GradeList_table

def CheckGrade(self, driver):
    ################ 졸업사정표 페이지로 이동
    driver.find_element_by_xpath('//*[@id="30f2303171c98bdf57db799d0b834646"]/a/span/em').click()
    driver.switch_to.frame('contentAreaFrame')
    driver.switch_to.frame('isolatedWorkArea')
    #print("프레임 바뀜")

    time.sleep(7)

    table = driver.find_element_by_xpath('/html/body/table')
    tr = table.find_element_by_tag_name('tbody')
    tr_1 = tr.find_element_by_tag_name('tr')
    tr_2 = tr_1.find_element_by_tag_name('td')
    tr_3 = tr_2.find_element_by_xpath('//*[@id="sapwd_main_window_root_"]')
    tr_4 = tr_3.find_element_by_tag_name('tbody')
    tr_5 = tr_4.find_element_by_tag_name('tr')
    tr_6 = tr_5.find_element_by_tag_name('td')
    tr_7 = tr_6.find_element_by_tag_name('div')
    tr_8 = tr_7.find_element_by_tag_name('table')
    tr_9 = tr_8.find_element_by_tag_name('tbody')
    tr_10 = tr_9.find_element_by_xpath('//*[@id="WD11"]/tbody/tr[3]')
    tr_11 = tr_10.find_element_by_xpath('//*[@id="WD65"]')
    tr_12 = tr_11.find_element_by_xpath('//*[@id="WD66"]')
    tr_13 = tr_12.find_element_by_xpath('//*[@id="WD66-tbd"]')
    tr_14 = tr_13.find_element_by_xpath('//*[@id="WD66-tbd"]/tr')
    tr_15 = tr_14.find_element_by_xpath('//*[@id="WD66-tbd"]/tr/td')
    tr_16 = tr_15.find_element_by_xpath('//*[@id="WD68-r"]')
    tr_17 = tr_16.find_element_by_xpath('//*[@id="WD68"]')
    tr_18 = tr_17.find_element_by_xpath('//*[@id="WD68"]/tbody') #졸업사정 결과

    grad_table = tr_18.find_element_by_xpath('//*[@id="WD68"]/tbody/tr[2]')
    gt1 = grad_table.find_element_by_xpath('//*[@id="WD7B"]')
    gt2 = gt1.find_element_by_xpath('//*[@id="WD7C"]')
    gt3 = gt2.find_element_by_xpath('//*[@id="WD7C"]/tbody')
    gt4 = gt3.find_element_by_xpath('//*[@id="WD7C"]/tbody/tr')
    gt5 = gt4.find_element_by_xpath('//*[@id="WD7C-content"]')
    gt6 = gt5.find_element_by_xpath('//*[@id="WD7C-content"]/table')
    gt7 = gt6.find_element_by_xpath('//*[@id="WD7C-contentTBody"]') #표 접근

    graduate_table = []

    #졸업사정결과
    canGraduate_1 = tr_18.find_element_by_xpath('//*[@id="WD68"]/tbody/tr[1]')
    canGraduate_2 = canGraduate_1.find_element_by_xpath('//*[@id="WD6B"]')
    canGraduate_3 = canGraduate_2.find_element_by_xpath('//*[@id="WD6C"]')
    canGraduate_4 = canGraduate_3.find_element_by_xpath('//*[@id="WD70"]')
    canGraduate_5 = canGraduate_4.find_element_by_xpath('//*[@id="WD74"]')
    canGraduate_6 = canGraduate_5.find_element_by_xpath('//*[@id="WD75"]')
    canGraduate_7 = canGraduate_6.get_attribute('lsdata')
    canGraduate_8 = canGraduate_7.split("\'")
    canGraduate_f = False
    if canGraduate_8[1] == "불가능":
        canGraduate_f = False
    else:
        canGraduate_f = True
    graduate_table.append(canGraduate_f)

    #학부졸업학점133
    grad133_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[2]') #졸업요건 행 접근
    grad133_2 = grad133_1.find_element_by_xpath('//*[@id="WD9B"]')
    grad133_f = float(grad133_2.text)
    graduate_table.append(grad133_f)
    #print(grad133_f)

    #기독교과목4학점
    christ4_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[5]') #기독교학점 행 접근
    christ4_2 = christ4_1.find_element_by_xpath('//*[@id="WDBF"]')
    christ4_f = int(float(christ4_2.text))
    graduate_table.append(christ4_f)
    #print(christ4_f)

    #소프트공인증
    softeng60_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[6]') #소프트공
    softeng60_2 = softeng60_1.find_element_by_xpath('//*[@id="WDCB"]')
    softeng60_f = int(float(softeng60_2.text))
    graduate_table.append(softeng60_f)
    #print(softeng60_f)

    #소프트BSM공인증
    softbsm18_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[7]') #소프트공BSM
    softbsm18_2 = softbsm18_1.find_element_by_xpath('//*[@id="WDD7"]')
    softbsm18_f = int(float(softbsm18_2.text))
    graduate_table.append(softbsm18_f)
    #print(softbsm18_f)

    #전문교양소프트인증
    prosoft12_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[8]') #전문교양소프트인증
    prosoft12_2 = prosoft12_1.find_element_by_xpath('//*[@id="WDE3"]')
    prosoft12_f = int(float(prosoft12_2.text))
    graduate_table.append(prosoft12_f)
    #print(prosoft12_f)

    #설계소프트공인증
    archsoft12_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[9]')
    archsoft12_2 = archsoft12_1.find_element_by_xpath('//*[@id="WDEF"]')
    archsoft12_f = int(float(archsoft12_2.text))
    graduate_table.append(archsoft12_f)
    #print(archsoft12_f)

    #편입요이수지정과목
    pyeonip_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[3]')
    pyeonip_2 = pyeonip_1.find_element_by_xpath('//*[@id="WDAB"]')
    pyeonip_3 = pyeonip_2.text
    pyeonip_f = False
    if pyeonip_3 == "충족":
        pyeonip_f = True
    else :
        pyeonip_f = False
    graduate_table.append(pyeonip_f)
    #print(pyeonip_f)

    #졸업논문/졸업시험
    gradtest_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[4]')
    gradtest_2 = gradtest_1.find_element_by_xpath('//*[@id="WDB7"]')
    gradtest_3 = gradtest_2.text
    gradtest_f = False
    if gradtest_3 == "충족":
        gradtest_f = True
    else:
        gradtest_f = False
    graduate_table.append(gradtest_f)
    #print(gradtest_f)

    #기초과학
    elementsci_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[10]')
    elementsci_2 = elementsci_1.find_element_by_xpath('//*[@id="WDFF"]')
    elementsci_3 = elementsci_2.text
    elementsci_f = False
    if elementsci_3 == "충족":
        elementsci_f = True
    else:
        elementsci_f = False
    graduate_table.append(elementsci_f)
    #print(elementsci_f)

    #종합설계
    allarch_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[12]')
    allarch_2 = allarch_1.find_element_by_xpath('//*[@id="WD0117"]')
    allarch_3 = allarch_2.text
    allarch_f = False
    if allarch_3 == "충족":
        allarch_f = True
    else:
        allarch_f = False
    graduate_table.append(allarch_f)
    #print(allarch_f)

    #공학설계입문
    engarchelem_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[11]')
    engarchelem_2 = engarchelem_1.find_element_by_xpath('//*[@id="WD010B"]')
    engarchelem_3 = engarchelem_2.text
    engarchelem_f = False
    if engarchelem_3 == "충족":
        engarchelem_f = True
    else:
        engarchelem_f = False
    graduate_table.append(engarchelem_f)
    #print(engarchelem_f)

    #수학(소프트공학)
    matheng_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[13]')
    matheng_2 = matheng_1.find_element_by_xpath('//*[@id="WD0123"]')
    matheng_3 = matheng_2.text
    matheng_f = False
    if matheng_3 == "충족":
        matheng_f = True
    else:
        matheng_f = False
    graduate_table.append(matheng_f)
    #print(matheng_f)

    #졸업확정신고여부
    gradnotice_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[14]')
    gradnotice_2 = gradnotice_1.find_element_by_xpath('//*[@id="WD012F"]')
    gradnotice_3 = gradnotice_2.text
    gradnotice_f = False
    if gradnotice_3 == "충족" :
        gradnotice_f = True
    else:
        gradnotice_f = False
    graduate_table.append(gradnotice_f)
    #print(gradnotice_f)

    #교양필수
    libartess_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[15]')
    libartess_2 = libartess_1.find_element_by_xpath('//*[@id="WD0138"]')
    libartess_f = int(float(libartess_2.text))
    graduate_table.append(libartess_f)
    #print(libartess_f)

    #교양선택
    libartselect_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[16]')
    libartselect_2 = libartselect_1.find_element_by_xpath('//*[@id="WD0145"]')
    libartselect_f = int(float(libartselect_2.text))
    graduate_table.append(libartselect_f)
    #print(libartselect_f)

    #공동체,리더십
    leadership_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[17]')
    leadership_2 = leadership_1.find_element_by_xpath('//*[@id="WD0151"]')
    leadership_f = leadership_2.text

    if leadership_f == ' ':
        leadership_f = 0
    else:
        leadership_f = int(float(leadership_f))
    graduate_table.append(leadership_f)

    #의사소통글로벌
    comglobal_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[18]')
    comglobal_2 = comglobal_1.find_element_by_xpath('//*[@id="WD015D"]')
    comglobal_f = int(float(comglobal_2.text))
    graduate_table.append(comglobal_f)
    #print(comglobal_f)

    #전기소프트
    majorelemsoft_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[20]')
    majorelemsoft_2 = majorelemsoft_1.find_element_by_xpath('//*[@id="WD0176"]')
    majorelemsoft_f = int(float(majorelemsoft_2.text))
    graduate_table.append(majorelemsoft_f)
    #print(majorelemsoft_f)

    #전필소프트
    majoresssoft_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[21]')
    majoresssoft_2 = majoresssoft_1.find_element_by_xpath('//*[@id="WD0183"]')
    majoresssoft_f = int(float(majoresssoft_2.text))
    graduate_table.append(majoresssoft_f)
    #print(majoresssoft_f)

    #전공소프트
    majorsoft_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[22]')
    majorsoft_2 = majorsoft_1.find_element_by_xpath('//*[@id="WD018F"]')
    majorsoft_f = int(float(majorsoft_2.text))
    graduate_table.append(majorsoft_f)
    #print(majorsoft_f)

    #교선창의융합2개
    libertyart_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[19]')
    libertyart_2 = libertyart_1.find_element_by_xpath('//*[@id="WD016D"]')
    libertyart_3 = libertyart_2.text
    libertyart_f = False
    if libertyart_3 == "충족":
        libertyart_f = True
    else:
        libertyart_f = False
    graduate_table.append(libertyart_f)
    #print(libertyart_f)

    #채플
    chaple_1 = gt7.find_element_by_xpath('//*[@id="WD7C-contentTBody"]/tr[23]')
    chaple_2 = chaple_1.find_element_by_xpath('//*[@id="WD01A0"]')
    chaple_3 = chaple_2.text
    chaple_f = False
    if chaple_3 == "충족":
        chaple_f = True
    else:
        chaple_f = False
    graduate_table.append(chaple_f)
    #print(chaple_f)

    return graduate_table


def add_new_items(c1, c2, c3):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',"myapi.settings")
    import django
    django.setup()
    from crawling_backend.models import BoardData
    
    BoardData(
        #c1 첫 페이지에 구할 수 있는 정보들
        studentID = c1[0],
        studentGrade = c1[1],
        studentSemester = c1[2],
        studentEnrolled = c1[3],

        #c2 학기별 성적조회 페이지에서 구할 수 있는 정보들
        #listenList = c2[0], 
        #scoreList = c2[1],
        graduateScore = c2[2],

        #c3 졸업사정표 페이지에서 구할 수 있는 정보들
        canGraduate = c3[0],

        grad133_f = c3[1],

        christ4_f = c3[2],
        softeng60_f = c3[3],
        softbsm18_f = c3[4],
        prosoft12_f = c3[5],
        archsoft12_f = c3[6],

        pyeonip_f = c3[7],
        gradtest_f = c3[8],
        elementsci_f = c3[9],
        allarch_f = c3[10],
        engarchelem_f = c3[11],
        matheng_f = c3[12],
        gradnotice_f = c3[13],

        libartess_f = c3[14],
        libartselect_f = c3[15],
        leadership_f = c3[16],
        comglobal_f = c3[17],
        majorelemsoft_f = c3[18],
        majoresssoft_f = c3[19],
        majorsoft_f = c3[20],

        libertyart_f = c3[21],
        chaple = c3[22]
    ).save()
    print("추가 완료!")


def mainFunc(self):
    options = webdriver.ChromeOptions()

    try:
        driver = webdriver.Chrome('C:/testserver/crawling_backend/venv/chromedriver.exe', options=options)
        driver.set_window_size(1920, 1080)
    except:
        print("! 크롬 드라이버 로드 실패. 크롬 버전과 호환되는 크롬드라이버가 설치되어 있는지, chromedriver.exe가 폴더 내에 있는지 확인해주세요.")

    try:
        Login(self, driver, self.id, self.pw)
    except:
        print("! 로그인에 실패하였습니다")
        
    try:
        c1 = FirstPage(self, driver)
        c2 = GradeList(self, driver)
        c3 = CheckGrade(self, driver)
        add_new_items(c1, c2, c3)

    except Exception as e:
        print(f"! 성적 확인 도중 문제가 발생했습니다. {e}")


class Temp():
    def __init__(self):
        self.isRun = False
        self.id = "20201759"
        self.pw = "dlstod!26"
    def run(self):
        mainFunc(self)

tmp = Temp()
tmp.run()