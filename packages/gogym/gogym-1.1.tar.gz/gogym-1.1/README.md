# AutoBookingGym
one click is all you need

## 使用方法：
1. 调用 User.save() 保存账号。 
2. 在每天 13:00 调用 go() 函数即可。

## 实现功能
1. 若cookie过期则自动保存cookie
2. 通过全局变量HEADLESS支持浏览器无头模式
3. 增加了parallel.py模块的go()函数支持对所有用户的并行操作
4. 写一个ready文件，再写一个go文件，分批执行。
5. 去掉了日志功能
6. 增加了：“是否打印”功能。
7. 添加日志功能
8. 对log文件只保存前5个，多了就自动放到more里面。
9. 对cookie文件只保存前三个，多了就自动放到more里面。
10. 每个用户用json格式来写
11. 支持检测用户账户密码正不正确
12. 支持无numpy和requests
13. 支持校外访问

整理格式
black . --line-length 200





