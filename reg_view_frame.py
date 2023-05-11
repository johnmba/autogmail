
from random import choice, uniform, randrange
import time
import requests

import sqlite3
from customtkinter import CTkFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from fake_useragent import UserAgent

from export import Generator


class Regdata(CTkFrame):
    
    def __init__(self, master: any=None, datasheet=None,  **kwargs):
        self.display = datasheet
        self.default = True
        self.web = ""
        self.selet_xpath = (#LXRPh container class
            #"//*[@id='asset-view-details']"
            "//div[@class='LXRPh']"
            "[contains(text(),'{}')]"#VfPpkd-vQzf8d
        )
        self.next = ""
        self.url = "https://accounts.google.com/signup"
        user_agent = UserAgent()
        self.user_agents = user_agent.random
        self._con = sqlite3.connect("datahouse.db")
        self._cur = self._con.cursor()
        self._cur.execute("CREATE TABLE IF NOT EXISTS userAgents(id INTEGER PRIMARY KEY, user_agent TEXT UNIQUE)")
        self._cur.execute("CREATE TABLE IF NOT EXISTS ips(id INTEGER PRIMARY KEY, ip_addr TEXT UNIQUE)")
        self._con.commit()
        self._con.close()
        
        self.PROXIES = [
            'http://19.151.94.248:88', 'http://149.169.197.151:80', 'http://212.76.118.242:97'
        ]
        super().__init__(master, **kwargs)
        
    def setdriver(self):
        """
        scan and fetch availabe drivers on the system
        """
        
    def save_header(self):
        """
        check if header already exists 
        do not exists add record
        """
        
        sql = "insert into userAgents(user_agent) values(?,)"
        try:
            self._cur.executemany(sql, self.user_agents)
        except sqlite3.IntegrityError:
            self._con.close()
            for user_agent in self.user_agents:
                self._cur.execute(__sql=sql, __parameters=(user_agent))
            self._con.close()
        
    def header_db(self):
        """
        create data storage for I and user agents
        """
        
        url='https://headers.scrapeops.io/v1/browser-headers'
        params={
            'api_key': 'bc0676e7-e32f-4e8c-845b-e7365de4786a',
            'num_headers': '10'
        }
        
        if(user_agent := requests.get(url=url, params=params)) and user_agent.status_code == 200:
            agents = user_agent.json()
            self.user_agents = agents["result"]
        return choice(list(self.user_agents))
        
    def setagent(self):
        
        user_agent = self.user_agents
        
        if not self.default:
            profile = Options()
            profile.add_argument(f"user-agent={user_agent}")
        
        if self.default:
            profile = webdriver.FirefoxOptions()
            return profile.set_preference("general.useragent.override", user_agent)
            
        #return profile
    
    def bot(self, stop:bool=False):
        
        agent = self.setagent()
        
        if not self.default:
            self.web = webdriver.Chrome(agent)
        
        if self.default:
            webdriver.FirefoxOptions.proxy = choice(self.PROXIES)
            self.web = webdriver.Firefox(agent)
        if stop:
            self.web.close()
        self.header_db()
        
    def typeText(self, send_text, value, byname=By.ID):
        """
        Try selecting and on exception click next
        """
        
        success = False
        wait = WebDriverWait(self.web, 10)
        
        try:
            element = self.web.find_element(by=byname, value=value)
            
            while success == False:
                actions = ActionChains(self.web)
                actions.reset_actions()
                actions.click(on_element=element)
                actions.move_to_element(wait.until(EC.visibility_of_element_located((byname, value)))).perform()
                element.clear()
                #element.click()
                
                for character in send_text:
                    actions.send_keys(character).perform()
                    time.sleep(uniform(0.13, 0.4))

                if element.get_attribute("data-initial-value") == send_text:
                    success = True
        except NoSuchElementException:
            success = False
        finally:
            return success
        
    #day #class="whsOnd zHQkBf" jsname="YPqjbf"  id="day"
    #month #select class="UDCCJb" jsname="YPqjbf" id="month" 
    # year direct #name="year" value="" id="year" 
    #gender #class="UDCCJb" jsname="YPqjbf" id="gender"
    #choose mail #id="selectionc0" class="d3GVvd jGAaxb" jsname="CeL6Qc"
    #choose country <span jsname="K4r5Ff" class="VfPpkd-StrnGf-rymPhb-b9t22c">Nigeria (+234)</span>
    def selector(self):
        
        gender = False
        dob = False
        genders = ["Male", "Female"]
        months = [
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
        ]
        dropdown = lambda value: Select(self.web.find_element(value=value))
        
        try:
            if not gender:
                optns = dropdown(value="gender")
                optns.select_by_value(choice(genders))
                gender = True
            if not dob:
                self.typeText(send_text=range(1, 28), value="day")
                self.typeText(send_text=range(1960, 2005), value="day")
                optns = dropdown(value="month")
                optns.select_by_value(choice(months))
                dob = True
        except NoSuchElementException:
            try:
                self.typeText(send_text=range(1, 28), value="day")
                self.typeText(send_text=range(1960, 2005), value="day")
                optns = dropdown(value="month")
                optns.select_by_value(choice(months))
                dob = True
            except NoSuchElementException:
                optns = dropdown(value="gender")
                optns.select_by_value(choice(genders))
                gender = True
        finally:
            if gender and dob:
                return True
            return False
    
    def newuser(self, send_text):
        
        error_note = False
        wait =  WebDriverWait(self.web, 10)
        actions = ActionChains(self.web)
        sugestn_index = choice(range(1, 4))
        sugestn_frame = (By.XPATH, "//ul[@class='S9BUjf']/li")
        seletpath = f"""//ul[@class='S9BUjf']/li[{sugestn_index}]"""#/button[@class='TrZEUc' and @jsname='xqKM5b']
        tooshort = "Sorry, your username must be between 6 and 30 characters long."#o6cuMc Jj6Lae
        taken = "That username is taken. Try another."#o6cuMc Jj6Lae
        
        if self.typeText(send_text=send_text, value="username"):     
            uname = self.web.find_element(value="username")
            sugestn =  uname.get_attribute("data-initial-value")
            uname.send_keys(Keys.TAB)
            try:
                if actions.move_to_element(wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "o6cuMc")))):
                    error = self.web.find_element(by=By.CLASS_NAME, value="o6cuMc")
                if(
                    EC.text_to_be_present_in_element(locator=error, text_=taken) or 
                    EC.text_to_be_present_in_element(locator=error, text_=tooshort)
                ):
                    error_note = True
                    sugestn =  uname.get_attribute("data-initial-value")
                    if wait.until(EC.visibility_of_element_located(sugestn_frame)):
                        actions.reset_actions()
                        self.web.find_element(by=By.XPATH, value=seletpath).click()
                        sugestn =  uname.get_attribute("data-initial-value")
            except TimeoutException:
                if error_note:
                    random_number = str(randrange(1, 1000))
                    send_text = send_text + random_number
                    return self.newuser(send_text=send_text)
                return error_note
            except NoSuchElementException:
                return self.newuser(send_text=send_text)
            return sugestn
  
    def usaname(self, username):
        
        wait =  WebDriverWait(self.web, 10)
        actions = ActionChains(self.web)
        new_email = "Create a new Gmail address instead"
        
        try:
            actions.reset_actions()
            if success := self.newuser(send_text=username):
                return success
            if create_new := actions.move_to_element(
                wait.until(EC.visibility_of_element_located((By.XPATH, self.selet_xpath.format(new_email))))
            ):#expected condition
                create_new.perform().click()#data-username="jmba4037"
                self.newuser(send_text=username)
        except TimeoutException:      
            if self.selector():#expected condition
                self.next
                try:
                    actions.reset_actions()
                    if optn := self.web.find_element(value="selectionc0"):
                        sugestn = optn.get_attribute("data-initial-value")
                        optn.click()
                        return sugestn
                except NoSuchElementException:
                    pass
        return False
            
    def bot_reg(self, data):
        """
        craw the page and register user
        save to database
        life update of the the datasheet
        """
        
        self.web.get(self.url)
        btn_selector =  ("//span[@class='VfPpkd-vQzf8d']"
                         "[text()='Next']")#.format("Next")
        sugestn = False
        phone = "phoneNumberId"
        #o6cuMc Jj6Lae#username is taken
        self.next = self.web.find_element(By.XPATH, btn_selector)#class="VfPpkd-vQzf8d"
        name = data["fullname"].split(" ")
        
        if self.typeText(send_text=name[1], value="firstName") and self.typeText(send_text=name[0], value="lastName"):
            sugestn = self.usaname(username = data["username"])
        if(
            self.typeText(send_text=data["password"], byname=By.NAME, value="Passwd") and 
            self.typeText(send_text=data["password"], byname=By.NAME, value="ConfirmPasswd")
        ):#Password #aria-label="Confirm"
            self.next.click()
        return sugestn
        
    def isVissible(self, attr, by=By.ID, text_test=""):
        """
        if access denied close and restart the bot
        """
        try:
            selected = self.web.find_element(by=by, value=attr)
        except NoSuchElementException:
            return False
        
        if selected != "":
            return True
        elif selected.size() != 0:
            return True
        elif selected.contains(text_test):
            return True
        else:
            return False
    

if __name__ == "__main__":
    setup = Regdata()
    setup.bot()
    setup.bot_reg({"fullname": "john mba", "username": "johnba4567", "password": "napapaGod4me"})