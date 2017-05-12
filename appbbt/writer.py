import os

import time

from appbbt import BbtCase

STAGE_NONE = 0
STAGE_TESTCASE = 1


class Writer(object):
    stage = STAGE_NONE

    def __init__(self, testName, testDescription):
        self.testName = testName
        self.testDescription = testDescription

        self.time_str = time.strftime('%Y%m%d-%H%M%S')
        self.index_file = 'index.md'
        self.report_file = '%s/report.md' % self.time_str
        self.screenshots_dir = '%s/screenshots' % self.time_str

        os.makedirs('reports/%s' % self.time_str, exist_ok=True)
        os.chdir("reports")

        self.writeTitle()

    def write(self, message):
        with open(self.report_file, 'a', encoding='utf-8') as fp:
            fp.write(message)

    def writeTitle(self):
        with open(self.report_file, 'w', encoding='utf-8') as fp:
            fp.write('# 测试报告 - %s\n\n' % self.testName)
            if self.testDescription:
                fp.write(self.testDescription)
                fp.write('\n')
            fp.write('* 测试开始于 %s\n' % time.strftime('%Y-%m-%d %H:%M:%S'))

    def writeTestCase(self, test:
        BbtCase

    ):
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        if self.stage < STAGE_TESTCASE:
            self.stage = STAGE_TESTCASE
            fp.write('\n## 测试用例\n\n')

        anchor = test._testMethodName
        fp.write('<a id="%s"></a>\n' % anchor)
        fp.write('### %s\n\n' % test)

        fp.write('* 开始时间: %s\n\n' % time.strftime('%Y-%m-%d %H:%M:%S'))

        if test._testMethodDoc.description:
            fp.write(test._testMethodDoc)
            fp.write('\n')


def writeStartStep(self, step):
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        fp.write('步骤 %d: %s\n\n' % (step.number, step.name))
        fp.write('| 操作 | 用时（秒） |\n')
        fp.write('| ---- | ----: |\n')


def writeStopStep(self, step):
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        fp.write('| 合计 | %.2f |\n\n' % step.time_taken)


def writeStartAction(self, action):
    pass


def writeStopAction(self, action):
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        fp.write('| %s | %.2f |\n' % (action.name, action.time_taken))


def writeSuccess(self, test):
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        fp.write('* 测试结果: 通过，用时 %.2f 秒\n\n' % test.time_taken)


def writeTraceback(self, err, fp):
    fp.write('```python\n')
    fp.write(err)
    fp.write('```\n\n')


def takeScreenShot(self, test):
    from .app import app

    app.logger.info('开始截屏 ...')
    start_time = time.time()
    os.makedirs(self.screenshots_dir, exist_ok=True)
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        filename = '%s-%s.png' % (test._testMethodName, time.strftime('%Y%m%d-%H%M%S'))
        save_as = os.path.join(self.screenshots_dir, filename)
        if app.driver and app.driver.get_screenshot_as_file(save_as):
            time_taken = time.time() - start_time
            app.logger.info('截屏成功，用时 %.2f 秒', time_taken)
            fp.write('截屏成功，用时 %.2f 秒\n\n' % time_taken)
            link = 'screenshots/%s' % (filename)
            fp.write('![%s](%s)\n\n' % (link, link))
        else:
            time_taken = time.time() - start_time
            app.logger.info('截屏失败，用时 %.2f 秒', time_taken)
            fp.write('截屏失败，用时 %.2f 秒\n\n' % time_taken)


def writeFailure(self, test, err):
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        fp.write('* 测试结果: 未通过，用时 %.2f 秒\n\n' % test.time_taken)
        self.writeTraceback(err, fp)
        self.takeScreenShot(test)


def writeError(self, test, err):
    with open(self.report_file, 'a', encoding='utf-8') as fp:
        fp.write('* 测试结果: 出错，用时 %.2f 秒\n\n' % test.time_taken)
        self.writeTraceback(err, fp)
        self.takeScreenShot(test)


def writeSummary(self, result):
    self.writeReportSummary(result)
    self.writeReportIndex(result)


def writeReportIndex(self, result):
    summary_header = ''.join((
        '| 测试时间 | 测试名称 | 通过 | 未通过 | 出错 | 合计 |\n',
        '| ---- | ---- | ---- | ---- | ---- | ---- |\n',
    ))
    summary_row = (
        self.time_str,
        '[%s](%s)' % (self.testName, self.report_file),
        str(len(result.successes)),
        str(len(result.failures)),
        str(len(result.errors)),
        str(result.testsRun)
    )
    summary_line = '| ' + ' | '.join(summary_row) + ' |\n'
    with open(self.index_file, 'a', encoding='utf-8') as fp:
        if fp.tell() == 0:
            fp.write(summary_header)
        fp.write(summary_line)


def writeReportSummary(self, result):
    summary_line = '测试用例 %d 个, 通过 %d 个，未通过 %d 个，出错 %d 个。\n' % (
        result.testsRun, len(result.successes), len(result.failures), len(result.errors)
    )

    with open(self.report_file, 'a', encoding='utf-8') as fp:
        fp.write('## 总结\n\n')
        fp.write('| 测试用例 | 结果 | 用时（秒） |\n')
        fp.write('| ----- | ---- | ----: |\n')
        for test in result.successes:
            fp.write('| [`%s`](#%s) | 通过 | %.2f |\n' % (test, test._testMethodName, test.time_taken))
        for test, _err in result.failures:
            fp.write('| [`%s`](#%s) | 未通过 | %.2f |\n' % (test, test._testMethodName, test.time_taken))
        for test, _err in result.errors:
            fp.write('| [`%s`](#%s) | 出错 | %.2f |\n' % (test, test._testMethodName, test.time_taken))
        fp.write('\n')
        fp.write(summary_line)
