
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


class eduserve:

    def __init__(self, login_id, password) -> None:
        self.User_Name = login_id
        self.Password = password
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def login(self):
        self.driver.get('https://eduserve.karunya.edu/Login.aspx')
        self.driver.find_element(By.ID, "mainContent_Login1_UserName").send_keys(self.User_Name)
        self.driver.find_element(By.ID, 'mainContent_Login1_Password').send_keys(self.Password)
        self.driver.find_element(By.ID, 'mainContent_Login1_LoginButton').click()
        time.sleep(1)
        if(self.driver.title == "Hourly Feedback"):
            try:
                for i in range(1,10):
                    self.driver.find_element(By.XPATH,  f'/html/body/form/div[3]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/table/tbody/tr[{i}]/td[5]/div/ul/li[4]').click()
            except:
                self.driver.find_element(By.ID, "mainContent_btnSave").click()

    def getTimeTable(self):
        self.driver.find_element(By.XPATH,'//*[@id="ctl00_radMenuModule"]/ul/li[2]/a/span').click()
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, '//*[@id="ctl00_radMenuModule"]/ul/li[2]/div/ul/li[11]/a/span').click()
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, '//*[@id="ctl00_radMenuModule"]/ul/li[2]/div/ul/li[11]/div/ul/li[15]/a/span').click()
        Select(self.driver.find_element(By.ID, 'mainContent_DDLACADEMICTERM')).select_by_value('22')

        f = open('Time_Table.txt','w')
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_grdData_ctl00"]/thead/tr/th[1]')))
        lis = []
        for j in range(0, 5):
            for i in range(3, 11):
                if i != 8 or i != 3:
                    ele = self.driver.find_element(By.XPATH, f'//*[@id="ctl00_mainContent_grdData_ctl00__{j}"]/td[{i}]')
                    if ele.text[-3:][0] != 'b':
                        lis.append(ele.text[9:-3]+ele.text[-3:]+'|'.strip())
                    else:
                        lis.append(ele.text[9:-5]+ele.text[-5:-2]+'_'+ele.text[-1]+"|".strip())
            try:    
                for _ in range(2):
                    lis.remove(' |')   
            except:
                pass
            finally:
                f.write("".join(lis))
            f.write("\n")
            lis=[]
        f.close()
        
    def backHome(self):
        self.driver.find_element(By.XPATH, '//*[@id="ImageButton1"]').click()

    def exit(self):
        self.driver.close()

