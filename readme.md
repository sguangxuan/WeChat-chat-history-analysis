# 微信聊天记录分析

## 聊天记录按好友导出至excel脚本

1. 手机->设置->更多设置->备份和重置->本地备份，备份微信APP。将 MIUI/backup/ALLBackup/yyyymmdd_xxxxxx/ 文件夹下的 com.tecent.mm.bak拷贝至电脑，使用解压软件7-zip直接对 com.tecent.mm.bak进行解压。
2. 在文件 com.tecent.mm\apps\com.tencent.mm\sp\ auth_info_key_prefs.xml中获取微信uin码，标识name=int_value。获取手机IMEI码（小米隐匿模式可能是123456789ABCDE）。
3. 获得数据库密码。将IMEI和uin拼接，用MD5加密（32位），取前7位字母小写就是数据库的密码(d8f3a1b)。
4. 使用数据库密码，通过sqlicipher软件打开com.tecent.mm\apps\com.tencent.mm\r\MicroMsg\xxxx\EnMicroMsg.db数据库文件，将message、rcontect表导出到csv。
5. 在根目录下创建文件夹`save`，运行脚本`聊天记录按好友导出csv.py`（注意修改`addr`变量，将路径写至第4步数据库导出的csv），导出的聊天记录会保存至save文件夹下。

## 聊天记录截屏与拼接

1. 电脑端需要安装安卓adb工具，并设置path变量。（cmd命令：`adb version`）
2. 手机中创建`/sdcard/临时/screen/`目录用来存放截图
3. 运行`微信聊天记录截图.py`，注意修改`savedir`变量，截图将去掉头部和尾部后，存至`savedir`目录中。
4. 运行`截图合成.py`脚本，将图片拼接后重新分割，新分割的图片将不会有重叠，可选增加图片头尾，需要提前准备`head.png`和`tail.png`头尾图片文件。