#-*- coding=utf-8 -*-
'''
Created on 2019年7月22日
@author: hanbian
'''
import hashlib
import json

import requests
import urllib
import base64


def image():
    f = open(r'C:\Users\hanbian\Pictures\Camera Roll\1.jpg', 'rb')  # 二进制方式打开图文件
    md = hashlib.md5()
    data = f.read()
    md.update(data)
    res1 = md.hexdigest()
    print(res1)
    ls_f = base64.b64encode(data)  # 读取文件内容，转换为base64编码
    print(ls_f)


    f.close()



# image()

def getSogouImag(category, length, path):
    n = length
    cate = category
    imgs = requests.get(
        'http://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category=' + cate + '&tag=%E5%85%A8%E9%83%A8&start=0&len=' + str(
            n))
    jd = json.loads(imgs.text)
    jd = jd['all_items']
    imgs_url = []
    for j in jd:
        imgs_url.append(j['bthumbUrl'])
    m = 0
    for img_url in imgs_url:
        print(img_url)
        print('***** ' + str(m) + '.jpg *****' + '   Downloading...')
        urllib.request.urlretrieve(img_url, path + str(m) + '.jpg')
        m = m + 1
        if m > 5:
          return
    print('Download complete!')


# getSogouImag('壁纸', 2000, 'd:/download/壁纸/')


def send_weixin_message(apiurl, image, content,mention_users, text_str=''):

    with open(image, 'rb') as file:  # 转换图片成base64格式
        data = file.read()
        encodestr = base64.b64encode(data)
        image_data = str(encodestr, 'utf-8')

    with open(image, 'rb') as file:  # 图片的MD5值
        md = hashlib.md5()
        md.update(file.read())
        image_md5 = md.hexdigest()

    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "image",
        "image": {
            "base64": image_data,
            "md5": image_md5
        }
    }

    res = requests.post(url=apiurl, json=data, headers=headers)
    print("http response status: ", res.status_code)


    # data1={
    #     "msgtype": "markdown",
    #     "markdown": {
    #         "content": content
    #     }
    # }
    # res=requests.post(url=apiurl,json=data1,headers={"Content-Type":"application/json;charset=utf-8"})
    # print("http response status1: ",res.status_code)

def send_120duty_reminder_wxmsg(plat, fortest=False):
    '''发送企业微信-群消息
    见：get_duty_name_2days_for_wx 返回的格式
    '''
    reminder_users = ''

    wx_apiurls = {
        'b2b': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9d77fc57-7275-49cc-af7d-89ba2c1cc59b',
        'b2c': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e659bc6e-43a0-49dd-81cc-0e21cda75f72',
        'IT': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c7eaf192-62c9-455f-b286-200f276f6006',
        'qm120': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e7cdbaec-f5ca-420f-9f72-11c0fba0945b',
        'itmanager': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c7eaf192-62c9-455f-b286-200f276f6006',
        'snatchPic2': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0a9c53f8-9989-4b6c-a1b2-8ab80a8270f8',
        'snatchPic3': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1c5b1465-eec1-4399-be2e-5c388a6691fe',
        'snatchPic': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2acadc82-c18a-4af9-8374-150e592262ae',
        'cancer': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8dd5250e-3d41-4891-a7a5-b5d43227f2b0'
    }

    apiurl = wx_apiurls[plat]
    print('群消息机器人：', apiurl)
    if fortest != False:
        to_users_name = ["hanbian"]  # just for test
        print('需提醒的人员: ', to_users_name)
        print('【测试用】群消息机器人：', apiurl)
        print('发送企业微信 群消息: ', apiurl)
        image ="C:\\Users\\hanbian\\Pictures\\Camera Roll\\ff.jpg"
        # image ="/usr/local/hanbian/image/ff.jpg"
        content ="Life is anacreontic, Everything is lovely "
        send_weixin_message(apiurl, image,content, to_users_name,
                            reminder_users)
        return True


if __name__ == '__main__':
    pass
    send_120duty_reminder_wxmsg('snatchPic', fortest=True)
