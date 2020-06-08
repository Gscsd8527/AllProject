import re
mysr = '谭振华1233fggf dfds 2332打的 '
re_com = re.compile('(\d.*?)\D')
data = re.findall(re_com, mysr)
print(data)