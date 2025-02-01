# 此文件有关 selenium、cookie、check、User
import json
import time
from typing import Union
from datetime import datetime
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gogym.config import *
from gogym.control import rewrite_print, manage_file
from gogym.underlying import get_date_next_week, date_to_weekday, is_cookie_not_expired, is_date_valid, get_date_now


class User:
    # 因为地下的go函数需要用User，User要用初始化driver
    # 为了避免循环引用只能把user放到这个文件
    def __init__(self, initial: str, name: str, account: str, password: str, phone: str, slot_preference: list):
        """
        初始化一个 User 实例
        :param initial: "hxt"
        :param name: "黄啸天"
        :param account: "36920251111111"
        :param password: "HXT123456"
        :param phone: "13871111111"
        :param slot_preference: [5, 6, 7, 1, 2, 3, 4]
        """
        self.initial = initial
        self.name = name
        self.account = account
        self.password = password
        self.phone = phone
        self.slot_preference = slot_preference
        self.path = PATH_USER / f"{initial}.json"

    @classmethod
    def save(cls, initial: str, name: str, account: str, password: str, phone: str, slot_preference: list):
        """
        这个类函数会直接将一下的参数保存到users目录下
        :param initial: "hxt"
        :param name: "黄啸天"
        :param account: "36920251111111"
        :param password: "HXT123456"
        :param phone: "13871111111"
        :param slot_preference: [5, 6, 7, 1, 2, 3, 4]
        """

        # 制作用户数据字典
        user_data = {"initial": initial, "name": name, "account": account, "password": password, "phone": phone, "slot_preference": slot_preference}

        # 检查该用户是否已经存在
        json_path = PATH_USER / f"{initial}.json"
        if json_path.exists():
            print(f"{initial}: 此用户已经存在，请查看users文件夹。")
            return False

        # 检查用户密码是否正确
        if not is_match(account, password):
            print(f"{initial}: 用户账号和密码不匹配，请仔细检查。")
            return False

        # 保存
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)

        # 保存成功提示
        print(f"{initial}: 新用户创建成功。")
        return True

    @classmethod
    def load(cls, initial):
        """
        这个类函数会根据首字母返回一个user实例。
        :param initial: "hxt"
        :return: a User instance
        """

        # 检查文件夹是否存在，不存在返回False
        json_path = PATH_USER / f"{initial}.json"
        if not json_path.exists():
            raise FileNotFoundError(f"用户文件 '{json_path}' 不存在。")

        # 若有次文件夹，则打开文件，读取内容到user_data
        with open(json_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        # 返回一个实例
        return cls(
            initial=user_data["initial"],
            name=user_data["name"],
            account=user_data["account"],
            password=user_data["password"],
            phone=user_data["phone"],
            slot_preference=user_data["slot_preference"],
        )

    @classmethod
    def get_info(cls):
        """
        这个函数会读取所有的用户的信息，返回一个info的ndarray。
        注意：在有三个用户的情况下这一步会花费0.001秒，足以见得io操作在现实尺度几乎可忽略操作时间。
        :return: numpy ndarray
        """

        # 创建一个待返回的空列表
        info = []

        # 使用 Path.glob() 查找所有以 .json 结尾的文件
        for file_path in PATH_USER.glob("*.json"):
            # 打开并读取 JSON 文件
            with file_path.open("r", encoding="utf-8") as f:
                user_data = json.load(f)

            # 每个用户对应一行
            row = [user_data["initial"], user_data["name"], user_data["account"], user_data["password"], user_data["phone"], user_data["slot_preference"]]

            # 将此用户的所有信息添加到info列表中
            info.append(row)

        return info


def initiate_driver(url: str, user_cookie: Union[str, bool] = False, admin_cookie: bool = False, headless=HEADLESS) -> webdriver.Chrome:
    """
    此函数会根据 url 初始化一个 driver 实例。\n
    此函数可以选择是否使用 admin_cookie 与 user_cookie。\n
    :param url: 待访问的网址
    :param user_cookie: 需要则填 user:str，不需要则填 False
    :param admin_cookie: 是否是外网环境
    :param headless: 无头模式
    :return: driver instance
    """
    """
    1. 匿名访问（不带饼干）：driver = initiate_driver(url:str)
    2. 保存管理员饼干（不带饼干）：driver = initiate_driver(URL_IDCALLBACK_INTERNET)
    3. 保存用户饼干（带管理员饼干）：driver = initiate_driver(URL_IDCALLBACK_INTRANET, admin_cookie=IS_INTERNET)
    4. 访问预约界面（带两个饼干）：driver = initiate_driver(url=url, user_cookie=user, admin_cookie=IS_INTERNET)
    4. 查询用户预约信息（带两个饼干）：driver = initiate_driver(URL_MY_RESERVATION, user_cookie=each_user, admin_cookie=IS_INTERNET, headless=HEADLESS)
    """
    # 创建一个option实例，如果选择无头模式则不显示 chrome 浏览器。
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    # 启动浏览器，并通过 DevTools 协议启用 Network
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Network.enable", {})

    # 如果需要 user_cookie 则添加 user_cookie
    if user_cookie:
        driver.execute_cdp_cmd(cmd="Network.setCookie", cmd_args=load_user_cookie(user=user_cookie))

    # 如果需要 admin_cookie 则添加 admin_cookie
    if admin_cookie:
        driver.execute_cdp_cmd(cmd="Network.setCookie", cmd_args=load_admin_cookie())

    # 带着 cookie 直接访问 url
    driver.get(url)

    return driver


def driver_submit(driver, user):
    """
    这个函数用于在填写电话号码点击确认的那个页面。
    在那个页面填写电话号码，点击提交。
    :param driver: driver
    :param user: user
    :return: True
    """

    # 等待页面响应
    wait_until(driver, By.ID, "page-title")

    # 填写电话号码
    phone = User.load(user).phone
    blank_phone = driver.find_element(By.ID, "edit-field-tel-und-0-value")
    blank_phone.send_keys(phone)

    # 定位“提交”元素，并点击
    button_submit = driver.find_element(By.ID, "edit-submit")
    button_submit.click()
    # print("顺利：已填写电话号码并提交。")

    # 等待页面跳转到“健身房预约”界面
    wait_until(driver, By.ID, "page-title")
    # print("顺利：已成功跳转回“健身房预约”界面。")

    # 等待浅绿色的消息框加载出来
    wait_until(driver, By.CSS_SELECTOR, "div.alert.alert-block")

    # 打印浅绿色消息框里面的内容
    box = driver.find_element(By.CSS_SELECTOR, "div.alert.alert-block")
    phrase = box.text.split("\n")[-1]
    # print(f"顺利：系统提示：{phrase}。")

    return True


def is_match(account: str, password: str):
    """
    这个函数会验证新添的账户和密码是否匹配。
    :param account: 学好/工号
    :param password: 密码
    :return: bool
    """

    def wait_which_one(driver, timeout=60, interval=0.5):
        """
        这个函数会每隔一定时间查询当前页面，是不是目标页面A或者目标页面B
        然后返回A或者B
        :param interval: 没隔多少秒查询一次
        :param timeout: 一共查询多少秒
        :param driver:
        :return: -1 or 1
        """
        # 初始化查询次数，得到最大查询次数
        count = 0
        max_count = int(timeout / interval)

        # 查询大循环
        while True:
            # 如果能找到“场地预约”则账号密码匹配，返回 1
            try:
                driver.find_element(By.ID, "page-title")
                return 1
            except NoSuchElementException:
                pass

            # 如果能找到“页面错误”的字样则，返回-1
            try:
                driver.find_element(By.ID, "showErrorTip")
                return -1
            except NoSuchElementException:
                pass

            # 计数器更新，并且等待。
            count += 1
            time.sleep(interval)

            if count >= max_count:
                raise NoSuchElementException("页面没跳转，或者跳转了我不知道，请debug")

    # 创建driver实例
    driver = initiate_driver(URL_IDCALLBACK_INTRANET, admin_cookie=IS_INTERNET)

    # 等待页面返回（“统一身份认证”出现）
    wait_until(driver, By.CSS_SELECTOR, "p.login-title")

    # 填写账号
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(account)

    # 填写密码
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    # 点击登陆
    login_button = driver.find_element(By.ID, "login_submit")
    login_button.click()

    # 根据不同的页面判断密码正不正确
    flag = wait_which_one(driver)

    if flag == 1:
        return True
    elif flag == -1:
        return False
    else:
        raise ValueError("返回的什么玩意儿？？？")


def preopen_browser():
    """
    这个步骤会打开浏览器再关闭。
    相当于一个热身环节，以免在12点要打开浏览器的时候打开太慢。
    :return: True
    """
    # 打开浏览器再关掉
    driver = webdriver.Chrome()
    driver.quit()

    # print("顺利：初始化浏览器成功。")
    return True


def get_all_reservation_info(driver):

    # 等待“健身房预约”五个字出现
    wait_until(driver, By.ID, "page-title")

    # 获取所有的预约信息元素
    try:
        info = driver.find_elements(By.CSS_SELECTOR, ".table-responsive > .table > tbody > tr")
    except NoSuchElementException as e:
        info = []
        print("当前用户近一个月来没有预约记录。")

    # 把每个元素的text加入到info_list列表中
    info_list = []
    for each in info:
        info_list.append(each.text.replace(",", " "))

    return info_list


def get_available_slot_info(driver, date=get_date_next_week()):
    """
    这个函数能根据driver获得date日子里的每一个slot的可预约情况。
    :param driver: driver
    :param date: get_date_next_week()
    :return: list
    """
    # 等待“健身房预约”的字样出现
    wait_until(driver, By.ID, "page-title")

    # 获取7天的所有元素，每个元素代表一天
    seven_day = driver.find_elements(By.CSS_SELECTOR, "ul.slot-list > li.slot")

    # 从7天的元素里根据date定位当天。
    certain_day = [i for i in seven_day if date in i.text][0]

    # 获取当天的7个slot
    seven_slot = certain_day.find_elements(By.CSS_SELECTOR, "li > span.time-slot")

    # 获取每个slot的的日期，时间，class
    info = [[date, each_slot.text, each_slot.get_attribute("class")] for each_slot in seven_slot]

    # 把所有slot的class刷成可读的
    for each_line in info:
        part = each_line[-1].split(" ")
        each_line[-1] = "available" if len(part) == 1 else part[-1]

    return info


def check_availability(driver, user):
    """
    这个函数会检查当前的driver的网页，根据网页提示的不同内容返回不同的值：
    如果可以抢返回1，抢不了返回0，之前已经抢过了返回-1。
    具体的键值对以及返回值看config文件里的CONDITIONS。
    :param driver: driver
    :return: -1 or 0 or 1
    :param user: user
    """
    import re
    from selenium.webdriver.common.by import By

    # 等待页面响应
    wait_until(driver, By.ID, "block-system-main")

    # 获取页面源代码
    page_text = driver.page_source

    # 检查页面是否完整加载
    if "<body" not in page_text or "</body>" not in page_text:
        print(f"{user}: 不顺利：页面内容不完整，请检查网络或页面结构。")
        return 100

    # 下面开始搜索conditions里面的每个key。如果搜到了key则打印对应的value，返回对应的ret
    for _, (ret, key, value) in CONDITIONS.iterrows():
        if re.search(key, page_text):
            if ret == 0:
                # 如果ret是1或者是-1都交给go_user进行打印，ret等于0就在此打印。
                print(f"{user}: {value}")
            # 只要结果匹配就返回flag。
            return ret

    # 如果都找不到则写代码有问题或者页面更新了
    raise ValueError("页面不对了，要调试看一下页面。")


def cross_check(user, date, slot):
    """
    此函数会再次登陆页面，查看预约记录，交叉比对。
    :param user:
    :param date:
    :param slot:
    :return:
    """
    # 获得基本信息
    user_id = User.load(user).account
    weekday = date_to_weekday(date)
    time_span = GYM_INDEX_SLOT[slot]

    # 得到user的最新预约情况
    latest_reservation_info = get_reservation_info(user=user, date=date, is_print=False)[0]

    if user_id and weekday and time_span in latest_reservation_info:
        # print(f"顺利：交叉比对成功。")
        # print(f"预约信息：{latest_reservation_info}")
        return True
    else:
        print(f"{user}: 不顺利：交叉对比失败，或许是没有预约成功。")
        print(f"{user}: 不顺利：最近的一条预约信息是：{latest_reservation_info}")
        return False


def save_admin_cookie():
    """
    这个函数会返回一个外网cookie。
    这个外网cookie可以协助保存内网cookie，也可以和内网cookie一起被读入。
    :return: dict
    """
    # 初始化 driver 实例
    driver = initiate_driver(URL_IDCALLBACK_INTERNET)

    # 等待“厦门大学校外访问校内资源认证”这几个字出现（页面响应）
    wait_until(driver, By.CSS_SELECTOR, "div.main > div.header > div.portal-title.no-logo", 10)

    # 填写账号
    blank_account_internet = driver.find_element(By.ID, "user_name")
    blank_account_internet.send_keys(ADMIN_ACCOUNT)

    # 填写密码
    blank_password_internet = driver.find_element(By.CSS_SELECTOR, "div.login-form-item.password-field > div.el-input.password-input > input")
    blank_password_internet.send_keys(ADMIN_PASSWORD)

    # 回车
    button_login_internet = driver.find_element(By.ID, "login")
    button_login_internet.click()

    # 等待页面响应
    wait_until(driver, By.CSS_SELECTOR, "#navbar > div > div.navbar-header > a.name.navbar-brand")

    # 保存 cookie
    cookie = driver.get_cookies()[0]

    # 如果没有这个文件夹就做一个
    folder_path = PATH_COOKIE / "admin"
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)

    # 获取当前的时间，给即将保存cookie的json文件命名
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # 获得文件夹路径
    file_name = f"cookie_admin_{timestamp}.json"
    file_path = folder_path / file_name

    # 将cookie写入json文件
    with open(file_path, "w", encoding="utf-8") as f:  # type: ignore
        json.dump(cookie, f, ensure_ascii=False, indent=4)

    # 整理 cookie/user 文件夹
    manage_file(PATH_COOKIE / "admin", MAX_COOKIE_FILES, ".json")

    return True


