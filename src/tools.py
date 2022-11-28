#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# *******************************************
# -*- Time    : 2022/11/28 13:45:29
# -*- Author  : ayunwSky
# -*- File    : tools.py
# *******************************************


import yaml
import httpx
import gitlab
from pathlib import Path

from logging import config, getLogger

from src.config import settings


# 加载配置
config.dictConfig(settings.LOGGING_DIC)
logger = getLogger("console_log")


class GitLabTools(object):
    """调用GitLab API 进行批量操作"""

    def __init__(self):
        """ 直接打开配置文件,在这里就初始化好需要的配置参数 """
        # print('GitLabTools 初始化完成...', end='')
        logger.info('GitLabTools 初始化完成...')

        BASE_DIR = Path(__file__).resolve().parent.parent
        config_file_path = BASE_DIR / 'src/config/config.yaml'

        with open(config_file_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load_all(f)
            for config in config_data:
                self.config = config

        self.git_url = self.config["gitlab_infos"]["gitlab_url"]
        self.git_token = self.config["gitlab_infos"]["gitlab_token"]
        self.namespace_id = self.config["gitlab_infos"]["group_id"]
        self.headers = {
            "Content-Type": "application/json",
            "PRIVATE-TOKEN": self.git_token
        }

        try:
            self.client = gitlab.Gitlab(url=self.git_url, private_token=self.git_token, timeout=3)
            # print("连接 GitLab 成功!")
            logger.info("连接 GitLab 成功!")
            print()
        except Exception as e:
            # print(f"连接 GitLab 失败,正在尝试重新连接, message: {e}!")
            logger.info(f"连接 GitLab 失败,正在尝试重新连接, message: {e}!")
            # print()
            self.client = gitlab.Gitlab(url=self.git_url, private_token=self.git_token, timeout=3)

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
                logger.info(f"计划创建的子组: {subgroup_name} 已经存在,请检查!")
                exit(1)
            else:
                # print(f"计划创建的子组: {subgroup_name} 不存在,即将创建!")
                logger.info(f"计划创建的子组: {subgroup_name} 不存在,即将创建!")

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
                    payload = {"status_code": 999, "message": e}
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
                name = project['name']
                # print(f'project [{name}] has been created,', e)
                logger.info(f'project [{name}] has been created,', e)

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
                    status = {
                        "status_code": del_git_groups_resp.status_code,
                        "project_url": f"{del_git_groups_resp}",
                        "message": "Group not exist!"
                    }
                    print(status)
                else:
                    status = {
                        "status_code": del_git_groups_resp.status_code,
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
            del_project_name = del_project['name']
            project_api = self.config['gitlab_infos']['gitlab_project_api']
            del_project_api = project_api + str(del_project_id)

            try:
                del_git_project_resp = httpx.delete(url=del_project_api, headers=self.headers)

                if del_git_project_resp.status_code != 404:
                    status = {
                        "status_code": del_git_project_resp.status_code,
                        "project_name": del_project_name,
                        "project_url": f"{del_project_api}",
                        "message": "Delete project successfully!"
                    }
                    print(status)
                else:
                    status = {
                        "status_code": del_git_project_resp.status_code,
                        "project_name": del_project_name,
                        "project_url": f"{del_project_api}",
                        "message": f"This project has been deleted before, project id : {del_project_id}"
                    }
                    print(status)
            except Exception as e:
                print(e)
