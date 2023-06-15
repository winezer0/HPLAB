#  HPLAB And SSGD

```
1 HPLAB -> HTTP Packet Login Auto Brute 基于HTTP报文进行弱口令动态爆破

2 SSDG -> Super Social Dict GEN 基于规则的动态账号密码生成模块
```

## HPLAB

基于HTTP报文进行弱口令动态爆破

为了补充对于常规登录报文需要额外配置的盲点

实现快速对于常规场景进行登录爆破



## 功能说明

输入HTTP报文（自动定位|手动定位） 用户名和密码参数

读取账号密码字典 进行 循环替换和多线程报文重放

## 已实现部分：

```
【已实现】已实现多种请求体类型的参数更新
【已实现】基于报文操作,可使用burp-send-to插件实现直接在burp中调用脚本

【已实现】支持直接输入(用户名:密码对)字典 或编写动态字典规则
【已实现】仅爆破账号$user$、或仅爆破密码 $pass$
【已实现】动态分析爆破是否成功,并支持仅爆破一个账户
【已实现】请求头上的账号密码爆破|不支持自动分析请求头参数,需要手动标记$user$|$pass$

【已实现】发送前对参数值进行额外加密、编码、自定义JS脚本处理、自定义PY脚本处理(标签语法实现)

【已实现】多线程操作
【已实现】日志记录操作
【已实现】增加已爆破账号密码记录功能,不进行重复爆破

【已实现】自动记录已经爆破成功的账号密码,形成自己的口令频率字典
```

## 待实现部分：

```
暂无
```

## 可能实现部分：

```
【暂不实现】绕过csrf
【暂不实现】考虑验证码
```

## 字典文件内容编写规则

参考 [动态规则编写.md](动态规则编写.md)

## 标签语法说明(扩展)

```
语法格式 <md5>字符串</md5>
支持标签 
'b64'        # BASE64编码
'b64s'       # BASE64 URL安全编码
'md5',       # md5加密
'url',       # URL编码
'none',      # 原样返回,用于测试使用
'upper'      # 全部大写
'lower',     # 全部小写
'caper',     # 首字母大写
'js2py'      # 调用自定义Javascript脚本
'mypy'       # 调用自定义Python脚本
'sp4',       # 返回截断前4个字符
'sp6',       # 返回截断前6个字符
'sp8',       # 返回截断前8个字符
'rsp4',      # 返回截断后4个字符
'rsp6',      # 返回截断后6个字符
'rsp8',      # 返回截断后8个字符
'revs'       # 返回字符串的倒序 123456 -> 654321

注意: 
    1、标签语法在http packet处理时,在替换完毕账号密码后再进行处理. 用于密码编码加密场景较多
    1、标签语法在爆破字典生成处理时,在替换%%USERNAME%%变量之前处理. 用于字符串串反序,字符串截断等场景
```
