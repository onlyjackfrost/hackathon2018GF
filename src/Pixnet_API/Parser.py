import urllib.request
import json
import jieba
# from demjson import demjson
from bs4 import BeautifulSoup
import re

class Pixnet_API(object):

    def __init__(self):
        self._jkey = 0
        self._twArea = ['基隆', '新北', '台北', '桃園', '新竹', '苗栗', '台中','彰化','南投','雲林','嘉義',\
                        '台南','高雄','屏東','宜蘭','花蓮','台東','金門','馬祖','綠島','蘭嶼','小琉球','澎湖']
        self._key1 = ['articles', 'total', 'page', 'per_page', 'message', 'error', 'api_version']
        self._key2 = ['id', 'public_at', 'site_category', 'site_category_id', 'sub_site_category', 'sub_site_category_id', \
                 'category', 'category_id', 'link', 'status', 'is_top', 'is_nl2br', 'comment_perm', 'comment_hidden', \
                 'summary','title', 'thumb', 'cover', 'hits', 'info', 'hit_uri', 'sns', 'tags', 'user']
        self._cmd = ''

    def _getHTTP(self,_url,_attr,_category_id,_dataFormat):
        contents = urllib.request.urlopen(_url + _attr + '/' + _category_id + _dataFormat)
        decoder = contents.read().decode('utf-8')
        data = json.loads(decoder)  # dict
        return (data)  #json to dict

    def _parser(self,data,jkey): # jkey = str ,"台北"

        self._cmd = jkey
        # for i in jkey:
        #     if jkey in self._key2:
        #         self._jkey = i



        for i in range(0, len(data['articles'])):
            # for key,values in  data['articles'][i].items():
            # print ('---',key,values)
            # print('------------------------------------------')
            # print ('title = ',data['articles'][i][_key2[15]])
            b = data['articles'][i][self._key2[15]]
            a = jieba.cut(b, cut_all=False)
            # print ('a = ', a)
            # if jkey in self._twArea and jkey in a:
            if jkey in list(a):
                #for jkey in a:

                    # print(str(jkey))  # '我想去''
                    # print('tags = ', data['articles'][i][self._key2[22]])
                    # print('title = ', data['articles'][i][self._key2[15]])
                    # print('link = ', data['articles'][i][self._key2[8]])
                    if (data['articles'][i][self._key2[15]].find(jkey)):
                        # print ('title = ',data['articles'][i][self._key2[15]])
                        # print ('link = ',data['articles'][i][self._key2[8]])
                        # print ('link = ',data['articles'][i][self._key2[8]])
                        self._jkey = i
                        break
        return (data['articles'][self._jkey][self._key2[8]])

            # print('------------------------------------------')
        # return (data['articles'][i][self._key2[8]])

    def _catch(self,url):
        data = urllib.request.urlopen(url)
        soup = BeautifulSoup(data, "html.parser")
        a = soup.html.find_all("title")



        s_txt = soup.get_text()

        # a = re.findall(self._cmd+,s_txt)

        if s_txt.find(self._cmd):
            start = s_txt.find(self._cmd)
            end = s_txt[start:].find(' ')
            getStr = s_txt[start:end]

        # return (getStr)
        return (a)


        # try:
        #     data = urllib.request.urlopen(url)
        #     soup = BeautifulSoup(data, "html.parser")
        #     a = soup.html.find_all("title")
        #
        #     soup_chinese = re.compile(u"[\u4e00-\u9fa5]+",soup)
        #     # for strong_tag in soup.find_all('strong'):
        #     #     strong_tag.text, strong_tag.next_sibling
        #     # return (strong_tag.text,strong_tag.next_sibling)
        #     s_txt = soup.text()
        #     return (s_txt)
        # except TypeError:
        #     print ('error 100')
