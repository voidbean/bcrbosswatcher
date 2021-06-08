# bcrbosswatcher
hoshino插件
通过bigfun读取boss状态, 同时boss切换时进行群内提醒

在hoshino/modules中clone本项目
`git clone https://github.com/voidbean/livewatcher.git`

修改bosswatcher.py中的cookie_str, 内容为你在bigfun上的cookie, 登陆bigfun网页版后,F12打开Console, 输入document.cookie, 将获得的结果给cookie_str即可

在hoshino/config目录下修改__bot__.py, 然后在MODULES_ON中增加`bosswatcher`

启动bot后在需要启动该功能的群内输入`enable bosswathcer`即可
