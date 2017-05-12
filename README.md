# appbbt - Appium Black Box Testing

**主要特点**

* 封装 App 的常用操作（点击，输入文本，划动等）
* 实现相对与特定元素的位置运算
* 输出 Markdown 格式的报告

**主要概念**

* 步骤（Step)：一系列操作的集合
* 操作（Action）：一个动作，比如点击，输入文本等

## 用法

参见 examples 目录中的示例。

## API 说明

### appbbt.app

`init(testName, testDescription, logLevel)` - 初始化信息

* testName: 给测试起一个名称吧
* testDescription: 测试的描述，会出现在测试报告中
* logLevel: 输出日志的级别，可以是 INFO, DEBUG 等

`configure(...)` - 设备能力等配置

* command_executor: Appium 服务器的 url
* platformName: 平台名称，缺省为 Android
* platformVersion: 平台版本
* deviceName: 设备名称，可以用 `adb devices` 查看，也可以由程序自动检测
* app, appPackage, appActivity: 用于指定要测试的应用程序，app 或 appPackage+appActivity 至少要指定一个

`run` - 开始运行

上面的参数说明参见 [Appium server capabilities
](http://appium.io/slate/en/master/?python#appium-server-capabilities)。

### appbbt.BbtCase

* `find_element_by_id(id_, raise_=True)` - 查找元素
* `exists(id_)` - 判断元素是否存在，如果存在则返回找到的元素
* `get_position(el)` - 返回元素的位置对象（ElementPosition）

操作:

* `sleep(seconds)` - Sleep
* `hide_keyboard()` - 隐藏键盘
* `wait(ids, timeout, raise_=False)` - 等待期望的元素出现，返回元素
* `click(id_)` - 单击
* `send_keys(id_, value)`
* `set_text(id_, value)`
* `tap(positions, duration)` - 轻触
* `swipe(start_x, start_y, end_x, end_y)` - 按住然后划动
* `flick(self, start_x, start_y, end_x, end_y)` - 快速划动
  * 注意: 实际使用中发现，end_x、end_y 其实是相对坐标

### ElementPosition

* `left(n)`
* `right(n)`
* `up(n)`
* `down(n)`

### 其他

* `appbbt.step` - 定义操作步骤
* `appbbt.action` - 定义操作

## 技巧

### 如何减少测试的准备过程？

参见下面的示例，在 setUp 和 fast_login 函数中，进行判断，根据当前状态采用响应的操作：

```python
APP_PACKAGE = 'com.leoet.ftmsonline'
MAIN_ACTIVITY = '.activity.MainActivity'
LOGIN_ACTIVITY = '.activity.LoginActivity'


class YourTestCase(BbtCase)
    def setUp(self):
        super().setUp()

        # 如果是主窗口，直接返回
        if app.driver.current_activity == MAIN_ACTIVITY:
            return

        # 如果不是登录窗口，显示登录窗口
        if app.driver.current_activity != LOGIN_ACTIVITY:
            app.driver.start_activity(APP_PACKAGE, LOGIN_ACTIVITY)

        # 尝试快速登录
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

...
app.configure(
    ...
    noReset=True,
)
```

上面的代码中用到的主要技巧包括：

* 采用常量定义，减少输入错误导致的判断失败;
* app.configure 中指定 noReset 为 True
* setUp 函数中利用 app.driver.current_activity 判断当前的界面;
* setUp 函数中利用 app.driver.start_activity 启动界面;
* fast_login 函数中跳过输入用户名和密码
* 尽量避免使用 app.driver.reset()

### 如何加快 Session 的启动速度？

Appium 启动一个 Session 的速度也是醉了，动不动就是几十秒甚至一百多秒，下面是提高启动速度的方法：


	* 启动 Session 时指定 appPackage 和 appActivity 而不是指定 app
	* 修改 appium-android-driver 源代码，避免不必要的软件安装


这里着重说明第二个方法，下面的文件均基于文件目录：


	* appium-desktop\resources\app\node_modules\appium\node_modules\appium-android-driver


lib\android-helpers.js:

这个文件是真正的源代码，但是真正起作用的是 build 目录下下面编译过的代码文件。

```javascript
  // ...
  await adb.install(unicodeIMEPath, false);
  // ...
  await adb.install(unlockApkPath, false);
```

build\lib\android-helpers.js:

真正要修改的文件，把 install 改成 installOrUpgrade，下面是修改后的代码：

```javascript
        // ...
        return _regeneratorRuntime.awrap(adb.installOrUpgrade(_appiumAndroidIme.path, false));
        // ...
        return _regeneratorRuntime.awrap(adb.installOrUpgrade(_appiumUnlock.path, false));
```