def load_admin_cookie():
    """
    此函数会返回一个 admin cookie。
    此函数会先判断 cookie 是否有效，如果无效则保存新的。
    :return: dict
    """
    # 定向管理员文件夹
    folder_path = PATH_COOKIE / "admin"

    # 如果目录不存在则新建目录
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    # 如果目录里没有 json 文件则保存一个新的cookie
    if len([each for each in folder_path.glob("cookie_admin_*.json") if each.is_file()]) == 0:
        print(f"admin: 管理员cookie文件夹为空，正在重新保存管理员cookie。")
        save_admin_cookie()
        return load_admin_cookie()

    # 对所有 json 文件排序，找到最新的 json 文件的文件名
    jsons = [each.name for each in folder_path.glob("cookie_admin_*.json") if each.is_file()]
    jsons.sort()
    file_name = jsons[-1]

    # 根据文件名查看 cookie 是否过期，如果过期则重新保存一个新的
    time_str = file_name.split("_", 2)[-1].replace(".json", "")
    if not is_cookie_not_expired(time_str, TIMEOUT_INTERNET_COOKIE):
        print(f"admin: 管理员cookie过期，正在重新保存管理员cookie。")
        save_admin_cookie()
        return load_admin_cookie()

    # 读取 json 文件得到 cookie
    cookie_path = folder_path / file_name
    with open(cookie_path, "r", encoding="utf-8") as f:
        admin_cookie = json.load(f)

    return admin_cookie


