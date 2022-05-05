# efb-solitaire_optimize-middleware
将群组信息里面的接龙信息简洁化

目前只能一时间处理一个接龙，有需求的话后期会优化

具体功能展现形式为：

1、一个接龙信息只会在一条信息上更新 (每个群**只处理最新的一个接龙**）

2、使用 ``` jl` ``` +名字**回复一条接龙信息进行接龙**

>例：```jl` 张三```

使用方法：

1、把`solitaire.py`放入EFB目录下的`modules/`中

2、在EFB目录下`profiles/default/config.yaml`文件中添加

```
middlewares:
  - solitaire.MatrixLauMiddleware
```

3、在`solitaire.py`中`solitaire_keyword`字典中添加接龙关键词（因为不同语言登录的Wechat提示的信息都不一样，目前加了简中跟繁中的）
