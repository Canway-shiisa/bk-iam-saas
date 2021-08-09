# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-权限中心(BlueKing-IAM) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import logging
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from django.utils.translation import gettext as _
from pydantic import BaseModel
from pydantic.tools import parse_obj_as

from backend.common.error_codes import APIException, error_codes
from backend.service.models import (
    ResourceAttribute,
    ResourceAttributeValue,
    ResourceInstanceBaseInfo,
    ResourceInstanceInfo,
)
from backend.service.resource import ResourceProvider

logger = logging.getLogger(__name__)


class ResourceAttributeBean(ResourceAttribute):
    pass


class ResourceAttributeValueBean(ResourceAttributeValue):
    pass


class ResourceInstanceBaseInfoBean(ResourceInstanceBaseInfo):
    pass


class ResourceInfoBean(ResourceInstanceInfo):
    def get_attr(self, attr: str) -> Any:
        """获取某个属性值"""
        return self.attributes.get(attr) or None

    def list_attr(self) -> Dict[str, Any]:
        return self.attributes


class ResourceInfoDictBean(BaseModel):
    data: Dict[str, ResourceInfoBean]

    def has(self, _id: str) -> bool:
        return _id in self.data

    def get_attributes(self, _id: str, ignore_none_value=False):
        """默认忽略属性里的None值"""
        attrs = self.data[_id].list_attr()
        return {k: v for k, v in attrs.items() if not ignore_none_value or v is not None}


class ResourceNodeBean(BaseModel):
    system_id: str
    type: str
    id: str

    def __hash__(self):
        return hash((self.system_id, self.type, self.id))

    def __eq__(self, other):
        return self.system_id == other.system_id and self.type == other.type and self.id == other.id


class ResourceNodeNameDictBean(BaseModel):
    data: Dict[ResourceNodeBean, str]

    def has(self, system_id: str, _type: str, _id: str):
        return ResourceNodeBean(system_id=system_id, type=_type, id=_id) in self.data

    def get_name(self, system_id: str, _type: str, _id: str):
        """获取资源实例名称"""
        return self.data.get(ResourceNodeBean(system_id=system_id, type=_type, id=_id), None)


