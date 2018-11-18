import logging

import click
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from config import get_url


def getWebDriver():
    opts = webdriver.ChromeOptions()
    # opts.add_argument('--headless')
    return webdriver.Chrome(chrome_options=opts)

# FIXME: temporarily set as global object 
driver = None

def step1_login_reserve(
    username, password,
    date, hour_from, hour_to, is_indoor):

    url = get_url(date, hour_from, hour_to, is_indoor)
    driver.get(url)

    try:
        input_member_code = driver.find_element_by_id('input_reserver_code')
        input_password = driver.find_element_by_id('input_reserver_password')
        input_submit = driver.find_element_by_css_selector("input[type='submit']")
    except NoSuchElementException as e:
        # NOTE: ASSUMPTION specified time is unavailable
        # of course, this could be the case of form HTML changed
        logging.exception(
            f'step1: specified time for reservation unavailable: {date}-{hour_from}-{hour_to}'
        )
        return
    else:
        input_member_code.send_keys(username)
        input_password.send_keys(password)
        input_submit.click()

def step2_confirm(mobile_phone_number):
    try:
        input_mobile_no = driver.find_element_by_id('input_reserver_tel_mobile')
        input_submit = driver.find_element_by_css_selector("input[type='submit' name='submit_conf']")
    except NoSuchElementException:
        logging.exception(
            f'step2: specified time for reservation unavailable: {mobile_phone_number}'
        )
        return
    else:
        input_mobile_no.send_keys(mobile_phone_number)
        input_submit.click()   


@click.command()
@click.option('--username', help='username')
@click.option('--password', help='password')
@click.option('--date', help='date in YYYY-MM-DD')
@click.option('--timerange', help='for instance, 1800-2000')
@click.option('--tel', help='mobile tel number to reserve in')
@click.option('--indoor/--outdoor', default=False, help='set this if booking indoor court; defaults to outdoor court')
def main(username, password, date, timerange, tel, indoor):
    try:
        hour_from, hour_to = timerange.split('-')
        # TODO: validation on date & timerange

        driver = getWebDriver()

        step1_login_reserve(username, password, date, hour_from, hour_to, indoor)
        step2_confirm(mobile_phone_number)
    finally:
        driver.close()
    


if __name__ == '__main__':
    main()
