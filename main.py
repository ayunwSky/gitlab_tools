#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ************************************************
# -*- Author   : ayunwSky
# -*- Time     : 2022/11/14 09:42
# ************************************************


import yaml
import httpx
import gitlab
from logging import config, getLogger

from src.config import settings


# 加载配置
config.dictConfig(settings.LOGGING_DIC)
logger = getLogger("console_log")

class GitLabTools(object):
    """调用GitLab API 进行批量操作"""

    def __init__(self, git_url, git_token, group_id=None):
        self.git_url = git_url
        self.git_token = git_token
        self.namespace_id = group_id
        self.headers = {
            "Content-Type": "application/json",
            "PRIVATE-TOKEN": self.git_token
        }

        try:
            self.client = gitlab.Gitlab(url=self.git_url, private_token=self.git_token, timeout=3)
            # print("连接gitlab成功...")
            logger.info("连接gitlab成功...")
        except Exception as e:
            # print(f"连接gitlab失败,正在尝试重新连接..., message: {e}")
            logger.info(f"连接gitlab失败,正在尝试重新连接..., message: {e}")
            self.client = gitlab.Gitlab(url=self.git_url, private_token=self.git_token, timeout=3)

        with open('./src/config/config.yaml', 'r', encoding='utf-8') as configFile:
            config_data = yaml.safe_load_all(configFile)
            for config in config_data:
                self.config = config

    def create_git_subgroup(self):
        """创建gitlab subgroup"""
        all_groups_list = []
        all_groups = self.client.groups.list(get_all=True)
        for group_name in all_groups:
            all_groups_list.append(group_name.name)

        for subgroup in self.config['create_subgroup_infos']:
            subgroup_name = subgroup['name']
            subgroup_path = subgroup['path']
            parent_id = subgroup['parent_id']
            subgroup_description = subgroup['description']

            payload = {
                "name": subgroup_name,
                "path": subgroup_path,
                "parent_id": parent_id,
                "description": subgroup_description
            }

            if subgroup_name in all_groups_list:
                print(f"计划创建的子组: {subgroup_name} 已经存在,请检查!")
                exit(1)
            else:
                print(f"计划创建的子组: {subgroup_name} 不存在,即将创建!")                
                try:
                    subgroup = self.client.groups.create(payload)
                    payload = {
                        "status_code": 200,
                        "subgroup_id": subgroup.id,
                        "subgroup_name": subgroup.name,
                        "subgroup_full_path": subgroup.full_path,
                        "message": "create subgroup successfully!"
                    }
                    print(payload)
                except Exception as e:
                    payload = {
                        "status_code": 999,
                        "message": e
                    }
                    print(payload)

    def create_git_project(self):
        """ 创建gitlab project """
        group_id = self.config['gitlab_infos']['group_id']
        project_info_list = self.config['create_project_infos']
        group_info_public_list = self.config['group_info_public']

        for project in project_info_list:
            payload = {
                "namespace_id": group_id,
                "name": f"{project['name']}",
                "path": f"{project['name']}",
                "initialize_with_readme": "true",
                "description": f"{project['description']}",
                "visibility": group_info_public_list[0]['visibility'],
                "maintainer": group_info_public_list[0]['project_creation_level'],
                "project_creation_level": group_info_public_list[0]['project_creation_level'],
                "default_branch_protection": group_info_public_list[0]['default_branch_protection']
            }

            try:
                projects_create_resp = self.client.projects.create(payload)
                # print(f'create project: {projects_create_resp.name} successfully!')
                logger.info(f'create project: {projects_create_resp.name} successfully!')
            except Exception as e:
                print(e)

    def delete_git_groups(self):
        """删除gitlab group"""
        delete_group_info_list = self.config['del_group_infos']
        for del_group in delete_group_info_list:
            del_group_id = del_group['id']
            group_api = self.config['gitlab_infos']['gitlab_group_api']
            del_group_api = group_api + str(del_group_id)
            print(del_group_api)

            try:
                del_git_groups_resp = httpx.delete(url=del_group_api, headers=self.headers)
                if del_git_groups_resp.status_code == 404:
                    status = {"status_code": del_git_groups_resp.status_code,
                              "project_url": f"{del_git_groups_resp}",
                              "message": "Group not exist!"
                              }
                    print(status)
                else:
                    status = {"status_code": del_git_groups_resp.status_code,
                              "project_url": f"{del_git_groups_resp}",
                              "message": f"Delete group successfully, group id : {del_group_id}"
                              }
                    print(status)
            except Exception as e:
                print(e)

    def delete_git_projects(self):
        """根据project id来删除gitlab project"""
        del_projects_info_list = self.config['del_project_infos']
        for del_project in del_projects_info_list:
            del_project_id = del_project['id']
            project_api = self.config['gitlab_infos']['gitlab_project_api']
            del_project_api = project_api + str(del_project_id)

            try:
                del_git_project_resp = httpx.delete(url=del_project_api, headers=self.headers)
                if del_git_project_resp.status_code == 404:
                    status = {"status_code": del_git_project_resp.status_code,
                              "project_url": f"{del_project_api}",
                              "message": "Delete project successfully!"
                              }
                    print(status)
                else:
                    status = {"status_code": del_git_project_resp.status_code,
                              "project_url": f"{del_project_api}",
                              "message": f"This project have been delete, project id : {del_project_id}"
                              }
                    print(status)
            except Exception as e:
                print(e)

    def main(self):
        """ 入口函数，不开启功能函数调用的话,该工具不进行任何操作 """

        print("入口函数!")
        print()
        # print(f"配置文件信息: {self.config}")

        # 功能函数调用
        # self.create_git_subgroup()
        # self.create_git_project()
        # self.delete_git_projects()
        # self.delete_git_groups()


if __name__ == "__main__":
    with open("./src/config/config.yaml", 'r', encoding='utf-8') as configFile:
        data = yaml.safe_load_all(configFile)
        for conf in data:
            git_url = conf["gitlab_infos"]["gitlab_url"]
            git_token = conf["gitlab_infos"]["gitlab_token"]

    api_tools = GitLabTools(git_url=git_url, git_token=git_token)
    api_tools.main()
