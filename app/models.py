from config import *
import pymysql.cursors

conn = pymysql.connect(host='db',user='root',password='',db='FindFolks',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

