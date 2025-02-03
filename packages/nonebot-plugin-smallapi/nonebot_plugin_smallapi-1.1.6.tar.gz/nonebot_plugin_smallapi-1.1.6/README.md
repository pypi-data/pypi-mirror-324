<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://v2.nonebot.dev/logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
</div>

<div align="center">

# nonebot_plugin_smallapi

_✨ 高效，快速的小小WEBAPI调用插件！ ✨_


<a href="https://github.com/chaichaisi/nonebot_plugin_smallapi/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/chaichaisi/nonebot_plugin_smallapi?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/chaichaisi/nonebot_plugin_smallapi/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/chaichaisi/nonebot_plugin_smallapi?color=Emerald%20green&style=flat-square">
</a>
<a href="https://github.com/chaichaisi/nonebot_plugin_smallapi/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/chaichaisi/nonebot_plugin_smallapi?color=%2300BFFF&style=flat-square">
</a>
<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/chaichaisi/nonebot_plugin_smallapi.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_smallapi">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_smallapi.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
</a>

</div>

## 🙏 致谢

感谢大佬[lgc2333](https://github.com/lgc-NB2Dev/)提供借鉴源代码
[借鉴的代码](https://github.com/lgc-NB2Dev/ShigureBot/blob/main/src/plugins/shigure_bot/plugins/site_tool/__main__.py)

## 📖 前言及介绍

PS: 这是我第一次写(划掉，是借鉴去ctrlcv！详见最下方致谢)插件，没有多少经验，写的也不规范，如果介意可以不用，望多多关照～(如果可以，给个star)  
不要喷我～这个插件大佬5分钟就能搓出来……我是为了那些想写插件但是不会写的人群而写的这个插件，你可以随便借鉴，没什么精髓，只要标明致谢就好了～(╥╯^╰╥)  
这个插件主要功能是调用WEBAPI链接获取数据处理后发到QQ里面的，目前统一使用json调用并解析，有问题记得issues！

## 🔧 开发环境
Nonebot2：2.0.0rc4  
python：3.11.3  
操作系统：Linux（Windows兼容性问题不大）  
编辑器：VS Code

## 💿 安装  

### 1. nb-cli安装（推荐）

在你bot工程的文件夹下，运行cmd/shell（运行路径要对啊），执行nb命令安装插件，插件配置会自动添加至配置文件  
```
nb plugin install nonebot_plugin_smallapi
```

### 2. pip安装
```
pip install nonebot_plugin_smallapi
```  
打开 nonebot2 项目的 ```bot.py``` 文件, 在其中写入  
```nonebot.load_plugin('nonebot_plugin_smallapi')```  
当然，如果是默认nb-cli创建的nonebot2的话，在bot路径```pyproject.toml```的```[tool.nonebot]```的```plugins```中添加```nonebot_plugin_smallapi```即可  
pyproject.toml配置例如：  
``` 
[tool.nonebot]
plugin_dirs = ["src/plugins"]
plugins = ["nonebot_plugin_smallapi"]
``` 

### 3. 本地安装(不推荐)

仓库没更新，建议nb-cli
将项目clone到你的机器人插件下的对应插件目录内（一般为机器人文件夹下的`src/plugins`），然后把`nonebot_plugin_smallapi`文件夹里的内容拷贝至上一级目录即可。  
clone命令参考（得先装`git`，懂的都懂）：
```
git clone https://github.com/chaichaisi/nonebot_plugin_smallapi.git
``` 
也可以直接下载压缩包到插件目录解压，然后同样提取`nonebot_plugin_smallapi`至上一级目录。  
目录结构： ```你的bot/src/plugins/nonebot_plugin_smallapi/__init__.py```  

### 更新版本
```
nb plugin update nonebot_plugin_smallapi
```

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| smallapi_token | 否 | 空 | [故梦API](https://www.gmya.net/api)的调用KEY |

例如.env.prod :
```
...
smallapi_token="qwer1234114514"
#不可以填纯数字哈，不可以没有""哈，除非你闲的没事a.e
#密钥获取网址: https://www.gmya.net/api
```
不填写也能用，但是有调用限制哈！


## 🎉 功能
  
  1. 齐全的API随机图片系统  
  2. 齐全的API随机文本系统  
  3. 好使的网站工具系统

## 👉 命令
  
  PS: 请查看你env中起始符的配置(默认```/```)  
  1. API图片系统(图片系统)  
  2. API文字系统(文字系统)
  3. API站点系统(站点系统)

### API图片系统
命令结构：```(/)API图片系统```  
例如：```API图片系统```  

### API文字系统
命令结构：```(/)API文字系统```  
例如：```API文字系统```  

### API站点系统
命令结构：```(/)API站点系统```  
例如：```API站点系统```

## ⚙ 拓展
 
 还没有呢～

## 📝 更新日志

<details>
<summary>展开/收起</summary>

<<<<<<< HEAD
<<<<<<< HEAD
### 1.0.0

=======
### 1.1.5
=======
### 1.1.5

- 调用地址更新  
- 增加故梦的appkey调用方法  
- 此版本未修复部分功能的兼容性问题，如需使用请提交Issus！  

### 1.1.0

- 站点代码重写更新  

### 1.0.7

- 优化更新  

### 1.0.6

- 维护更新，蟒蛇(Python)版本要求最低改为3.10  

### 1.0.5

- 修复ip查询中的致命语法错误  

### 1.0.4

- 更换稳定API, 修复部分Bug  

### 1.0.3  
  
- 梅开三度，终于修好了依赖  

### 1.0.2
  
- 梅开二度. 

### 1.0.1

- 修复依赖问题  

### 1.0.0

- 插件初次发布
>>>>>>> 0578ffb5897abb55ffea079f5f82e5c79261e17a

- 调用地址更新  
- 增加故梦的appkey调用方法  
- 此版本未修复部分功能的兼容性问题，如需使用请提交Issus！  

### 1.1.0

- 站点代码重写更新  

### 1.0.7

- 优化更新  

### 1.0.6

- 维护更新，蟒蛇(Python)版本要求最低改为3.10  

### 1.0.5

- 修复ip查询中的致命语法错误  

### 1.0.4

- 更换稳定API, 修复部分Bug  

### 1.0.3  
  
- 梅开三度，终于修好了依赖  

### 1.0.2
  
- 梅开二度. 

### 1.0.1

- 修复依赖问题  

### 1.0.0

>>>>>>> 0578ffb5897abb55ffea079f5f82e5c79261e17a
- 插件初次发布

### 1.0.1

- 修复依赖问题  

### 1.0.2
  
- 梅开二度  
  
### 1.0.3  
  
- 梅开三度，终于修好了依赖

### 1.0.4

- 更换稳定API, 修复部分Bug

### 1.0.5

- 修复ip查询中的致命语法错误

### 1.0.6

- 维护更新，蟒蛇(Python)版本要求最低改为3.10

### 1.0.7

- 优化更新

### 1.1.0

- 站点代码重写更新
</details>

## 致谢
- [借鉴的代码](https://github.com/lgc-NB2Dev/ShigureBot/blob/main/src/plugins/shigure_bot/plugins/site_tool/__main__.py)
- [nonebot-plugin-template](https://github.com/A-kirami/nonebot-plugin-template)
