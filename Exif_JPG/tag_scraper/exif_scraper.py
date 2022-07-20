from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://exiv2.org/tags.html'
browser = webdriver.Chrome()
browser.get(url)
rows = len(browser.find_elements(by = By.XPATH,value="/html/body/div[1]/table/tbody/tr")) + 1
column = len(browser.find_elements(by = By.XPATH,value="/html/body/div[1]/table/tbody/tr/td"))

print(rows)
print(column)
with open('test.txt','w') as file:
    for x in range(1,rows):
        file.write(browser.find_element(by = By.XPATH,value='/html/body/div[1]/table/tbody/tr[' + str(x) + ']/td[2]').get_attribute('outerText') + '    ')
        file.write(browser.find_element(by = By.XPATH,value='/html/body/div[1]/table/tbody/tr[' + str(x) + ']/td[4]').get_attribute('outerText') + '    ')
        file.write(browser.find_element(by = By.XPATH,value='/html/body/div[1]/table/tbody/tr[' + str(x) + ']/td[6]').get_attribute('outerText') + '\n')
