from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from config import LOGIN, PASS, HOST, SIGNIN_PAGE
from typing import List, Tuple
from random import randrange
import requests
import json

final_res = []

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def enter_input(_id: str, key: str, enter=False) -> None:
    _input = driver.find_element(By.ID, _id)
    _input.clear()
    _input.send_keys(key)
    sleep(randrange(3, 10))
    if enter:
        _input.send_keys(Keys.ENTER)
        sleep(10)


def sign_in(signin_page: str) -> None:
    driver.get(signin_page)
    sleep(randrange(3, 10))


def select_invisible() -> None:
    select = Select(driver.find_element(By.ID, 'online'))
    select.select_by_value('invisible')


def get_page(num: int) -> None:
    base_url = f"https://{HOST}/agent/agents?page="
    _page = base_url + str(num)
    driver.get(_page)
    sleep(randrange(3, 10))


def get_departments_list() -> List[str]:
    url = f"https://{HOST}/api/v2/departments"
    r = requests.get(url=url, headers={"Accept": "application/json"},
                     auth=(LOGIN, PASS))
    output = json.loads(r.text)
    output = [x['name'] for x in output]
    return output


def parse_department(cur_deps: List[str]) -> List[List[str]]:
    root1 = driver.find_element(By.TAG_NAME, 'af-root')
    shadow_root1 = root1.shadow_root
    elements = shadow_root1.find_elements(By.CLASS_NAME, "departments")
    list_of_deps = [h.text for h in elements]

    page_res = []
    for d in list_of_deps:
        agent_deps = []
        for dep in cur_deps:
            if d.__contains__(dep):
                agent_deps.append(dep)
        page_res.append(agent_deps)

    return page_res


def parse_name() -> List[str]:

    page_res = []
    _timeout = 10

    root1 = driver.find_element(By.TAG_NAME, 'af-root')
    shadow_root1 = root1.shadow_root
    elements = shadow_root1.find_elements(By.CSS_SELECTOR, "af-agent-card")

    for element in elements:
        shadow_root2 = element.shadow_root
        data = WebDriverWait(driver, _timeout).until(
            EC.visibility_of(shadow_root2.find_element(
                By.CSS_SELECTOR, ".name"))).text
        page_res.append(data)

    return page_res


def iterate_pages(_final_res: List[Tuple]) -> None:

    current_deps = get_departments_list()
    previous_url = ''
    i = 1
    get_page(i)

    while driver.current_url != previous_url:
        res_name = parse_name()
        res_deps = parse_department(current_deps)
        _final_res.extend([(n, d) for n, d in zip(res_name, res_deps)])
        previous_url = driver.current_url
        i += 1
        get_page(i)


if __name__ == '__main__':

    sign_in(SIGNIN_PAGE)
    select_invisible()
    enter_input('login_or_email', LOGIN)
    enter_input('password', PASS, enter=True)
    iterate_pages(final_res)
