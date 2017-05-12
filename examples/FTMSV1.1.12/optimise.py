from appbbt import BbtCase, app, action, step

APP_PACKAGE = 'com.leoet.ftmsonline'
MAIN_ACTIVITY = '.activity.MainActivity'
LOGIN_ACTIVITY = '.activity.LoginActivity'


class TestCase(BbtCase):
    def setUp(self):
        super().setUp()

        # 如果是主窗口，直接返回
        if app.driver.current_activity == MAIN_ACTIVITY:
            return

        # 如果不是登录窗口，显示登录窗口
        if app.driver.current_activity != LOGIN_ACTIVITY:
            app.driver.start_activity(APP_PACKAGE, LOGIN_ACTIVITY)

        # 登录
        if not self.fast_login():
            self.login('13838003920', 'asdf1234')

    @step('快速登录')
    def fast_login(self):
        self.click('user_login_btn')
        return self.wait_activate(MAIN_ACTIVITY, 5, 0.5)

    @step('登录')
    def login(self, username, password):
        self.set_text('login_userName_edt', username)
        self.set_text('login_userPwd_edt', password)
        self.click('user_login_btn')
        self.wait_activate(MAIN_ACTIVITY, 5, 0.5)

    def test_1(self):
        print('test_1')
        self.sleep(3)

    def test_2(self):
        print('test_2')
        self.sleep(3)

    def test_3(self):
        print('test_3')
        self.sleep(3)


if __name__ == "__main__":
    app.init('登录测试', __doc__)
    app.configure(
        keep_alive=True,
        appPackage=APP_PACKAGE,
        appActivity=LOGIN_ACTIVITY,
        noReset=True,
    )
    app.run()
