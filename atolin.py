import os
from random import choice
from shutil import rmtree
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def main(proxy, useragent):
    proxy_id, port = proxy.split(':')
    print(i, proxy_id, port)
    os.system('rd /s /q "GoogleChromePortable\\Data\\profile\\profile"')
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server=http://{proxy_id}:{port}')
    options.binary_location = "GoogleChromePortable\\GoogleChromePortable.exe"
    options.add_argument(r'--user-data-dir=GoogleChromePortable\Data\profile')
    options.add_argument('--profile-directory=profile')
    options.add_argument('--process-per-site')
    options.add_argument(f'--user-agent="{useragent}"')
    driver = webdriver.Chrome(options=options)
    # driver.get('https://browserleaks.com/ip')
        
    def registration():
        try:
            driver.get('https://atolin.ru/')
        except WebDriverException:
            print('ERR_PROXY_CONNECTION_FAILED')
        try:
            driver.find_element_by_xpath('//a/img[@src="/themes/mobile/images/register.svg"]').click()
        except NoSuchElementException:
            driver.quit()
            return False
        WebDriverWait(driver, 10).until(ec.frame_to_be_available_and_switch_to_it(
            driver.find_element_by_xpath("//iframe[@class='fancybox-iframe']")))
        name = '//input[@id="data2registration-name"]'
        driver.find_element_by_xpath(name).send_keys(str(choice(open('names').readlines()).removesuffix('\n')))
        gender = '//label[@class="label_gender0"]'
        driver.find_element_by_xpath(gender).click()
        age = '//input[@id="data2registration-age"]'
        driver.find_element_by_xpath(age).send_keys(str(choice(range(18, 27))))
        heigth = '//input[@id="data2registration-heigth"]'
        driver.find_element_by_xpath(heigth).send_keys(str(choice(range(160, 180))))
        weight = '//input[@id="data2registration-weight"]'
        driver.find_element_by_xpath(weight).send_keys(str(choice(range(55, 70))))
        city = '//optgroup/option[text()="Москва"]'
        driver.find_element_by_xpath(city).click()
        submit_button = '//button[@class="blue-button btn btn-primary btn-sm"]'
        driver.find_element_by_xpath(submit_button).click()
        sleep(4)
    registration()
    driver.quit()


def create_bat(proxy, user_agent):
    proxy_id, port = proxy.split(':')
    bat = f'''\
rd /s /q "GoogleChromePortable\\Data\\profile\\profile"
"GoogleChromePortable\\GoogleChromePortable.exe" --profile-directory=profile \
--user-data-dir="GoogleChromePortable\\Data\\profile" --user-agent="{user_agent}" --process-per-site \
--proxy-server="http://{proxy_id}:{port}" https://atolin.ru/?rgcd=okdmw 
'''
    open(f'{str(i)}.cmd', 'w').write(bat)


if __name__ == '__main__':
    ports = [proxy.replace('\n', '') for proxy in open('ports.txt').readlines()]
    for i, proxy in enumerate(ports, 1):
        user_agent = str(choice(open('useragents.txt').readlines()).replace('\n', ''))
        # main(proxy, user_agent)
        create_bat(proxy, user_agent)
    print('completed')
