from appbbt import BbtCase, step
from appbbt.app import app


class TestCase(BbtCase):
    @step('登录')
    def login(self):
        self.wait('et_user_name', 5, True)
        self.set_text('et_user_name', 'zhuzhe')
        self.set_text('et_pwd', '123456')
        self.click('btn_login')
        self.wait('btn_test', 15, True)

    @step('队伍管理')
    def group_team(self):
        #
        self.click('ll_group')
        self.click('rl_team')
        self.click('tv_add_team')

        # 队伍名称
        self.set_text('et_name', 'BBT001')

        # 队伍类型
        self.click('tv_team_type')
        position = self.get_position('tv_team_type').down(30)
        self.tap([position])

        # 年龄组
        self.click('tv_age_group')
        position = self.get_position('tv_age_group').down(30)
        self.tap([position])

        # 确定
        self.click('btn_confirm')

        # 向上滚屏
        start = self.get_position('rv_team_list').down(-100)
        self.flick(*start, 0, -800)
        self.sleep(2)

        for el in app.driver.find_elements_by_id('tv_class_name'):
            print(el.text)
            if el.text == 'BBT001':
                self.swipe(*self.get_position(el).center, *self.get_position(el).center.left(200))

                self.sleep(2)
                self.click('ll_delete')

                self.sleep(5)
                if self.exists('exit_ok'):
                    self.click('exit_ok')

                # 继续
                start = self.get_position('rv_team_list').down(-100)
                self.flick(*start, 0, -800)
                self.sleep(2)

    def test_team(self):
        self.login()
        self.group_team()


if __name__ == "__main__":
    app.init('登录测试', __doc__)

    app.configure(
        appPackage='com.mt.digitalsports',
        appActivity='.user.activity.view.UserLoginActivity',
        unicodeKeyboard=False,
    )

    app.run()
