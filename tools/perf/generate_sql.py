from datetime import datetime

# 获取当前时间字符串
current_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")

# 读取并过滤数据
data = []
with open('/home/clay/timetrace.log', 'r') as file:
  i =0
  for line in file:
    if not "MEGAETH" in line:
      continue
    if not "sql" in line:
      continue
    i = i + 1
    print("i:", i)
    start = line.find('sql="') + len('sql="')
    end = line.rfind('"')
    sql_query = line[start:end] + ";\n"
    with open("/home/clay/timetrace.sql", "a") as file:
      file.write(sql_query)
