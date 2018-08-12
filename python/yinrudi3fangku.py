#coding=utf-8
#引人第三方库
import sys#导入sys模块，因此接下来可以访问sys模块的所有功能
def test():
	args=sys.argv#sys模块有一个argv变量，用list存储了命令行的所有参数。argv至少有一个元素，因为第一个参数永远是该.py文件的名称，例如：运行python3 hello.py获得的sys.argv就是['hello.py']；运行python3 hello.py Michael获得的sys.argv就是['hello.py', 'Michael]。
 if _name_=='_main_':
 	test()