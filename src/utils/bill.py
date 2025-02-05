import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


def click(driver: webdriver, xpath: str):
    driver.find_element(By.XPATH, xpath).click()


def send_keys(driver, xpath: str, text: str):
    enter_phone = driver.find_element(By.XPATH, xpath)
    enter_phone.send_keys(text)


def get_text(driver, xpath: str):
    return driver.find_element(By.XPATH, xpath).text


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    options.add_argument("--headless")
    # options.add_argument("user-data-dir=selenium1618")
    options.add_argument("--incognito")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36",
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=False,
        run_on_insecure_origins=False,
    )
    return driver


def get_receipt(driver: webdriver, string_from_qr: str):
    x = "/html/body/div[1]/div[2]/div[1]/div[4]/div[2]/ul/li[4]/a"
    click(xpath=x, driver=driver)
    x = "/html/body/div[1]/div[2]/div[1]/div[4]/div[2]/div[1]/div[3]/div/div/div/form/div[1]/div/textarea"
    click(xpath=x, driver=driver)
    send_keys(
        xpath=x,
        driver=driver,
        text=string_from_qr,
    )
    x = "/html/body/div[1]/div[2]/div[1]/div[4]/div[2]/div[1]/div[3]/div/div/div/form/div[2]/div/button"
    click(xpath=x, driver=driver)
    receipt = driver.find_elements(By.CLASS_NAME, "b-check_item")
    return receipt


def receipt_to_dict(driver: webdriver, receipt):
    data = {}
    _items = []
    name_keys = ["n", "name", "price", "count", "sum"]
    for item in receipt:
        splitted_item = item.find_elements(By.TAG_NAME, "td")
        _item = {}
        for i, name_key in zip(splitted_item, name_keys):
            new_i = None
            if name_key == "n":
                continue
            if name_key in ["price", "sum"]:
                new_i = round(float(i.text), 2)
            if name_key == "count":
                new_i = float(i.text)
            _item[name_key] = i.text if not new_i else new_i
        _items.append(_item)
    data["items"] = _items
    return data


class StringQr:
    @staticmethod
    def get_format_time(string_from_qr: str):
        r = string_from_qr.split("&")[0]
        r = r.split("=")[1]
        date, time = r.split("T")
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        hour = time[0:2]
        minute = time[2:4]
        s = f"{day}.{month}.{year} {hour}:{minute}"
        return datetime.datetime.strptime(s, "%d.%m.%Y %H:%M")

    @staticmethod
    def get_fp_fn_fd(string_from_qr: str):
        r = string_from_qr.split("&")
        fp = r[3].split("=")[1]
        fn = r[2].split("=")[1]
        fd = r[4].split("=")[1]
        return fp, fn, fd

    @staticmethod
    def get_sum(string_from_qr: str):
        r = string_from_qr.split("&")
        s = r[1].split("=")[1]
        return round(float(s), 2)


def get_dict_products(string_from_qr: str):
    url = "https://proverkacheka.com/?hl=ru_RU"
    driver = init_driver()
    driver.get(url)
    driver.implicitly_wait(5)
    receipt = get_receipt(
        driver,
        string_from_qr=string_from_qr,
    )
    return receipt_to_dict(driver, receipt)
