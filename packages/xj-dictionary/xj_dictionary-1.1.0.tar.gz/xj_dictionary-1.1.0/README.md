# Xj-Dictionary Module

> 字典模块



# Part 1. Introduce

> 介绍

- 本模块使用M工程化开发文档（MB 311-2022）标准编写

- 本模块采用MSA设计模式（MB 422-2022）



## Install

> 安装

- **依赖**

```shell
# 注：使用pip install django-simple-api会安装不上
pip install git+https://e.coding.net/aber/github/django-simple-api.git@setup.py
```

- **/settings.py**

```python
INSTALLED_APPS = [
    ...,
    "django_simple_api",
    'apps.dictionary.apps.DictionaryConfig',
]
MIDDLEWARE = [
    ...,  
    "django_simple_api.middleware.SimpleApiMiddleware", 
]
```

- **/main/urls.py**

```python
from django.urls import include, re_path
urlpatterns = [
    ...,
    re_path(r'(api/)?dictionary/?', include('apps.dictionary.urls')),
]
urlpatterns += [
    path("docs/", include("django_simple_api.urls"))
]
```





# Part 2. API Document

> API 接口文档



## Chapter 3. Detail Design

> 详细设计



### 3.7 Dictionary 配置类

> 注：配置不建议从接口中添加，前期设计为从后台添加



#### 1、配置添加(dictionary_configure)

- 地址

  ```
  标准	/api/dictionary_configure/		POST
  简写	/api/config/		POST
  ```

- 参数

| 参数        | 名词 | 类型   | 必须 | 默认    | 说明 |
| ----------- | ---- | ------ | ---- | ------- | ---- |
| group       | 分组 | string | 否   | default | -    |
| key         | 键   | string | 是   |         |      |
| value       | 值   | string | 是   |         |      |
| description | 说明 | string | 否   |         |      |



#### 2、配置查找 (dictionary_configure)

- 地址

  ```
  /api/dictionary_configure/<group>		GET
  /api/dictionary_configure/<group>/<key>		GET
  ```

- 参数

  | 参数  | 名词 | 类型   | 必须 | 默认    | 说明             |
  | ----- | ---- | ------ | ---- | ------- | ---------------- |
  | group | 分组 | string | 否   | default | 不传则为默认分组 |


- 返回参数说明

  | 返回参数    | 名称 | 类型   | 说明 |
  | ----------- | ---- | ------ | ---- |
  | key         | 键   | string | 是   |
  | value       | 值   | string | 是   |
  | description | 说明 | string | 否   |

- 返回示例（/api/）

  ```json
  {
      "err": 0,
      "msg": "200 OK",
      "data": {
          "logo":
      }
  }
  ```



#### 2、配置列表 (dictionary_list)

- 地址

  ```
  /api/dictionary_configure_list/		GET
  ```

- 参数

  | 参数  | 名词 | 类型   | 必须 | 默认    | 说明             |
  | ----- | ---- | ------ | ---- | ------- | ---------------- |
  | group | 分组 | string | 否   | default | 不传则为默认分组 |

- 返回参数说明

  | 返回参数    | 名称 | 类型   | 说明 |
  | ----------- | ---- | ------ | ---- |
  | key         | 键   | string | 是   |
  | value       | 值   | string | 是   |
  | description | 说明 | string | 否   |

- 返回示例（/api/）

  ```json
  {
      "err": 0,
      "msg": "200 OK",
      "data": {
          "logo":
      }
  }
  ```


# SQL

```mysql
CREATE TABLE `dictionary_configure` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group` varchar(128) NOT NULL,
  `key` varchar(128) NOT NULL,
  `value` longtext NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `dictionary_configure_group_key_d0e0a692_uniq` (`group`,`key`) USING BTREE,
  KEY `dictionary_configure_group_09d9ee65` (`group`) USING BTREE,
  KEY `dictionary_configure_key_52d53a3c` (`key`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
```










