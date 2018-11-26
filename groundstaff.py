import logging

import click

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from config import get_url


class ReservationUnavailable(BaseException):
    pass


class MissingInput(BaseException):
    pass


def getWebDriver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(chrome_options=opts)


def step1_login_reserve(driver,
                        username, password,
                        date, hour_from, hour_to,
                        is_indoor):

    url = get_url(date, hour_from, hour_to, is_indoor)
    driver.get(url)

    try:
        input_member_code = driver.find_element_by_id(
            'input_reserver_code'
        )
        input_password = driver.find_element_by_id(
            'input_reserver_password'
        )
        input_submit = driver.find_element_by_css_selector(
            "input[type='submit']"
        )
    except NoSuchElementException:
        # NOTE: ASSUMPTION specified time is unavailable
        # of course, this could be the case of form HTML changed
        logging.exception(
            ('step1: unable to locate username and password inputs: '
             f'{date}-{hour_from}-{hour_to}')
        )
        raise ReservationUnavailable()
    else:
        input_member_code.send_keys(username)
        input_password.send_keys(password)
        input_submit.click()


def step2_confirm(driver, mobile_phone_number, make_reservation):
    try:
        input_mobile_no = driver.find_element_by_id(
            'input_reserver_tel_mobile'
        )
        input_next = driver.find_element_by_css_selector(
            "input[type='submit']"
        )
    except NoSuchElementException:
        logging.exception(
            ('step2: unable to locate mobile tel input or next button: '
             f'{mobile_phone_number}')
        )
        raise ReservationUnavailable()
    else:
        input_mobile_no.send_keys(mobile_phone_number)
        input_next.click()

    try:
        input_confirm = driver.find_element_by_css_selector(
            "input[name='submit_ok']"
        )
    except NoSuchElementException:
        logging.exception(
            ('step2: : unable to locate confirmation button: '
             f'{mobile_phone_number}')
        )
        raise ReservationUnavailable()
    else:
        if make_reservation:
            input_confirm.click()


@click.command()
@click.option('--username', help='username')
@click.option('--password', help='password')
@click.option('--date', help='date in YYYY-MM-DD')
@click.option('--timerange', help='for instance, 1800-2000')
@click.option('--tel', help='mobile tel number to reserve in')
@click.option('--indoor/--outdoor', default=False,
              help='set --indoor or --outdoor; defaults to outdoor')
@click.option('--dryrun', is_flag=True,
              help='use --dryrun if you do not want to make reservation')
def main(username, password, date, timerange, tel, indoor, dryrun):
    driver = getWebDriver()
    make_reservation = not dryrun

    try:
        hour_from, hour_to = timerange.split('-')
        # TODO: validation on date & timerange

        step1_login_reserve(
            driver, username, password, date, hour_from, hour_to, indoor
        )

        if not tel:
            raise MissingInput('tel number is required for confirmation')

        step2_confirm(driver, tel, make_reservation)

    finally:
        driver.close()


if __name__ == '__main__':
    main()
