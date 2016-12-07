#-*-coding:utf8-*-
import requests
import re
import multiprocessing

def main_url(url):                  #获取详情页面url
    url_list = []
    report = requests.get(url)

    limit1 = r"http://war3.uuu9.com/Soft/2016(.+?)\""
    for url_last in re.findall(limit1, report.content, re.DOTALL):
        the_url = "http://war3.uuu9.com/Soft/2016"+url_last
        url_list.append(the_url)
    set(url_list)
    url_list.remove("http://war3.uuu9.com/Soft/201604/38079.shtml")
    return url_list

class U9w3x():

    def __init__(self, First_url):
        self.First_url = First_url
        self.u9_down = requests.session()
    
    def down_url(self):                #获取真实下载链接 传入详情页面
        report = self.u9_down.get(self.First_url)
        limit1 = r"iframe marginheight=\"0\" id=\"iframe\" src=\"(.+?)\"  frameborder"
        url_down = re.findall(limit1, report.content, re.DOTALL)
        if not url_down:
            print "no url"
            return
        url_down = url_down[0]
        
        down_report = self.u9_down.get(url_down)
        limit2 = r"href=\"http://war3down1.uuu9.com/war3(.+?)\">"
        download = re.findall(limit2, down_report.content, re.DOTALL)
        s = re.sub(r"/(.+?)/","",download[0])
        print "文件为:", s
        download = "http://war3down1.uuu9.com/war3"+download[0]

        
        r = self.u9_down.get(download)
        with open(s, "wb") as code:
            code.write(r.content)

def down(url):
    U9_w3xdown = U9w3x(url)
    U9_w3xdown.down_url()

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=8)
    url_list = main_url("http://war3.uuu9.com/")
    
    for url in url_list:
        pool.apply_async(down, args=(url,))
    pool.close()
    pool.join()
