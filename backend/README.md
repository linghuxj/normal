# 后台文档

## 项目结构

使用的是仿照 Django 项目结构：

- alembic：数据库迁移配置目录
  - versions_dev：开发环境数据库迁移配置文件目录
  - versions_prod：生产环境数据库迁移配置文件目录
  - env.py：映射配置文件
- application：主项目配置目录，也存放了主路由文件
  - config：基础环境配置文件
    - development.py：开发环境
    - production.py：生产环境
  - setting.py：主项目配置文件
  - urls.py：主路由文件
- apps：项目的app存放目录
  - admin：基础服务
    - auth：用户 - 角色 - 菜单接口服务
      - models：ORM 模型目录
      - params：查询参数依赖项目目录
      - schemas：pydantic 模型，用于数据库序列化操作目录
      - utils：登陆认证功能接口服务
      - curd.py：数据库操作
      - view.py：视图函数
- core：核心文件目录
  - crud.py：关系型数据库操作核心封装
  - database.py：关系型数据库核心配置
  - data_types.py：自定义数据类型
  - exception.py：异常处理
  - logger：日志处理核心配置
  - middleware.py：中间件核心配置
  - dependencies.py：常用依赖
  - event.py：全局事件
  - mongo_manage.py：mongodb 数据库操作核心封装
  - validator.py：pydantic 模型重用验证器
- db：ORM 模型基类
- logs：日志目录
- static：静态资源存放目录
- utils：封装工具类目录
- main.py：程序主入口文件
- alembic.ini：数据库迁移配置文件

## 使用

```
# 安装依赖库
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```