import appbbt
from appbbt import app, step, action


class TestCase(appbbt.BbtCase):
    def test_01_success(self):
        pass

    def test_02_failure(self):
        """通不过"""
        self.assertTrue(False, '失败了!')

    def test_03_error(self):
        """会出错"""
        error

    @action
    def set_text(self, id_, value):
        pass

    @action
    def click(self, id_):
        pass

    @action
    def hide_keyboard(self):
        pass

    @action
    def wait(self, id_, timeout):
        return id_

    @step('登录')
    def login(self):
        self.set_text('et_account', 'zhuzhe')
        self.set_text('et_pwd', '123456')
        self.hide_keyboard()
        self.click('btn_login')
        self.assertIsNotNone(self.wait('ll_settings', 20), '登录失败')

    def test_04_step(self):
        """综合测试"""
        self.login()
        self.login(step_name='再次登录')


if __name__ == "__main__":
    app.init('登录测试', __doc__)

    # app.configure(
    #     appPackage='com.mt.digitalsports',
    #     appActivity='.user.activity.view.UserLoginActivity',
    # )

    app.run()
