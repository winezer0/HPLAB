# AutoLoginPacketBrute

基于HTTP报文进行弱口令动态爆破

为了补充对于常规登录报文需要额外配置的盲点

## 功能说明

输入HTTP报文（自动定位|手动定位） 用户名和密码参数

读取账号密码字典 进行 循环替换和多线程报文重放

## 已实现部分：

```
【已实现】已实现多种请求体类型的参数更新
【已实现】基于报文操作,可使用burp-send-to插件实现直接在burp中调用脚本

【已实现】支持直接输入(用户名:密码对)字典
【已实现】仅爆破账号$user$、或仅爆破密码 $pass$
【已实现】动态分析爆破是否成功,并支持仅爆破一个账户

【已实现】可直接使用常规的目录字典进行爆破
【已实现】增加账号字典、密码字典动态变量支持,具体写法参考 参考 [动态规则编写.md] 

【已实现】中文账号密码编码问题
【已实现】中文账号变形处理
【已实现】发送前对参数值进行额外加密、编码
【已实现】优化用户名变量的替换过程  扩展出 大小写

【已实现】最终账号密码格式筛选

【已实现】多线程操作
【已实现】日志记录操作
【已实现】增加已爆破账号密码记录功能,不进行重复爆破

```

## 待实现部分：

```
【实现中】字典规则整理
```

## 放弃实现部分：

```
【未实现】请求头上的账号密码爆破
【不实现】绕过csrf
【不实现】考虑验证码
```

## 字典文件内容编写规则

参考 [动态规则编写.md](动态规则编写.md)

