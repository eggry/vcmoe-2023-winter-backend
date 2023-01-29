# 小横竖2023冬曲萌后端
## Demo
[Swagger UI](https://xiaohengshu.com/vcmoe-2023-winter/draw.html)
## 配置
程序配置使用环境变量，相关代码见 [config.py](./src/config.py)

- `DATA_DIR`：存放程序数据的目录
- `HOST_UID`：曲萌举办用户的UID
- `HOST_AVID`：曲萌举办视频的av号
- `CORS_ALLOW_ORIGINS`：[CORS策略](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS)

```shell
export DATA_DIR=../data
export HOST_UID=1
export HOST_AVID=10492
```
## 部署
本程序可以部署在各类云服务平台上，如 [Azure App Service](https://azure.microsoft.com/en-us/pricing/details/app-service/windows/)。

您也可以在本地运行该程序
```shell
# clone project
git clone https://github.com/eggry/vcmoe-2023-winter-backend

cd vcmoe-2023-winter-backend

# install packages
pip install -r ./requirements.txt

# run 
./startup.sh
```

## 概述
本项目主要使用 [FastAPI](https://fastapi.tiangolo.com/zh/)开发，主要实现曲萌视频抽签、曲萌投票统计功能。

本程序设计为无状态服务。数据实时从B站收藏夹或评论区解析，在本地仅记录日志，不存储任何永久状态。

```
.
├── main.py      # API
├── bilibili.py  # 获取B站API
├── config.py    # 程序配置
├── election.py  # 投票评论解析
├── seq.py       # 分组、编号
├── storage.py   # 日志
└── utils.py     
```




