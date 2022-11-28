#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- Time    : 2022/11/28 13:44:34
# -*- Author  : ayunwSky
# -*- File    : main.py
# -*- Desc    :
# *******************************************


from src.tools import GitLabTools


""" 注意: 需要什么功能就打开注释以调用哪个函数 """
def main():
    # 导入工具类后自动调用 GitLabTools() 方法可以测试工具是否正常执行,可以注释掉
    GitLabTools()

    # 1. 创建子组(GitLab上的顶级组不能通过API创建)
    # GitLabTools().create_git_subgroup()

    # 2. 创建project
    # GitLabTools().create_git_project()

    # 3. 删除 project
    # GitLabTools().delete_git_projects()

    # 4. 删除组(可以删除顶级组和子组)
    # GitLabTools().delete_git_groups()

main()
