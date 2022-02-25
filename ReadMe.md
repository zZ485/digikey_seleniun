# DigiKey & Arrow平台自动爬虫
 
------
 
这是一个适用于**DigiKey**(德捷)和**Arrow**电子元件电商平台，获取库存信息，在库存达到用户要求时，可以向用户指定邮箱发送邮件的系统

>这是一个纯Python爬虫的项目

### 项目所需要的Python第三方库和驱动
 
- Selenium v4.1.0
- chromedriver v98.0.4758.102
- google chrome v98.0.4758.102

>用户可以通过更改**config.json**和**GoodList.txt**中的内容改变程序中的参数.<br>
>(注：GoodList.txt中只需要放入需要获取元件的系列号)


####程序的入口是main.py,启动项目时，浏览器会自动开启。<br><br>

##项目实现24小时监控，其中每30分钟进行一次扫描