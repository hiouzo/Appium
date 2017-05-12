# 测试报告 - 登录测试

* 测试开始于 2017-04-28 11:48:56
* 初始化 WebDriver 成功, 用时 19.22 秒.

## 测试用例

<a id="test_team"></a>
### test_team

* 开始时间: 2017-04-28 11:49:15

步骤 1: 登录

| 操作 | 用时（秒） |
| ---- | ----: |
| set_text('et_user_name', 'zhuzhe') | 7.39 |
| set_text('et_pwd', '123456') | 5.61 |
| tap([(1000, 1000)]) | 0.16 |
| wait('btn_test', 20) | 20.19 |
| 合计 | 33.34 |

步骤 2: 我的团队 > 队伍

| 操作 | 用时（秒） |
| ---- | ----: |
截屏成功，用时 8.84 秒

![screenshots/test_team-20170428-114949.png](screenshots/test_team-20170428-114949.png)

* 测试结果: 出错，用时 33.61 秒

```python
Traceback (most recent call last):
  File "D:/appbbt/examples/test_login.py", line 21, in test_team
    self.group_team()
  File "D:\appbbt\appbbt\case.py", line 68, in inner
    result = func(self, *args, **kwargs)
  File "D:/appbbt/examples/test_login.py", line 16, in group_team
    self.click('ll_group')
  File "D:\appbbt\appbbt\case.py", line 84, in inner
    result = func(self, *args, **kwargs)
  File "D:\appbbt\appbbt\case.py", line 212, in click
    el = self.find_element_by_id(id_)
  File "D:\appbbt\appbbt\case.py", line 129, in find_element_by_id
    raise RuntimeError('指定的元素不存在: %s', id_)
RuntimeError: ('指定的元素不存在: %s', 'll_group')
```

## 总结

| 测试用例 | 结果 | 用时（秒） |
| ----- | ---- | ----: |
| [`test_team`](#test_team) | 出错 | 33.61 |

测试用例 1 个, 通过 0 个，未通过 0 个，出错 1 个。