def save_user_cookie(user: str):
    """
    这个函数会用user这个账号登陆url这个网页，抓取到一个cookie
    并将得到的cookie写入一个json文件
    :param user: user
    :return: True
    """
    # 加载用户信息
    _user = User.load(user)
    account = _user.account
    password = _user.password

    # 根据网络情况初始化浏览器实例
    driver = initiate_driver(URL_IDCALLBACK_INTRANET, admin_cookie=IS_INTERNET)

    # 等待页面响应
    wait_until(driver, By.CSS_SELECTOR, "p.login-title", 10)

    # 填写账号
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(account)

    # 填写密码
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    # 点击登陆
    login_button = driver.find_element(By.ID, "login_submit")
    login_button.click()

    # 获得用户 cookie
    cookie = driver.get_cookies()[0]

    # 待写入 json 文件的文件夹的路径
    folder_path = PATH_COOKIE / user

    # 如果没有这个文件夹就做一个
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)

    # 获取当前的时间，给即将保存cookie的json文件命名
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # 获得文件夹路径
    file_name = f"cookie_{user}_{timestamp}.json"
    file_path = folder_path / file_name

    # 将cookie写入json文件
    with open(file_path, "w", encoding="utf-8") as f:  # type: ignore
        json.dump(cookie, f, ensure_ascii=False, indent=4)

    # 整理 cookie/user 文件夹
    manage_file(PATH_COOKIE / user, MAX_COOKIE_FILES, ".json")

    return True


