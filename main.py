from analysis.parser import ApacheLog_V_1_1
from report.statistic import ApacheLogReporter
import time

# 读取本地日志文件
f = open('agent/resource/large_log_10m.log', 'r', encoding='utf-8')
content = f.readlines()
print(len(content))
f.close()

times = 1

start = time.time()
for i in range(times):
    # 初始化日志解析类并解析
    print(i)
    parser = ApacheLog_V_1_1()
    parser.parse(content)
    parse_res = parser.result()

    # 初始化日志统计类
    statistic_er = ApacheLogReporter()
    statistic_er.parser_content_2_statistic(parse_res)
    # 生成-文章报表
    article_rep = statistic_er.article_report()
    # 生成-ip报表
    ip_rep = statistic_er.ip_report()
    # 生成-完整报表
    com_rep = statistic_er.complete_report()
    print(article_rep)
    print()
    print(ip_rep)
    print()
    print(com_rep)
    print()

end = time.time()
print(round(end - start, 3), ' s')

