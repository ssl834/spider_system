#coding:utf-8
# 接受一个路径进行写文件
def write_files(path,content):
    with open(path,'w',encoding='utf-8') as f:
        f.write(content)
# 接受一个字符串 以filtrate为依据进行格式化
def format_file(datas,filtrate=None):
    content=" "
    for data in datas:

        if data and data!=filtrate:
            content+=data
    return content