def load_user_cookie(user: str):
    """
    此函数返回返回用户cookie。
    :param user: str
    :return: dict
    """
    # 定向用户文件夹
    folder_path = PATH_COOKIE / user

    # 如果目录不存在则新建目录
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    # 如果目录里没有 json 文件则保存一个新的cookie
    if len([each for each in folder_path.glob("cookie_*.json") if each.is_file()]) == 0:
        print(f"{user}: 用户cookie文件夹为空，正在重新保存用户cookie。")
        save_user_cookie(user)
        return load_user_cookie(user)

    # 对所有 json 文件排序，找到最新的 json 文件的文件名
    jsons = [each.name for each in folder_path.glob("cookie_*.json") if each.is_file()]
    jsons.sort()
    file_name = jsons[-1]

    # 根据文件名查看 cookie 是否过期，如果过期则重新保存一个新的
    time_str = file_name.split("_", 2)[-1].replace(".json", "")
    if not is_cookie_not_expired(time_str, TIMEOUT_INTRANET_COOKIE):
        print(f"{user}: 用户cookie过期，正在重新保存用户cookie。")
        save_user_cookie(user)
        return load_user_cookie(user)

    # 读取 json 文件得到 cookie
    cookie_path = folder_path / file_name
    with open(cookie_path, "r", encoding="utf-8") as f:
        user_cookie = json.load(f)

    return user_cookie


