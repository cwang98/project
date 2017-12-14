import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, sys

class SimulateWebOperation():
    driver = webdriver.Chrome("/Users/ssui9307/Desktop/chromedriver")
    
    def go_to_a_website(self, url):
        self.driver.get(url)
        time.sleep(6)

    def close_browser(self):
        self.driver.quit()
        
    def submit_click(self, webXpath, wait=1):
        tp = self.driver.find_element_by_xpath(webXpath)
        tp.click()
        print('click')
        time.sleep(wait)
       
    def select_dropdown_option(self, webXpath, option_text, wait=1):
            """ Selects the option in the drop-down
            required params:
            @XPAH == XPATH location of dropdown menu
            @option_text == the text of the option """
            dropdown = self.driver.find_element_by_xpath(webXpath)
            for option in dropdown.find_elements_by_tag_name('option'):
                if option.text == option_text:
                    option.click()
                    time.sleep(wait)
                    break
                
    def get_child_elements_number(self, webXpath, wait =1):

        childCount = len(self.driver.find_elements_by_xpath(webXpath))
        time.sleep(wait)
        return childCount

    def get_content_in_element(self, webXpath, wait =1):

        return self.driver.find_element_by_xpath(webXpath).text



if __name__=='__main__':

    
    writeinTxtFile = open("/Users/ssui9307/Desktop/haha.txt", 'a')
    
    url_nba='https://stats.nba.com/team/1610612744/boxscores-traditional/?Season=2016-17&SeasonType=Regular%20Season'
    #selectAllXpath = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select'   #在网页中通过inspect然后右键选择xpath找到下拉菜单的xpath
    selectAllXpath = '/html/body/main/div[2]/div/div/div[3]/div/nav-dropdown/nav/section[1]/ul/li'
	
    teamSelectXpath = '/html/body/main/div[2]/div/div/div[3]/div/nav-dropdown/nav/section[1]/div/div/a'
    dropdownAllXpath = '/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[1]/div/div/select'
    selectText = 'All'
    gameList_totaltbodyXpath = '/html/body/main/div[2]/div/div/div[3]/div/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr'


    nbaWebStats=SimulateWebOperation()
    nbaWebStats.go_to_a_website(url_nba)
    gameCount = nbaWebStats.get_child_elements_number(gameList_totaltbodyXpath, 0)
    print(gameCount)
    # statsColCount4EachGame = nbaWebStats.get_child_elements_number(gameList_totaltdXpath, 0)
    #nbaWebStats.select_dropdown_option(selectAllXpath,selectText,3)  #找到下拉菜单并选择一次显示全部
    
	
	
    teamCount = nbaWebStats.get_child_elements_number(selectAllXpath , 0)#通过上面每个tr的xpath找出一共有多少个球员
    i=0
    teamXpath = selectAllXpath + '[' + str(i + 1) + ']'+ '/a'
    print(teamXpath)
    nbaWebStats.submit_click(teamSelectXpath,0)




    i = 0
    while i < teamCount:
        teamXpath = selectAllXpath + '[' + str(i + 1) + ']'+ '/a'
        nbaWebStats.submit_click(teamXpath,1)

        # 在这输入你想进行的操作，例如选择数据等
        nbaWebStats.submit_click(teamSelectXpath,0)
        nbaWebStats.select_dropdown_option(dropdownAllXpath, selectText, 3)

        i += 1

        j = 0
        while j < 82:
            teamList_totaltdXpath = gameList_totaltbodyXpath + '[' + str(i + 1) + ']' + '/td'
            statsColCount4EachTeam = nbaWebStats.get_child_elements_number(teamList_totaltdXpath,
                                                                   0)  # 在当前球员的xpath下，在对他有多少项统计数据进行计数

            n = 0
            while n < statsColCount4EachTeam:
                teamList_eachtdXpath = teamList_totaltdXpath + '[' + str(n + 1) + ']'  # 在当前球员的xpath下，他的某一个数据的xpath路径
                data = nbaWebStats.get_content_in_element(teamList_eachtdXpath, 0)
                writeinTxtFile.write(data + '\t')
                n += 1
                print('Number ' + '(' + str(j + 1) + '/' + str(teamCount) + ')' + ' team data is being written into file. (' + str(n) + '/' + str(statsColCount4EachTeam) + ')')
            writeinTxtFile.write('\n')
        j += 1



    writeinTxtFile.close()

    nbaWebStats.close_browser()
    
    
