# -*- coding: UTF-8 -*- 
import os  
  
path='/Users/mianmian/Study/Python/shuzi.txt'  
  
dirpath=os.path.splitext(path)  
  
if not os.path.exists(dirpath):   #判断是否存在新文件夹，否则创建  
    os.mkdir(dirpath)