def wait_until(driver, locator, value, timeout: int = TIME_WAIT_UNTIL):
    """
    这个函数能直接进行等待，这次封装可以不那么繁琐，不用写等待时长。
    因为很多时候都忘记这个等待怎么写。
    :param driver: driver
    :param locator: By.xxxx
    :param value: 定位内容
    :param timeout: 等待时长，如果整个时长过去了就下一步
    :return: True
    """

    w = WebDriverWait(driver, timeout)
    w.until(EC.presence_of_element_located((locator, value)))

    return True


def get_reservation_url(date, slot):
    slot += 8  # slot range: 1-7
    url = f"https://cgyy.xmu.edu.cn/room_apl/1/{date}/{slot}/cg"
    return url


def get_reservation_info(user: str = "all", date: str = "now", is_print: bool = True):
    """
    这个函数很成熟，会返回一个二维列表，这个二维列表中的每一行都是一个预约记录。
    user可以选"all", "hjl", "gby"等
    如果user选all就返回所有用户的信息，不然就只返回某个用户的信息
    date可以选"all", "now", "new", "this_week", "2025-01-01"
    如果date是all就返回所有的预约信息，now就返回今天的预约信息，new就返回下周的预约信息，this_week返回这周的所有预约信息，
    如果是2025-01-01就返回某天的预约信息。
    :param user: "all", "hjl", "gby"
    :param date: "all", "this_week", "now", "new", "2025-01-01"
    :param is_print: 是否需要打印出来
    :return: (-1, -1) ndarray
    """
    # 待返回的数组，会存有目标用户目标天的预约信息
    info = []

    # 如果选择all模式则要把所有的用户都加入到users列表中，不然就是单人模式
    users = [each[0] for each in User.get_info()] if user == "all" else [user]

    # 对每个users列表里面的user，得到用户列表里所有用户的预约记录，添加到info里面
    for each_user in users:
        # 获得每个用户的所有预约记录
        driver = initiate_driver(URL_MY_RESERVATION, user_cookie=each_user, admin_cookie=IS_INTERNET, headless=HEADLESS)
        each_user_info = get_all_reservation_info(driver)
        # 把当前用户的所有记录添加到info列表中
        info.extend(each_user_info)

    # 根据date对info里面的记录进行筛选
    if date == "all":  # 不进行筛选
        info = info
    elif date == "this_week":  # 打印本周的预约信息
        info = [each for each in info if "取消预约" in each]
    elif date == "now":  # 打印今天的预约信息
        info = [each for each in info if get_date_now() in each]
    elif date == "new" or date == "next_week":  # 打印下周这个点的预约信息
        info = [each for each in info if get_date_next_week() in each]
    elif is_date_valid(date):  # date是2025-01-01类似的时间，打印某天的预约信息
        info = [each for each in info if date in each]
    else:
        raise ValueError(f"时间格式不正确：{date}")

    # 如果需要打印则把info的内容打印出来
    if is_print:
        for each in info:
            print(each)

    return info


