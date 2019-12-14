from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dt
from datetime import timedelta
import pause
import time

def BookCourt(daysInForward, startHour, emailAddress, password, cvv):
    # hard coded numbers
    startTryHour=6
    startTryMin=59
    startTrySecond=45

    browser = webdriver.Chrome('/Users/Tony/Desktop/mcfet/chromedriver')
    browser.get(('https://apm.activecommunities.com/chicagoparkdistrict/ActiveNet_Home?FileName=onlinequickfacilityreserve.sdi'))

    emailBox = browser.find_element_by_id('ctl05_ctlLoginLayout_txtUserName')
    pwdBox = browser.find_element_by_id('ctl05_ctlLoginLayout_txtPassword')
    loginButton = browser.find_elements_by_id('ctl05_ctlLoginLayout_btnLogin')

    while len(loginButton)>0:
        time.sleep(1)
        emailBox = browser.find_element_by_id('ctl05_ctlLoginLayout_txtUserName')
        pwdBox = browser.find_element_by_id('ctl05_ctlLoginLayout_txtPassword')
        emailBox.clear()
        emailBox.send_keys(emailAddress)
        pwdBox.send_keys(password)
        loginButton[0].click()

        loginButton = browser.find_elements_by_id('ctl05_ctlLoginLayout_btnLogin')

    dayDropDown = Select(browser.find_element_by_id('begd'))

    today=dt.today()
    date=today+timedelta(days=daysInForward)
    if date.month!=today.month:
        monthDropDown = Select(browser.find_element_by_id('begm'))
        monthDropDown.select_by_value(str(date.month-1))
        yearDropDown = Select(browser.find_element_by_id('begy'))
        yearDropDown.select_by_value(str(date.year))

    dayDropDown = Select(browser.find_element_by_id('begd'))
    dayDropDown.select_by_value(str(date.day))


    facilityDropDown= Select(browser.find_element_by_id('facilitygroup_id'))
    facilityDropDown.select_by_index(2)

    courtNo = 1
    foundCourt = False
    while courtNo <= 6 and (not foundCourt):
        firstHour=browser.find_elements_by_xpath('//*[@title="McFetridge Tennis Court 0%s : %spm"]' % (courtNo,startHour))
        secondHour=browser.find_elements_by_xpath('//*[@title="McFetridge Tennis Court 0%s : %spm"]' % (courtNo,startHour+1))

        if len(firstHour)==1 and len(secondHour)==1:
            firstHour[0].click()
            secondHour[0].click()
            nameIndex = (str(firstHour[0].get_attribute('name')).split('.'))[0]
            attendBox = browser.find_element_by_name('event_attendance_%s' %(nameIndex))
            attendBox.send_keys('2')

            foundCourt = True
            print('FOUND COURT NO.%s FROM %sPM TO %sPM' %(courtNo,startHour,startHour+2))

        elif len(firstHour)==1 and len(secondHour)==0:
            firstHour[0].click()
            nameIndex = (str(firstHour[0].get_attribute('name')).split('.'))[0]
            attendBox = browser.find_element_by_name('event_attendance_%s' %(nameIndex))
            attendBox.send_keys('2')

            print('FOUND COURT NO.%s FROM %sPM TO %sPM' %(courtNo,startHour,startHour+1))

            secondCourtNo = 1
            foundsecondCourt = False
            while secondCourtNo <= 6 and (not foundCourt):
                secondHour=browser.find_elements_by_xpath('//*[@title="McFetridge Tennis Court 0%s : %spm"]' % (secondCourtNo,startHour+1))
                if len(secondHour)==1:
                    secondHour[0].click()
                    nameIndex = (str(secondHour[0].get_attribute('name')).split('.'))[0]
                    attendBox = browser.find_element_by_name('event_attendance_%s' %(nameIndex))
                    attendBox.send_keys('2')

                    foundCourt = True
                    print('FOUND COURT NO.%s FROM %sPM TO %sPM' %(secondCourtNo,startHour+1,startHour+2))
                
                secondCourtNo+=1
    
        courtNo+=1

    if foundCourt:
        pause.until(dt(today.year,today.month,today.day,startTryHour,startTryMin,startTrySecond))
        browser.find_element_by_xpath('//*[@title="Reserve Now"]').click()

        while len(browser.find_elements_by_xpath('//*[@title="Reserve Now"]'))>0:
            browser.find_element_by_xpath('//*[@title="Reserve Now"]').click()
        browser.find_element_by_name('thirteen').click()

        browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
        cvvBox = browser.find_element_by_id("cvv")
        cvvBox.send_keys(cvv)
        browser.switch_to.default_content()

        browser.find_element_by_name('Continue').click()

        time.sleep(10)
        if len(browser.find_elements_by_name('Continue'))>0:
            print("PAYMENT FAILED, CHECK CVV")
            return False


    else:
        print("NO LUCK TODAY...")
        time.sleep(10)
        return False

    print('BOOKED COURT NO.%s FROM %sPM' %(courtNo,startHour))
    time.sleep(10)
    return True