class ResourceBiz:
    """资源实例各种业务场景的调用"""

    def new_resource_provider(self, system_id: str, resource_type_id: str):
        return ResourceProvider(system_id, resource_type_id)

    def list_attr(self, system_id: str, resource_type_id: str) -> List[ResourceAttributeBean]:
        """查询某个资源类型可用于配置权限的属性列表"""
        rp = self.new_resource_provider(system_id, resource_type_id)
        attrs = rp.list_attr()
        return parse_obj_as(List[ResourceAttributeBean], attrs)

    def list_attr_value(
        self, system_id: str, resource_type_id: str, attr: str, keyword: str = "", limit: int = 10, offset: int = 0
    ) -> Tuple[int, List[ResourceAttributeValueBean]]:
        """获取一个资源类型某个属性的值列表"""
        rp = self.new_resource_provider(system_id, resource_type_id)
        count, results = rp.list_attr_value(attr, keyword, limit, offset)
        return count, parse_obj_as(List[ResourceAttributeValueBean], results)

    def list_instance_for_topology(
        self,
        system_id: str,
        resource_type_id: str,
        parent_type: str = "",
        parent_id: str = "",
        limit: int = 10,
        offset: int = 0,
    ) -> Tuple[int, List[ResourceInstanceBaseInfoBean]]:
        """拓扑树的场景下，根据上级资源获取某个资源实例列表"""
        rp = self.new_resource_provider(system_id, resource_type_id)
        count, results = rp.list_instance(parent_type, parent_id, limit, offset)
        return count, parse_obj_as(List[ResourceInstanceBaseInfoBean], results)

    def search_instance_for_topology(
        self,
        system_id: str,
        resource_type_id: str,
        keyword: str,
        parent_type: str = "",
        parent_id: str = "",
        limit: int = 10,
        offset: int = 0,
    ) -> Tuple[int, List[ResourceInstanceBaseInfo]]:
        """拓扑树的场景下，根据上级资源和Keyword搜索某个资源实例列表"""
        rp = self.new_resource_provider(system_id, resource_type_id)
        count, results = rp.search_instance(keyword, parent_type, parent_id, limit, offset)
        return count, parse_obj_as(List[ResourceInstanceBaseInfoBean], results)

    def fetch_auth_attributes(
        self, system_id: str, resource_type_id: str, ids: List[str], raise_api_exception=False
    ) -> ResourceInfoDictBean:
        """查询所有资源实例的用于鉴权的属性，同时如果查询有问题，则直接忽略错误"""
        rp = self.new_resource_provider(system_id, resource_type_id)

        # 鉴权属性，需要包括拓扑路径，这种由权限中心产生的
        # TODO: _bk_iam_path_ 需要提取为常量，目前多处都直接裸写
        attrs = ["_bk_iam_path_"]
        # 查询支持该资源类型配置的属性
        try:
            resource_attrs = rp.list_attr()
            attrs.extend([i.id for i in resource_attrs])
        except APIException as error:
            logging.info(
                f"fetch_resource_all_auth_attributes({system_id}, {resource_type_id}) list_attr error: {error}"
            )
            # 判断是否忽略接口异常
            if raise_api_exception:
                raise error

        # 查询资源实例的属性
        try:
            resource_infos = rp.fetch_instance_info(ids, attrs)
        except APIException as error:
            logging.info(
                f"fetch_resource_all_auth_attributes({system_id}, {resource_type_id}) "
                f"fetch_instance_info error: {error}"
            )
            # 不需要抛异常则直接返回
            if not raise_api_exception:
                return ResourceInfoDictBean(data={})
            raise error

        return ResourceInfoDictBean(data={i.id: ResourceInfoBean(**i.dict()) for i in resource_infos})

    def fetch_resource_name(
        self, resource_node_beans: List[ResourceNodeBean], raise_not_found_exception=False
    ) -> ResourceNodeNameDictBean:
        """获取资源实例名称, 默认查询不到的资源不会有异常"""
        resource_name_dict: Dict[ResourceNodeBean, str] = {}

        # 按system_id、resource_type_id 分组批量查询
        resource_ids_dict = defaultdict(list)
        for r in resource_node_beans:
            # 任意实例不需要查询
            if r.id == "*":
                resource_name_dict[ResourceNodeBean(system_id=r.system_id, type=r.type, id=r.id)] = _("无限制")
                continue
            # 需要查询的实例，添加到对应资源类型分组里
            resource_ids_dict[(r.system_id, r.type)].append(r.id)

        # 查询
        for k, ids in resource_ids_dict.items():
            system_id, resource_type_id = k
            # 接口查询
            rp = self.new_resource_provider(system_id, resource_type_id)
            resource_instance_base_infos = rp.fetch_instance_name(ids)
            # 遍历返回的数据
            for r in resource_instance_base_infos:
                resource_node = ResourceNodeBean(system_id=system_id, type=resource_type_id, id=r.id)
                resource_name_dict[resource_node] = r.display_name

        name_dict_bean = ResourceNodeNameDictBean(data=resource_name_dict)

        # 默认对于查询不到的资源实例Name，需要抛异常
        if raise_not_found_exception:
            # 校验每个资源是否都能查询到对应的资源Name
            for r in resource_node_beans:
                if not name_dict_bean.has(r.system_id, r.type, r.id):
                    raise error_codes.INVALID_ARGS.format(
                        "The resource(system_id:{}, type:{}, id:{}) display_name cannot be "
                        "queried through the API - fetch_instance_info".format(r.system_id, r.type, r.id)
                    )

        return name_dict_bean
