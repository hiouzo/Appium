import unittest
import time

from .app import app


class BbtResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.successes = []

    def startTestRun(self):
        """测试开始"""

    def stopTestRun(self):
        """测试结束
        """
        app.writer.writeSummary(self)
        self.printErrors()

    def startTest(self, test):
        """单个测试开始"""
        super().startTest(test)
        app.writer.writeTestCase(test)

    def stopTest(self, test):
        """单个测试结束"""
        super().stopTest(test)

    def addSuccess(self, test):
        self.successes.append(test)

        app.logger.info('%s ... 通过', test)
        app.writer.writeSuccess(test)

    def addFailure(self, test, err):
        """测试失败

        参数说明参见 addError
        """
        super().addFailure(test, err)
        app.logger.info('%s ... 未通过', test)

        test, err = self.failures[-1]  # 格式化过的错误信息
        app.writer.writeFailure(test, err)

    def addError(self, test, err):
        """测试过程中遇到错误（异常）

        :param test: TestCase 对象
        :type err: (type, value, traceback) 参见: sys.exc_info()
        """
        super().addError(test, err)
        app.logger.info('%s ... 出错', test)

        test, err = self.errors[-1]  # 格式化过的错误信息
        app.writer.writeError(test, err)

    def printErrors(self):
        """打印错误"""
        app.logger.info('运行测试 %d 个，出错: %d 个，未通过 %d 个',
                        self.testsRun, len(self.errors), len(self.failures))

        seperator = '----------------------------------------'

        for test, err in self.errors:
            app.logger.info('%s 出错，详细信息:\n%s\n%s%s',
                            test, seperator, err, seperator)

        for test, err in self.failures:
            app.logger.info('%s 未通过，详细信息:\n%s\n%s%s',
                            test, seperator, err, seperator)
