from appbbt import BbtCase, step
from appbbt.app import app


class LoginTestCase(BbtCase):
    @step('登录')
    def login(self):
        self.set_text('et_user_name', 'zhuzhe')
        self.set_text('et_pwd', '123456')
        # self.click('btn_login')
        self.tap([(1000, 1000)])
        self.wait('btn_test', 20)

    @step('我的团队 > 队伍')
    def group_team(self):
        self.click('ll_group')
        self.tap([(1250, 130)])

    def test_team(self):
        self.login()
        self.group_team()


if __name__ == "__main__":
    app.init('登录测试', __doc__)

    app.configure(
        appPackage='com.mt.digitalsports',
        appActivity='.user.activity.view.UserLoginActivity',
    )

    app.run()
