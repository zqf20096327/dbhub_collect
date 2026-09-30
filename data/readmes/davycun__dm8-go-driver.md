### 说明
这个是项目是达梦的go驱动程序，只是为了依赖管理方便，仅供学习参考。是从对应安装版本的drivers目录下拷贝出来的。

### 变更
- 增加了readme.md
- 为了能在macos中运行，在security包下复制了一份zzg_linux.go 为zzg_darwin.go 
- 修改了模块名为github.com/davycun/dm8-go-driver，其中v8对应的是dm8
- 把go的版本从1.13升级为了1.24.0

### 版本说明
- 从VERSION文件或者p.go文件中可以看到对应的数据库版本，比如8.1.4.48，在这里release版本修改为v1.4.48，最前面的8用模块路径中dm8代表
- 如果想要下载数据库版本8.1.4.48对应的go驱动，可以执行go get github.com/davycun/dm8-go-driver@v1.4.48