def get_available_slot_list(date=get_date_next_week(), show=True):
    """
    这个函数要完成两个目的：
    1. 打印当天的可预约结果
    2. 得到一个available list给每个用户
    :param date: date=get_date_next_week()
    :param show: 是否打印当天的预约结果
    :return: list
    """
    # 检查传入的日期合法性：
    if not is_date_valid(date):
        return None

    # 匿名初始化driver实例并获取当天预约信息
    driver = initiate_driver(URL_RESERVATION, admin_cookie=IS_INTERNET)
    info = get_available_slot_info(driver, date)
    available_slot_list = [i + 1 for i in range(7) if info[i][-1] == "available"]

    # 打印当天预约信息
    if show:
        # 打印当前时间，预约网址
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"预约时间：{t}")
        print(f"预约网址：{URL_RESERVATION}")
        # 打印当天预约信息
        for each_line in info:
            each_slot = f"[{each_line[0]} {each_line[1]}]: {each_line[2]}"
            print(each_slot)

    return available_slot_list


def go_user(user, date, avail_list, backup):
    """
    给每个用户分配若干个slot来抢
    go函数调用若干go_user函数，go_user函数调用若干go_user_slot函数。
    :param backup: 日志记录文件
    :param user: user
    :param date: 默认7天后
    :param avail_list: 还有空的列表
    :return: bool value
    """
    # 重写print
    rewrite_print(backup)

    # 有两种特殊情况需要排除，但是在这里排除不了：
    # 本账号在当天已经预约了其他天的健身房，以及本账号当天预约了当天的健身房
    # 其中本账号当天预约其他天数这个在服务器里是查不到的，只能通过预约结果来返回。
    # 所以这两种情况放到go_user_slot里面去查询然后返回。

    # 获取user的偏好列表，与empty列表进行比对，得到按照用户偏好排序的能抢的列表
    pref_list = User.load(user).slot_preference
    avail_pref_list = [each for each in pref_list if each in avail_list]

    # 如果avail_pref_list为空则跳出
    if not avail_pref_list:
        print(f"详情请查看链接：{URL_RESERVATION}")
        print(f"{user}: {date}当天已经没有你想要的时间段可以预约，但是有你不想要的时间段可以预约。")
        return False

    # 对有空偏好列表进行遍历，预约每一个时间段
    # 传回-1表示已有预约，传回0表示预约失败，传回1表示预约成功
    for each_slot in avail_pref_list:
        flag = go_user_slot(user, date, each_slot)
        if flag == 1:
            print(f"{user}: 按照用户喜好预约成功。")
            return True
        elif flag == -1:
            print(f"{user}: 用户今天已有预约，本次预约失败。")
            return False
        elif flag == 0:
            continue
        else:
            raise ValueError("go_user_slot()传回的参数有问题啊。")

    print(f"{user}: 预约{date}的健身房失败。")
    return False


def go_user_slot(user, date, slot):
    """
    这个函数是最基本的函数，最核心的函数，会对某个用户在某天的某个时间段进行预约。
    如果用户已有预约则本次预约会失败，则返回-1；
    如果本次预约成功则返回1；
    如果本次预约失败则返回0。
    :param user: 用户
    :param date: 日期
    :param slot: 时间段
    :return: -1, 0, 1
    """
    # 根据传入参数制作url给后续访问
    print(f"{user}: 开始预约 {date} 第 {slot} 个时间段 {GYM_INDEX_SLOT[slot]} 的健身房。", sep="")
    url = get_reservation_url(date, slot)

    # 带着cookie初始化driver实例
    driver = initiate_driver(url=url, user_cookie=user, admin_cookie=IS_INTERNET, headless=HEADLESS)

    # 直接访问预约页面，获取网页的提示结果，并根据提示结果返回-1，0，1。
    flag = check_availability(driver, user)

    # 如果可以预约则继续预约
    if flag == 1:
        if driver_submit(driver, user):
            if cross_check(user, date, slot):
                print(f"{user}: 成功预约 {date} 第 {slot} 个时间段 {GYM_INDEX_SLOT[slot]} 的健身房。", sep="")
                return True

    return flag
