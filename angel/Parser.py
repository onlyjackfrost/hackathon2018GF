import urllib.request
import json
import jieba
from bs4 import BeautifulSoup
import re
import random




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

        # self._keelung_hot_view = {'望幽谷':0, \
        #                 '和平島濱海公園':0, \
        #                 '八斗子漁港':0, \
        #                 '基隆國立海洋科技博物館':0, \
        #                 '基隆廟口':0, \
        #                 '基隆港':0, \
        #                 '彭佳嶼':0, \
        #                 '二砂灣砲台(海門天險)':0, \
        #                 '老大公廟':0, \
        #                 '仙洞巖':0, \
        #                 '基隆潮境公園':0, \
        #                 '正濱漁港':0, \
        #                 '藍色公路':0, \
        #                 '碧砂漁港':0, \
        #                 '情人湖公園':0, \
        #                 '八斗子海濱公園':0, \
        #                 '基隆海洋廣場':0, \
        #                 '基隆嶼野百合':0, \
        #                 '陽明海洋文化藝術館':0, \
        #                 '基隆河壺穴景觀':0}
        # self._keelung_hot_food = ['孝三路大腸圈','廖媽媽珍珠奶茶','珍珠園烤玉米','蒟蒻屋','阿華炒麵','張仙燴飯','美華牛肉麵']
        self._taipei_hot_view = {'猴硐貓村':0, \
                            '洛德城堡':0, \
                            '黃金瀑布':0, \
                            '台北動物園(木柵動物園)':0, \
                            '袖珍博物館':0, \
                            '大稻埕碼頭':0, \
                            '老梅綠石槽':0, \
                            '世界巧克力夢公園':0, \
                            '四四南村':0, \
                            '菁桐老街':0, \
                            '十分老街':0, \
                            '夢幻湖':0, \
                            '北海岸濱海公路':0, \
                            '平溪老街':0, \
                            '雲仙樂園':0, \
                            '八煙聚落':0, \
                            '十分瀑布':0, \
                            '擎天崗':0, \
                            '水湳洞陰陽海':0, \
                            '中正紀念堂': 0, \
                            '台北101購物中心':0}
        self._taipei_hot_food = {'畬室':0, \
                                 '忠南飯館':0, \
                                 '祥雲龍吟':0, \
                                 '肥前屋':0, \
                                 '寬巷子':0, \
                                 '上引水產':0, \
                                 '川味兒川菜館':0, \
                                 '阿宗麵線':0, \
                                 '八拾捌茶輪番所':0, \
                                 '林家蔬菜羊肉爐':0, \
                                 '山海樓':0, \
                                 '阜杭豆漿':0, \
                                 '四知堂':0, \
                                 '北平半畝園小館':0, \
                                 '肉大人肉舖火鍋':0, \
                                 '天津蔥抓餅':0, \
                                 '陳三鼎黑糖粉圓鮮奶':0, \
                                 '紫藤廬':0}
        # self._hsinchu_hot_view = {'北埔老街': 0, \
        #                      '味衛佳柿餅觀光農場': 0, \
        #                      '十七公里海岸風景區': 0, \
        #                      '內灣合興車站（愛情火車站）': 0, \
        #                      '內灣老街': 0, \
        #                      '小叮噹科學遊樂區': 0, \
        #                      '青蛙石': 0, \
        #                      '五指山': 0, \
        #                      '青草湖': 0, \
        #                      '北埔冷泉': 0, \
        #                      '綠世界生態農場(原綠世界休閒農場)': 0, \
        #                      '新月沙灣（坎頂與坎仔腳）': 0, \
        #                      '司馬庫斯神木群': 0, \
        #                      '新竹漁港(南寮漁港、南寮地中海、南寮舊漁港)': 0, \
        #                      '好客好品希望工場': 0, \
        #                      '眷村博物館': 0, \
        #                      '湖口老街': 0, \
        #                      '張學良文化園區（張學良故居）': 0, \
        #                      '鴛鴦谷瀑布群 ': 0}
        # self._hsinchu_hot_food = ['玉龍肉圓']

    def _CompareWithTopView(self,user_Say,qty): # return view , qty : 數量
        view_list = []
        if user_Say in self._taipei_hot_view.keys() or user_Say in ['台北','台北市'] :
            view_list = random.sample(self._taipei_hot_view_hot_view, qty)
        # elif user_Say in self._keelung_hot_view.keys() or user_Say in '基隆' :
        #     view_list = random.sample(self._keelung_hot_view, qty)
        # elif user_Say in self._hsinchu_hot_view.keys() or user_Say in '新竹' :
        #     view_list = random.sample(self._hsinchu_hot_view, qty)
        else:
            view_list = 'moabo'
        view_str = " ".join(str(x) for x in view_list)
        return ('這附近景點是' + view_str)

    def _CompareWithTop10Food(self,user_Say,qty): # return Food , qty :數量
        food_list = []
        if user_Say in self._taipei_hot_view.keys() or user_Say in ['台北','台北市'] :
            food_list = random.sample(self._taipei_hot_food.keys(), qty)
        # elif user_Say in self._keelung_hot_view.keys():
        #     food_list = random.sample(self._keelung_hot_food, qty)
        # elif user_Say in self._hsinchu_hot_view.keys():
        #     food_list = random.sample(self._hsinchu_hot_food, qty)
        else:
            food_list = '都是puan'
        food_str = " ".join(str(x) for x in food_list)
        return ('這附近美食'+ food_str)

    def _FoodRankViaPixnet(self,area,qty): # data : dict, area : str, return view or food.
        _food_list = []
        _url = 'https://emma.pixnet.cc/mainpage/blog/categories/'
        _attr = 'hot'
        _food_id = '26'  # 28 國內旅遊, 26:食物
        _rnd_page = '&page=' + str(random.randint(1, 10))
        _filter = '&fileter=top_authors'
        _dataFormat = '?&apiversion=2&format=json&per_page=20' + _filter  # +_rnd_page#

        foodRes = self._getHTTP(_url, _attr, _food_id, _dataFormat)
        self._parser(foodRes, area)
        for k, v in self._taipei_hot_food.items():
            if len(_food_list) == qty:
                _food_str = " ".join(str(x) for x in _food_list)
                return (_food_str)
            if v > 0:
                _food_list.append(k)
            else:
                _food_list = random.sample(self._taipei_hot_food.keys(), qty)

    def _ViewRankViaPixnet(self, area, qty):  # data : dict, area : str, return view
        _view_list = []
        _url = 'https://emma.pixnet.cc/mainpage/blog/categories/'
        _attr = 'hot'
        _view_id = '28'  # 28 國內旅遊, 26:食物
        _rnd_page = '&page=' + str(random.randint(1, 10))
        _filter = '&fileter=top_authors'
        _dataFormat = '?&apiversion=2&format=json&per_page=20' + _filter  # +_rnd_page#

        viewRes = self._getHTTP(_url, _attr, _view_id, _dataFormat)
        self._parser(viewRes,area)
        for k,v in self._taipei_hot_view.items():
            if len(_view_list) == qty:
                _view_str = " ".join(str(x) for x in _view_list)
                return (_view_str)
            if v >0 :
                _view_list.append(k)
            else:
                _view_list = random.sample(self._taipei_hot_view.keys(),qty)


    def _getHTTP(self,_url,_attr,_category_id,_dataFormat): # return data
        contents = urllib.request.urlopen(_url + _attr + '/' + _category_id + _dataFormat)
        decoder = contents.read().decode('utf-8')
        data = json.loads(decoder)  # dict
        # print(data)
        return (data)  #json to dict

    def _parser(self,data,jkey): # jkey = str ,"台北" , "食物"
        self._cmd = jkey
        for i in range(0, len(data['articles'])):
            for t in range(0,len(data['articles'][i][self._key2[22]])):
                b = data['articles'][i][self._key2[15]]
                c = data['articles'][i][self._key2[22]][t]['tag']
                a = jieba.cut(b, cut_all=False)
                d = jieba.cut(c, cut_all=False)
                if jkey in list(a) or jkey in list(d):
                    match_link = data['articles'][i][self._key2[8]]
                    match_title = data['articles'][i][self._key2[15]]
                    if jkey in self._taipei_hot_view.keys():
                        self._taipei_hot_view[jkey] += 1
                    if jkey in self._taipei_hot_food.keys():
                        self._taipei_hot_food[jkey] += 1
        # return

    def _catch(self,url):
        if not url:
            return 0
        data = urllib.request.urlopen(url)
        soup = BeautifulSoup(data, "html.parser")
        tag = soup.html.find_all('a')
        s_txt = soup.get_text()
        if s_txt.find(self._cmd):
            start = s_txt.find(self._cmd)
            end = s_txt[start:].find(' ')
            getStr = s_txt[start:end]

        return (tag)


if __name__=='__main__':

    pixnet = Pixnet_API()

    _area = 'forever 21'
    f = pixnet._CompareWithTop10Food(_area,3)

    print ('_CompareWithTop10Food = ', f)

    g = pixnet._CompareWithTopView(_area,3)

    print ('_CompareWithTopView = ', g)

    view_list = pixnet._ViewRankViaPixnet(_area,3)
    print ('_ViewRankViaPixnet = ', view_list)

    food_list = pixnet._FoodRankViaPixnet(_area,3)
    print ('_FoodRankViaPixnet = ', food_list)