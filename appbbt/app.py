import subprocess
import logging
import time
from appium import webdriver


class App(object):
    driver: webdriver.Remote = None
    logger: logging.Logger = None
    writer = None

    def init(self,
             testName,
             testDescription=None,
             logLevel='INFO',
             logFormat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
             ):
        from appbbt.writer import Writer

        logging.basicConfig(level=logLevel, format=logFormat)

        self.logger = logging.getLogger('appbbt')
        self.logger.info('程序启动.')

        self.writer = Writer(testName, testDescription)

    def configure(self,
                  # webdriver.Remote 参数
                  command_executor='http://127.0.0.1:4723/wd/hub',
                  keep_alive=False,

                  # desired_capabilities 参数
                  # 参考: https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/caps.md
                  platformName='Android',
                  platformVersion='4.4.2',
                  deviceName=None,
                  app=None,
                  appPackage=None,
                  appActivity=None,
                  unicodeKeyboard=True,  # 使用 unicode 键盘，可以使用中文
                  resetKeyboard=True,  # 测试结束后回复原来的键盘设置
                  noReset=False,
                  newCommandTimeout=180,  # 客户端命令超时时间
                  **kwargs
                  ):
        if deviceName is None:
            for line in subprocess.check_output('adb devices').splitlines():
                if line.endswith(b'\tdevice'):
                    deviceName = line.partition(b'\t')[0].decode()
                    break

        assert deviceName
        assert app or (appPackage and appActivity)

        self.logger.info('设备名: %s', deviceName)
        self.logger.info('应用程序: %s', app or appPackage + appActivity)

        # noinspection PyTypeChecker
        desired_capabilities = dict(
            platformName=platformName,
            platformVersion=platformVersion,
            deviceName=deviceName,
            app=app,
            appPackage=appPackage,
            appActivity=appActivity,
            unicodeKeyboard=unicodeKeyboard,
            resetKeyboard=resetKeyboard,
            noReset=noReset,
            newCommandTimeout=newCommandTimeout,
            **kwargs
        )

        self.logger.info('Appium 服务器: %s', command_executor)
        self.logger.info('desired_capabilities: %s', desired_capabilities)
        self.logger.info('初始化 WebDriver ...')

        start_time = time.time()
        self.driver = webdriver.Remote(command_executor, desired_capabilities, keep_alive=keep_alive)
        time_taken = time.time() - start_time

        self.logger.info('初始化 WebDriver 成功, 用时 %.2f 秒.', time_taken)
        self.writer.write('* 初始化 WebDriver 成功, 用时 %.2f 秒.\n' % time_taken)

    def run(self):
        import unittest
        from appbbt import BbtRunner

        self.logger.info('测试开始 ...')
        try:
            unittest.main(testRunner=BbtRunner)
        finally:
            self.quit()

    def quit(self):
        self.logger.info('退出程序.')
        if self.driver:
            self.driver.quit()


app = App()
