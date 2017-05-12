import functools
import subprocess
import textwrap
import time
import unittest

from appium.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException
from zope.cachedescriptors.property import Lazy as lazy_property

from . import util
from .app import app
from .position import ElementPosition


class Step(object):
    done = False

    def __init__(self, number, name):
        self.number = number
        self.name = name

        self.actions = []
        self.start_time = time.time()

        app.logger.info('步骤 %d. %s ...', self.number, self.name)
        app.writer.writeStartStep(self)

    @property
    def time_taken(self):
        return time.time() - self.start_time

    def stop(self):
        self.done = True

        app.logger.info('合计 %.2f 秒', self.time_taken)
        app.writer.writeStopStep(self)


class Action(object):
    def __init__(self, name):
        self.name = name

        self.start_time = time.time()

        app.logger.info('操作: %s ...', self.name)
        app.writer.writeStartAction(self)

    @property
    def time_taken(self):
        return time.time() - self.start_time

    def stop(self):
        app.logger.info('用时 %.2f 秒.', self.time_taken)
        app.writer.writeStopAction(self)


def step(name=None):
    def outer(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            nonlocal
            name
            if 'step_name' in kwargs:
                name = kwargs.pop('step_name')
            if name is None:
                name = '{}({})'.format(func.__name__, util.args_to_str(args, kwargs))
            self.startStep(name)
            result = func(self, *args, **kwargs)
            self.stopStep()
            return result

        return inner

    return outer


def action(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        action_name = kwargs.pop('action_name', None)
        if action_name is None:
            action_name = '{}({})'.format(func.__name__, util.args_to_str(args, kwargs))
        self.startAction(action_name)
        result = func(self, *args, **kwargs)
        self.stopAction()
        return result

    return inner


class TestMethodDoc(object):
    first_line = None
    description = None

    def __init__(self, doc):
        self.doc = doc
        if doc:
            self.first_line, _, self.description = doc.partition('\n')
            self.first_line = self.first_line.strip()
            self.description = textwrap.dedent(self.description).strip()


class BbtCase(unittest.TestCase):
    start_time = 0

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.steps = []
        self._testMethodDoc = TestMethodDoc(self._testMethodDoc)

    def __str__(self):
        if self._testMethodDoc.first_line:
            return '%s(%s)' % (self._testMethodDoc.first_line, self._testMethodName)
        return self._testMethodName

    def setUp(self):
        self.start_time = time.time()

    @lazy_property
    def time_taken(self):
        return time.time() - self.start_time

    def find_element_by_id(self, id_, raise_=True):
        try:
            el = app.driver.find_element_by_id(id_)
        except NoSuchElementException:
            el = None
        if el is None and raise_:
            raise RuntimeError('指定的元素不存在: %s', id_)
        return el

    def exists(self, id_):
        return self.find_element_by_id(id_, False) is not None

    def get_position(self, el):
        """获取位置
        :type el: WebElement or str
        """
        if isinstance(el, str):
            el = self.find_element_by_id(el)
        return ElementPosition.fromWebElement(el)

    @action
    def sleep(self, seconds):
        time.sleep(seconds)

    @action
    def hide_keyboard(self):
        app.driver.hide_keyboard()

    @action
    def adb(self, cmd_line):
        """执行 adb 命令

        实际执行的命令是： adb -s <deviceName> <cmd_line>

        :rtype: [status, output] 
        """
        deviceName = app.driver.capabilities['deviceName']
        cmd = 'adb -s %s %s' % (deviceName, cmd_line)
        return subprocess.getstatusoutput(cmd)

    @action
    def monkey(self, event_count):
        """调用 adb monkey

        :param event_count: 执行的次数 
        """
        deviceName = app.driver.capabilities['deviceName']
        appPackage = app.driver.capabilities['appPackage']
        seed = int(time.time())
        cmd = 'adb -s %s monkey -p %s -s %d %d' % (deviceName, appPackage, seed, event_count)
        return subprocess.getstatusoutput(cmd)

    @action
    def clever_monkey(self, event_count, exclude=None):
        """聪明一点的 Monkey，只点击能够点击的对象，知道哪些对象不能点击

        :param event_count: 
        :param exclude: 要排除的对象 
        """

    @action
    def wait(self, ids, timeout, raise_=False):
        """等待指定的对象出现，返回找到的对象id和对象

        :param ids: 对象 id 数组
        :param timeout: 超时时间，单位为秒
        :rtype: WebElement
        """
        if isinstance(ids, str):
            ids = [ids]
        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(1)
            for id_ in ids:
                el = self.find_element_by_id(id_, False)
                if el:
                    return el

        if raise_:
            raise RuntimeError('没有找到指定的元素: %s', ids)

    @action
    def wait_activate(self, activity, timeout, interval=1):
        """等待指定的 activity
        """
        return app.driver.wait_activity(activity, timeout, interval)

    @action
    def click(self, id_):
        el = self.find_element_by_id(id_)
        el.click()

    @action
    def send_keys(self, id_, value):
        el = self.find_element_by_id(id_)
        el.send_keys(value)

    @action
    def set_text(self, id_, value):
        el = self.find_element_by_id(id_)
        el.set_text(value)

    @action
    def tap(self, positions, duration=None):
        app.driver.tap(positions, duration)

    @action
    def swipe(self, start_x, start_y, end_x, end_y):
        """按住然后划动
        """
        app.driver.swipe(start_x, start_y, end_x, end_y)

    @action
    def flick(self, start_x, start_y, end_x, end_y):
        """快速划动

        注意: 实际使用中发现，end_x、end_y 其实是相对坐标
        """
        app.driver.flick(start_x, start_y, end_x, end_y)

    def _getLastStep(self):
        if self.steps:
            return self.steps[-1]

    def _createStep(self, name):
        number = len(self.steps) + 1
        step = Step(number, name)
        self.steps.append(step)
        return step

    def startStep(self, name):
        # 自动关闭上一个 Step
        step = self._getLastStep()
        if step and not step.done:
            step.stop()

        # 创建新的 Step
        self._createStep(name)

    def startAction(self, name):
        step = self._getLastStep()

        # 自动创建 Step
        if not step or step.done:
            step = self._createStep('未命名')

        action = Action(name)
        step.actions.append(action)

    def stopAction(self):
        step = self.steps[-1]
        action = step.actions[-1]
        action.stop()

    def stopStep(self):
        step = self.steps[-1]
        step.stop()
