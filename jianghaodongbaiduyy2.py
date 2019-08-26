# -*- coding: UTF-8 -*-
from aip import AipSpeech
import subprocess
import datetime
import os
import time
from pydub import AudioSegment
import math
import requests
from json import loads
# 定义常量
def yy():
    #APP_ID = '你的 App ID'
    APP_ID = '11617242'
    #API_KEY = '你的 API Key'
    API_KEY = 'jGxIpr9XISB0CAZI8gwnAVeH'
    #SECRET_KEY = '你的 Secret Key'
    SECRET_KEY = 'OgtAx0IWHZN10U8r5D7a06npNr9889V5'
    # 初始化AipSpeech对象
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    fileFullName=('voice.wav')
    # 文件处理
    def get_wave_filename(fileFullName):
            # MP3文件转换成wav文件
            # 判断文件后缀，是mp3的，直接处理为16k采样率的wav文件；
            # 是wav的，判断文件的采样率，不是8k或者16k的，直接处理为16k的采样率的wav文件
            # 其他情况，就直接返回AudioSegment直接处理
            fileSufix = fileFullName[fileFullName.rfind('.')+1:]
            print(fileSufix)
            filePath = fileFullName[:fileFullName.find(os.sep)+1]
            print(filePath)
            if fileSufix.lower() == "mp3":
                    wavFile = "wav_%s.wav" %datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    wavFile = filePath + wavFile
                    cmdLine = "ffmpeg -i \"%s\" -ar 16000 " %fileFullName
                    cmdLine = cmdLine + "\"%s\"" %wavFile
                    print(cmdLine)
                    ret = subprocess.run(cmdLine)
                    print("ret code:%i" %ret.returncode)
                    return wavFile
                    #if ret.returncode == 1:
                    #	return wavFile
                    #else:
                    #	return None
            else:
                    return fileFullName


    #文件分片


    filePath = fileFullName[:fileFullName.find(os.sep)+1]
    # 文件处理为Wav，采样率16k的文件，返回文件名
    wavFile = get_wave_filename(fileFullName)
    print(wavFile)
    record = AudioSegment.from_wav(wavFile)
    if wavFile != fileFullName:
            time.sleep(1)
            os.remove(wavFile)

    recLen = record.duration_seconds
    interval = 120 * 1000
    maxLoop = math.ceil(recLen*1000/float(interval))
    for n in range(0,math.ceil(recLen*1000/float(interval))):
            recSeg = record[n * interval : (n + 1)*interval]
            #print("Segment:%i,startat:%i,length:%i" %n,n*interval/1000,recSeg.duration_seconds)
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " >> Segment:" + str(n) +"/" + str(maxLoop))
            segFile = filePath + "seg%s.wav" %("0"*7 + str(n))[-6:]
            # 把分段的语音信息保存为临时文件
            file_handle = recSeg.export(segFile,format="wav",codec = "libvorbis")
            file_handle.close()
            # 读取分段的临时文件为字节
            file_handle = open(segFile, 'rb')
            file_content = file_handle.read()
            file_handle.close()
            # 删除临时文件
            os.remove(segFile)
            # 用百度API处理该语音
            result=aipSpeech.asr(file_content, 'pcm', 16000, {'lan': 'zh'})
            if result['err_no'] == 0:
                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " >> " + result['result'][0])
                    file = open('/home/pi/jiqiren/1.txt','w+')
                    file.write(result['result'][0])                
                                               
            else:
                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " >> " + "err_no:" + str(result['err_no']))
    class LoginTic(object):
        def __init__(self):
            self.headers = {
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
            }

            self.key = '35ff2856b55e4a7f9eeb86e3437e23fe'#'35ff2856b55e4a7f9eeb86e3437e23fe'0989c3cdc99d4883890e584f16dd3a9b
            # 创建一个网络请求session实现登录验证
            #self.key = '0989c3cdc99d4883890e584f16dd3a9b'
            self.session = requests.session()

        def talkWithTuling(self,text):
            url = 'http://www.tuling123.com/openapi/api'
            data = {
                'key':self.key,         #key
                'info':text,            #发给图灵的内容
                'userid':'123456swh'#'123456swh'302770    #用户id,自己设置1-32的字母和数字组合
            }
            response = requests.post(url=url, headers=self.headers, data=data)
            return response.text


    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    ll = LoginTic()
    file = open('/home/pi/jiqiren/2.txt','w+')
    file1 = open('/home/pi/jiqiren/1.txt','w+')
    print('你想和我聊什么？:')
    userName = result['result'][0]
    # cont = ll.talkWithTuling('你好')
    cont = ll.talkWithTuling(userName)
    print (cont)
    dd = loads(cont)
    if dd['code'] == 100000:
        # 返回的是文本
        print ('-'*10)
        print (dd['text'])
        file = open('/home/pi/jiqiren/2.txt','w')
        file.write(dd['text'])
        result = client.synthesis(dd['text'], options={'vol':5})
        if not isinstance(result,dict):
            with open('audio4.mp3','wb') as f:
                f.write(result)
        else:print(result)
        os.system('mpg123 audio4.mp3')

    elif dd['code'] == 200000:
        # '链接累的内容'
        print (dd['text'])
        print (dd['url'])
    elif dd['code'] == 302000:
        # 新闻类的内容
        print (dd['text'])
        print (len(dd['list']))
    elif dd['code'] == 308000:
        # 菜谱类的内容
        pass
    elif dd['code'] == 313000:
        # 儿歌类的
        pass
    elif dd['code'] == 314000:
        #儿童诗词类的
        pass
    else:
        print('shibiebudao')

    print ('按键进行录音对话')
