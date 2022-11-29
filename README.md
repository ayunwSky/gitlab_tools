# gitlab_tools
对GitLab做一些批量创建和删除的自动化工具

## 本次使用到的 Python 库

- 库名: python-gitlab
- 官方文档: https://python-gitlab.readthedocs.io/en/stable/

## 功能概述
以下功能皆可实现批量操作：

- 创建子组
- 创建项目
- 删除组和子组
- 删除项目

## 注意事项
> 1. 操作前需要编辑 gitlab_config.yaml 配置文件,最主要的是涉及到：创建子组、删除组(包括子组)、删除项目 这三个操作时,需要更改配置文件中的id为对应组或者项目的id；
> 2. 需要执行什么操作，就打开 main.py 工具中, main 入口函数中的功能函数,然后发起CI/CD即可.

## GitLab官方提示不允许使用API创建顶级组

创建顶级组不被允许,详情参考以下：
```shell
https://docs.gitlab.com/ee/api/groups.html#new-group
https://github.com/python-gitlab/python-gitlab/issues/2372
https://github.com/python-gitlab/python-gitlab/pull/2374/commits/6bf25a8766558ded0c9a3dd1a7111b2a1c9f4837
```

后续功能 包括不限于：自动勾选流水线必须成功以及commit规范的hooks钩子,这两项功能目前有待开发...

## 日志字典配置参考
```shell
https://www.cnblogs.com/hello-/articles/11605103.html
https://blog.51cto.com/u_13691477/4756422
```

## 字典模板关键字说明
```shell
定义三种日志输出格式, 日志中可能用到的格式化串如下:
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名
%(funcName)s 调用日志输出函数的函数名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s用户输出的消息
```

## 工具由来
公司经常出现突然一下子来2、3个项目，一个项目需要创建30~40个project的情况。且由于我们用GitLab做的CI/CD，因此需要在每个项目上都设置 "流水线必须成功" 的功能才能允许代码从下游分支合并至上游分支。因此出现了这个自动化工具。

四个步骤：
1、遇到了什么问题？
2、解决问题的思路？
3、解决问题的办法(方法)？
4、总结！




