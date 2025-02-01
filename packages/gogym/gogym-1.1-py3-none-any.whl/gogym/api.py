# api.py文件可以调用本项目的任何包
# 用户也只允许调用api.py的包
from multiprocessing import Process
from selenium.webdriver.common.by import By
from gogym.config import GYM_INDEX_SLOT, IS_INTERNET, URL_MY_RESERVATION
from gogym.control import get_safe_shared_list, rewrite_print, is_user_exist, generate_log
from gogym.core import get_available_slot_list, User, go_user, get_reservation_info, get_reservation_url, check_availability, driver_submit, cross_check, initiate_driver, wait_until
from gogym.underlying import get_date_next_week, everything_to_date_str


def save(initial, name, account, password, phone, slot_preference) -> None:
    """
    用户可以调用此函数来保存一个新的账户。
    其中的 slot_preference 表示你的场地偏好，
    [4, 5, 6, 7] 表示先抢第4个时间段的场地，抢不到就抢5，再是6，再是7，如果7还抢不到今天就不抢了。
    :param initial: "hxt"
    :param name: "黄啸天"
    :param account: "24820231162341"
    :param password: "Hxt20010623."
    :param phone: "13871234567"
    :param slot_preference: [4, 5, 6, 7]
    :return:
    """
    # 开始记录日志
    backup = get_safe_shared_list()
    rewrite_print(backup)

    # main
    User.save(initial, name, account, password, phone, slot_preference)

    # 生成日志文件
    generate_log(backup)
    return None


def go(user: str = "all", date: str = "new", slot: int = None) -> None:
    """
    此函数能够用多线程让每个用户预约健身房。
    :param user: "all", "hxt"
    :param date: "now", "new", "2025-01-01"
    :param slot: 5
    :return: None
    """
    # 日志记录：生成一个安全列表，并重写print
    backup = get_safe_shared_list()
    rewrite_print(backup)

    # 格式化 user
    users = [each[0] for each in User.get_info()] if user == "all" else [user]
    if not is_user_exist():  # 如果 users 目录里没有用户的 json 则提示需要保存并退出
        print(f"data/users目录中没有用户，请调用 user_save() 函数保存新用户。")
        return generate_log(backup)

    # 格式化 date
    date = everything_to_date_str(date)

    # 格式化 slot
    print(f"-----------------------------------当天预约信息-----------------------------------")
    slots = get_available_slot_list(date, show=True) if slot is None else [slot]
    if not slots:  # 如果当天没有可预约的时间段则退出
        print(f"------------------------{date} 当天已经没有时间段可以预约-----------------------")
        return generate_log(backup)

    # 将每个用户的go_user进程都添加到进程池 pool 里
    pool = []
    for user in users:
        each = Process(target=go_user, args=(user, date, slots, backup), name=f"Process-{user}")
        pool.append(each)

    # 启动所有进程
    for each in pool:
        each.start()
    print(f"----------------------------------所有进程已启动----------------------------------")

    # 等待所有进程结束
    for each in pool:
        each.join()
    print(f"----------------------------------所有进程已完成----------------------------------")

    # 打印所有用户今天所抢的健身房
    get_reservation_info(user="all", date=date, is_print=True)

    # 日志记录：生成日志文件
    return generate_log(backup)


def cancel(user: str = "all", date: str = "new") -> None:
    """
    此函数能取消用户预约。
    :param user: "all", "hxt"
    :param date: "now", "new", "next_week", "星期五", "2025-01-01"
    :return: None
    """

    def get_each_assignment(user, date):
        """
        得到某一个用户的所有目标预约信息
        :param user: "hxt"
        :param date: "2025-01-01"
        :return: tuple
        """
        # 初始化
        driver = initiate_driver(url=URL_MY_RESERVATION, user_cookie=user, admin_cookie=True)

        # 等待页面响应（翔安校区体育馆预约系统）
        wait_until(driver, By.CSS_SELECTOR, "#navbar > div > div.navbar-header > a.name.navbar-brand")

        # 找到所有的预约信息
        info = driver.find_elements(By.CSS_SELECTOR, "#block-system-main > div > div > div > table > tbody > tr")

        # 找到所有能取消的预约信息
        info_this_week = [(each.text.replace(",", " "), each.find_element(By.CSS_SELECTOR, "a").get_attribute("href")) for each in info if "取消预约" in each.text]

        # 找到目标预约信息，有就返回(info, url)，如果没有则返回None
        try:
            info_target = [(each[0], user, each[1]) for each in info_this_week if date in each[0]][0]
        except IndexError:
            info_target = None

        return info_target

    def handle_each_assignment(user, url):
        """
        取消预约页面处理
        :return:
        """
        # 初始化
        driver = initiate_driver(url, user_cookie=user, admin_cookie=IS_INTERNET)

        # 等待页面响应
        wait_until(driver, By.ID, "page-title")

        # 定位“删除”元素，点击删除
        button_delete = driver.find_element(By.ID, "edit-submit")
        button_delete.click()

    # 开始记录日志
    backup = get_safe_shared_list()
    rewrite_print(backup)

    # 格式化用户列表与日期字符串
    users = [each[0] for each in User.get_info()] if user == "all" else [user]
    date = everything_to_date_str(date)

    # 获取所有的待取消列表 [(info, initial, url), (...), ...]
    assignment = []
    for each_user in users:
        each_assignment = get_each_assignment(each_user, date)
        if each_assignment is not None:
            assignment.append(each_assignment)

    # 打印
    print(f"----------------------------------待取消预约信息----------------------------------")
    for each in assignment:
        print(each[0])

    # 如果目标账户群没有可以取消的预约记录就退出
    if not assignment:
        print(f"{user}: 没有可以取消的预约。")
        return generate_log(backup)

    # 对所有 url 进行取消操作
    print(f"-----------------------------------正在取消预约-----------------------------------")
    for each_assignment in assignment:
        handle_each_assignment(each_assignment[1], each_assignment[2])
        print(f"{each_assignment[1]}: 预约取消成功 “{each_assignment[0][:-5]}”")

    # 生成日志文件
    return generate_log(backup)


def check(user: str = "all", date: str = "all") -> None:
    """
    用户可以调用此函数来检查若干个用户的预约情况。
    user 可以选择"all", "xxx". 其中 xxx 是用户的 initial。
    all 表示查询 users 里的所有用户，xxx 表示查询某一个用户。
    date 可以选择"all", "now", "new", "this_week", "20xx-xx-xx".
    all 表示查询用户的所有预约，now 表示查询今天的预约，new 和 this_week 表示查询最新一天预约，
    20xx-xx-xx 表示查询某一天的预约（超过三十天的查询不到）。
    :param user: "all", "xxx"
    :param date: "all", "now", "new", "this_week", "20xx-xx-xx"
    :return: None
    """
    # 开始记录日志
    backup = get_safe_shared_list()
    rewrite_print(backup)

    # 日志记录头
    print(f"--------------- 正在查询 {user} 预约信息 ---------------")

    # 打印输出
    get_reservation_info(user=user, date=date, is_print=True)

    # 生成日志文件
    generate_log(backup)
    return None


if __name__ == "__main__":
    cancel(user="all", date="new")
    # go()
    pass
