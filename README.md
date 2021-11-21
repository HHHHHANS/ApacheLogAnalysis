# Apache 日志分析统计

# 总体框架模块：
+ data端（数据获取/格式转换）
+ analysis端（解析）
+ report端（输出报表）
+ tunnel模块（封装消息队列）

data端 --(tunnel模块)--> analysis端 --(tunnel模块)--> report端

# 各模块说明
### agent端：
+ 从本地/服务器获取日志
+ 日志内容安全性检测/解析
+ 读取不同类型的日志文件
+ 对于本地日志文件做大小限制

### tunnel模块：
+ 限制日志内容传输速度/大小
+ 可对transfer两端对接的模块进行配置
+ 

### analysis端：
+ 接收可处理的日志字符串
+ 将日志内容进行解析
+ 

### report端:
+ 从tunnel模块接收解析后的日志信息组成相应形式的报告


# 功能

分析apache日志，给出报表。

要求：
1. 完成“说明”一节中描述的要求；
2. 代码具有良好的可维护、可测试性；
3. 完成单元测试，代码行覆盖率90%以上；
4. 代码符合公司规范要求，代码评级即练习成绩；

## 说明

### 日志格式

```
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/miniprj/material.html HTTP/1.1" 200 38093
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-search-plus/search.css HTTP/1.1" 200 1095
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-disqus/plugin.css HTTP/1.1" 200 63
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-prism/prism-base16-ateliersulphurpool.light.css HTTP/1.1" 200 3290
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/style.css HTTP/1.1" 200 52701
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-anchors/plugin.css HTTP/1.1" 200 608
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-emphasize/plugin.css HTTP/1.1" 200 209
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-expandable-chapters-small/expandable-chapters-small.css HTTP/1.1" 200 580
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-katex/katex.min.css HTTP/1.1" 200 20991
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-splitter/splitter.css HTTP/1.1" 200 503
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-ace/ace.css HTTP/1.1" 200 104
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-donate/plugin.css HTTP/1.1" 200 2720
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-sectionx/sectionx.css HTTP/1.1" 200 376
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-tbfed-pagefooter/footer.css HTTP/1.1" 200 271
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-local-video/video-js.min.css HTTP/1.1" 200 40317
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-anchor-navigation-ex/style/plugin.css HTTP/1.1" 200 1657
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-fontsettings/website.css HTTP/1.1" 200 8596
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/theme.js HTTP/1.1" 200 113099
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-search-plus/search.js HTTP/1.1" 200 8305
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-search-plus/jquery.mark.min.js HTTP/1.1" 200 13390
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook.js HTTP/1.1" 200 105323
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-github/plugin.js HTTP/1.1" 200 388
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-github-buttons/plugin.js HTTP/1.1" 200 3566
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-edit-link/plugin.js HTTP/1.1" 200 859
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-disqus/plugin.js HTTP/1.1" 200 2392
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-ace/ace.js HTTP/1.1" 200 823
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-expandable-chapters-small/expandable-chapters-small.js HTTP/1.1" 200 2058
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-sectionx/sectionx.js HTTP/1.1" 200 1693
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-donate/plugin.js HTTP/1.1" 200 1960
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-fontsettings/fontsettings.js HTTP/1.1" 200 6447
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-splitter/splitter.js HTTP/1.1" 200 3864
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-local-video/video.min.js HTTP/1.1" 200 278740
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-ace/ace/ace.js HTTP/1.1" 200 347010
200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-sharing/buttons.js HTTP/1.1" 200 2875
200.200.76.130 - - [16/Feb/2019:11:27:21 +0800] "GET /coding/gitbook/fonts/fontawesome/fontawesome-webfont.woff2?v=4.6.3 HTTP/1.1" 200 71896
::1 - - [16/Feb/2019:11:27:29 +0800] "OPTIONS * HTTP/1.0" 200 -
200.200.76.130 - - [16/Feb/2019:11:28:16 +0800] "GET /coding/style/%E7%BC%96%E7%A0%81%E9%A3%8E%E6%A0%BC.zip HTTP/1.1" 200 1733226
177.1.81.42 - - [16/Feb/2019:11:28:49 +0800] "GET /designing/tools/image/favicon.ico HTTP/1.1" 404 1221
177.1.81.42 - - [16/Feb/2019:11:28:49 +0800] "GET /designing/tools/image/gitbook/images/favicon.ico HTTP/1.1" 404 1221
177.1.81.42 - - [16/Feb/2019:11:28:54 +0800] "GET /designing/tools/image/UML_classes.docx HTTP/1.1" 200 156676

```

apache服务器所在的地址为200.200.1.35。

### 功能需求

需要滤除css,js等文件的访问，只保留html/htm等页面文件，pdf/doc/docx等文档访问，mpg等媒体类型访问

支持几个子功能，生成3种报表，三种报表格式都采用markdown的表格样式。

#### 1. 文章报表

文章报表样式如下：

| URL  | 文章标题 | 访问人次   | 访问IP数 |
|------|----------|------------|----------|
|/coding/miniprj/material.html | 训练素材 | 20 | 4 |

如果是页面文件，给出页面的标题，其它文件给出文件名即可

#### 2. IP报表

IP报表的样式如下：

| IP  |  访问次数 | 访问文章数 |
|-----|-----------|------------|
| 200.200.76.130 | 40 | 15 |

#### 3. 完整报表

完整报表的样式如下：

| IP   | URL |  访问次数 |
|------|-----|-----------|
|200.200.76.130 | /coding/miniprj/material.html | 3 |
|200.200.76.130|/coding/style/%E7%BC%96%E7%A0%81%E9%A3%8E%E6%A0%BC.zip | 1 |
|177.1.81.42|/designing/tools/image/UML_classes.docx|1|

### 性能要求

1. 日志文件的大小约为300M-1G，要求在30s内分析完毕
2. 分析网页标题需要获取web页面内容，网页内容可以提前从200.200.1.35获取，不计算在分析时间内

### 扩展需求

1. 报表扩展需求，支持更多报表
2. 网页解析扩展，支持提取更多的信息

### 注意事项

1. 注意设计模块对外接口，保证模块后续可供复用，扩展；
2. 注意模块内部划分，保证各子模块相对独立，职责清晰，通过定义明确的接口进行交互；
3. 注意解耦，保证各子模块易于单元测试；
4. 各阶段有明确划分，各阶段输出数据定义清晰，可序列化和反序列化，易于手工构造案例数据进行单元测试；
5. 测试数据可自行模仿样例数据进行构建；
6. 异常处理，当无法连接200.200.1.35，或者获取不到文章标题时，确保程序不卡死，尽可能忽略错误，输出更多可用数据；

