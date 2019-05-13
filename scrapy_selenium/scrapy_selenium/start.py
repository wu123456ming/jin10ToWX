# from scrapy.cmdline import execute
# execute('scrapy crawl guazi'.split())
import os
import time

if __name__ == '__main__':
# os.system('pwd')
    while True:
        os.system("scrapy crawl jinshirili")
 # 每２个小时执行一次　６０＊６０＊２
        time.sleep(60*60*1)

