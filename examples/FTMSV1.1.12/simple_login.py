from appbbt import BbtCase, step
from appbbt.app import app


class LoginTestCase(BbtCase):
    @step('登录')
    def login(self):
        self.wait('user_login_btn', 5, True)
        self.set_text('login_userName_edt', '13838003920')
        self.set_text('login_userPwd_edt', 'asdf1234')
        self.click('user_login_btn')
        self.wait('trainingmodeImg', 10, True)

    def test_login(self):
        self.login()


if __name__ == "__main__":
    app.init('登录测试', __doc__)

    app.configure(
        appPackage='com.leoet.ftmsonline',
        appActivity='.activity.LoginActivity',
    )

    app.run()