# -----------Jieba cut------------------
# _twArea = ['基隆', '新北', '台北', '桃園', '新竹', '苗栗', '台中']
# _key1 = ['articles', 'total', 'page', 'per_page', 'message', 'error', 'api_version']
# _key2 = ['id', 'public_at', 'site_category', 'site_category_id', 'sub_site_category', 'sub_site_category_id',
#          'category', 'category_id', 'link', 'status', 'is_top', 'is_nl2br', 'comment_perm', 'comment_hidden', 'summary',
#          'title', 'thumb', 'cover', 'hits', 'info', 'hit_uri', 'sns', 'tags', 'user']
#
# sentence = '我是文青，我在台北輕旅行。'
# words = jieba.cut(sentence, cut_all=False)
# for word in words:
#     if word in _twArea:
#         print(str(word))  # '我想去''
#     # print (word)

# -----------HTTP get method-------------
# _url = 'https://emma.pixnet.cc/mainpage/blog/categories/'
# _attr = 'hot'
# _category_id = '28'  # 國內旅遊
# _dataFormat = '?&apiversion=2&format=json&per_page=20'
# contents = urllib.request.urlopen(_url + _attr + '/' + _category_id + _dataFormat)
# decoder = contents.read().decode('utf-8')
# data = json.loads(decoder)  # dict
#
# dem_data = demjson.decode(decoder)
# ----------------------------------------
# print (data)

# print (data.keys())
# print (data.values())
# for key,values in  data.items():
#    print (key,values)

# --------------------------------------------
# print (data['articles'][0].keys())
#
# for i in range(0, len(data['articles'])):
#     # for key,values in  data['articles'][i].items():
#     # print ('---',key,values)
#     print ('------------------------------------------')
#     # print ('title = ',data['articles'][i][_key2[15]])
#     b = data['articles'][i][_key2[15]]
#     a = jieba.cut(b, cut_all=False)
#     for word in a:
#         if word in _twArea:
#             print(str(word))  # '我想去''
#             print ('tags = ', data['articles'][i][_key2[22]])
#             print ('title = ', data['articles'][i][_key2[15]])
#             print ('link = ', data['articles'][i][_key2[8]])
#     #         if (data['articles'][i][_key2[15]].find(u'台中')):
#     #             print ('title = ',data['articles'][i][_key2[15]])
#     #             print ('link = ',data['articles'][i][_key2[8]])
#     # print ('link = ',data['articles'][i][_key2[8]])
#     print ('------------------------------------------')
# ------------------------------------------------------------
# print (data['articles'][0])
# print (data['page'])
# print (data['per_page'])
# print (data['error'])
# print (data['api_version'])

# --------------------------
# for key,values in  data['articles'][i].items():
#         #print ('---',key,values)
#     print ('link = ',data['articles'][i][_key2[8]])
# --------------------
# print (dem_data)
# --------------------------------------
# type(data)
# type(data['articles'])
# a = data['articles']
# b = dict(a)
# print (b.keys())


# DicData = dict(data['articles'])
# print (DicData['category'])


# --------------------------
# for i in range(0,len(data[_key1[0]])):
#     for key,values in  data[_key1[0]][i].items():
#         #print (key,values)
#         print (values)
#         if (values[5].find('台中')):
#             print ('title : %s',data[_key1[0]][i]['title'])
# ----------------------------------
# for i in range(0, len(data['articles'])):
#     for key, values in data['articles'][i].items():
#         print ('---', key, values)
# ---------------------------------


if __name__=='__main__':
    _url = 'https://emma.pixnet.cc/mainpage/blog/categories/'
    _attr = 'hot'
    _category_id = '28'  # 國內旅遊
    _filter = '&fileter=top_authors'
    _dataFormat = '?&apiversion=2&format=json&per_page=100'+_filter

    _jkey = '台北'

    pixnet = Pixnet_API()
    uWant = pixnet._getHTTP(_url,_attr,_category_id,_dataFormat)
    ulink = pixnet._parser(uWant,_jkey)
    # print ('uWant = ', uWant)
    print ('ulink = ', ulink)

    # catch_a,catch_b = pixnet._catch(ulink)
    # print (catch_a)
    # print (catch_b)
    txt = pixnet._catch(ulink)
    print (txt)