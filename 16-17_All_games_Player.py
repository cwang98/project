import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, sys


class SimulateWebOperation():
    path = "/Users/ssui9307/Desktop/chromedriver"
    driver = webdriver.Chrome("/Users/ssui9307/Desktop/chromedriver")

    def go_to_a_website(self, url):
        self.driver.get(url)
        time.sleep(6)

    def close_browser(self):
        self.driver.quit()

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

    def multiselect_set_selections(driver, element_id, labels):
        el = driver.find_element_by_id(element_id)
        for option in el.find_elements_by_tag_name('option'):
            if option.text in labels:
                option.click()

    def get_child_elements_number(self, webXpath, wait=1):

        childCount = len(self.driver.find_elements_by_xpath(webXpath))
        time.sleep(wait)
        return childCount

    def get_content_in_element(self, webXpath, wait=1):

        return self.driver.find_element_by_xpath(webXpath).text


if __name__ == '__main__':

    writeinTxtFile = open("/Users/ssui9307/Desktop/1617-AllGames-Reg-Advanced-Players.txt", 'a')

    url_nba = 'https://stats.nba.com/players/boxscores-traditional/?Season=2016-17&SeasonType=Regular%20Season'
    selectAllXpath = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select'

    selectText = 'All'
    selectPage = ['1','2']
    playerList_totaltbodyXpath = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr'



    nbaWebStats = SimulateWebOperation()
    nbaWebStats.go_to_a_website(url_nba)
    nbaWebStats.select_dropdown_option(selectAllXpath, selectPage, 5)

    gameCount = nbaWebStats.get_child_elements_number(playerList_totaltbodyXpath, 0)
    print(gameCount)

    i = 0
    while i < gameCount:
        playerList_totaltdXpath = playerList_totaltbodyXpath + '[' + str(i + 1) + ']' + '/td'
        statsColCount4EachPlayer = nbaWebStats.get_child_elements_number(playerList_totaltdXpath,
                                                                         0)
        n = 0
        while n < statsColCount4EachPlayer:
            playerList_eachtdXpath = playerList_totaltdXpath + '[' + str(n + 1) + ']'
            data = nbaWebStats.get_content_in_element(playerList_eachtdXpath, 0)
            writeinTxtFile.write(data + '\t')
            n += 1
            print('Number ' + '(' + str(i + 1) + '/' + str(gameCount) + ')' + ' game data is being written into file. (' + str(n) + '/' + str(
                statsColCount4EachPlayer) + ')')
        writeinTxtFile.write('\n')
        i += 1

    writeinTxtFile.close()
    nbaWebStats.close_browser()