## Note


linux kernel development  
```
第6章 内核数据结构 6.1， 6.2小节
第7章 中断和中断处理
第8章 下半部和推后执行的工作
第9章 内核同步介绍
第10章 内核同步方法
第12章 内存管理，12.1—12.7小节
第18章 调试
第19章 可移植性
Cis函数的cis_dev_call，也是抄的linux sensor驱动思路。
推荐再阅读一个简单的网卡驱动stmmac_main.c，了解下基本驱动写法和技巧。目前isp firmware驱动，比如isp_core_call，isp_device_call之类，很多思路也是抄的或者类似的。熟悉了内核的module_init之类的init section方法和原理，看到isp_core_call肯定是秒懂，根本不用思考。
```
#### [stmmac网卡驱动源码解读](https://blog.csdn.net/heliangbin87/article/details/75997189)

#### [const总结](https://blog.csdn.net/xingjiarong/article/details/47282255)
#### [Java面试题总结](https://blog.csdn.net/qq_40949465/category_8786155.html)
#### [Java单例模式](https://www.cnblogs.com/lyw-hunnu/p/12576345.html)
#### [Java之美[从菜鸟到高手演变]系列之博文阅读导航](https://blog.csdn.net/zhangerqing/article/details/8245560) 
#### [python 模块大全](https://blog.csdn.net/hanzihan123/article/details/41898643)


#### [如何系统地学习Python 中 matplotlib, numpy, scipy, pandas？](https://www.zhihu.com/question/37180159)

#### [python 自动化测试](http://blog.csdn.net/carolzhang8406/article/details/51601937)

#### [python selenium](http://www.cnblogs.com/fnng/p/3258946.html)

#### [python](http://www.cnblogs.com/fnng/category/454439.html)

#### [tensorflow 中文社区](http://www.tensorfly.cn/)

#### [wxpythonbuilder简单实用，构建图形界面](http://yuyongid.blog.51cto.com/10626891/1717514)
#### [wxpython——yibaipython教程](http://www.yiibai.com/wxpython/)

#### [如何优雅地使用 Sublime Text](http://blog.jobbole.com/95933/)
#### [百度地图创建地图](http://api.map.baidu.com/lbsapi/creatmap/)

#### [C++ 趣图](https://pic4.zhimg.com/51e24922e946c197859ff2bca752da97_r.jpg)
#### [搜索盘](http://www.sosuopan.com/file/108016)
#### [国外程序员整理的 C++ 资源大全](http://www.csdn.net/article/2014-10-24/2822269-c++)
#### [A curated list of awesome C/C++ frameworks, libraries, resources, and shiny things.](https://github.com/fffaraz/awesome-cpp)

#### [别瞎扯淡了，说重点](https://www.zhihu.com/question/20632491)

#### [W3School 后台教程](http://www.ctolib.com/docs//sfile/w3school-back-end/index.html)

#### [python django ](https://borisliu.gitbooks.io/from-python-to-django/content/)

#### [Android上打包jar并在真机上运行](http://blog.csdn.net/zhuvery/article/details/78011345)

#### [疫苗注射选择](https://mp.weixin.qq.com/s?__biz=MzI0NzE0MDcyMA==&mid=2650692626&idx=1&sn=051c86544ba0cb73e5ed5bc2be0f0fef&chksm=f1be640dc6c9ed1b66778c504f1d858bca45cf742d7bee0184a82fe9411c7ebc9196e0cf412e&scene=4#wechat_redirect)

#### Python网络数据采集 Django自学教程
#### [github pop java star](https://github.com/trending?l=java&since=monthly)

#### [网盘地址 python boot recommend](https://pan.baidu.com/s/15S0QQwIxIqyZ5PjKZRHPuQ)  密码：237a

```
main()
{
	mkdir sdcard/isp_log
	mkdir sdcard/hilogs
	mkdir sdcard/kmsgcat_log
	mkdir sdcard/tombstone
	while :
	do
		curdate=$(date +'%Y%m%d%H%M%S')
		echo $curdate
		for index in $(seq 1 25)  
		do	
			mv /data/vendor/log/isp-log/isp-log-$index.tar.gz /sdcard/isp_log/isp-log-$curdate-$index.tar.gz &> /dev/null
			rm /data/vendor/log/isp-log/isp-log-$index.tar.gz
			mv /data/log/android_logs/applogcat-log-$index.tar.gz /sdcard/applogcat_log/applogcat-log-$curdate-$index.tar.gz &> /dev/null
			rm /data/log/android_logs/applogcat-log-$index.tar.gz
			mv /data/log/android_logs/kmsgcat-log-$index.tar.gz /sdcard/kmsgcat_log/kmsgcat-log-$curdate-$index.tar.gz &> /dev/null
			rm /data/log/android_logs/kmsgcat-log-$index.tar.gz
			mv /data/log/hilogs/kmsgcat-log-$index.tar.gz /sdcard/kmsgcat_log/kmsgcat-log-$curdate-$index.tar.gz &> /dev/null
			rm /data/log/hilogs/kmsgcat-log-$index.tar.gz
			mv /data/tombstones/tombstone_0$index /sdcard/tombstones/tombstone-$curdate_0$index &> /dev/null
			rm /data/tombstones/tombstone_0$index
		done
		mv /data/log/hilogs/hiapplogcat-log.*.*.gz /sdcard/hilogs/ &> /dev/null
		sleep 100
	done
}

main
```
