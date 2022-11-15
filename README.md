# gitlab-tools
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

## 不允许使用API创建顶级组
```shell
创建顶级组不被允许,详情参考以下：
https://docs.gitlab.com/ee/api/groups.html#new-group
https://github.com/python-gitlab/python-gitlab/issues/2372
https://github.com/python-gitlab/python-gitlab/pull/2374/commits/6bf25a8766558ded0c9a3dd1a7111b2a1c9f4837
```

后续功能 包括不限于：自动勾选流水线必须成功以及commit规范的hooks钩子,这两项功能目前有待开发...
