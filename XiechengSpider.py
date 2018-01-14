import requests
from bs4 import BeautifulSoup
import bs4
import xlsxwriter
from urllib import parse,request
import json


def getAjaxResponse():
    textmod = {
        "__VIEWSTATEGENERATOR":"DB1FBB6D", "cityName":"北京", "StartTime":"2018-01-15", "DepTime":"2018-01-16",
        "txtkeyword":"", "Resource":"", "Room":"", "Paymentterm":"", "BRev":"", "Minstate":"", "PromoteType":"",
        "PromoteDate":"", "operationtype":"NEWHOTELORDER", "PromoteStartDate":"", "PromoteEndDate":"",
        "OrderID":"RoomNum", "IsOnlyAirHotel":"F", "cityId":"1", "cityPY":"beijing", "cityCode":"010",
        "cityLat":"39.9105329229", "cityLng":"116.413784021", "positionArea":"", "positionId":"", "hotelposition":"",
        "keyword":"", "hotelId":"", "htlPageView":"0", "hotelType":"F", "hasPKGHotel":"F", "requestTravelMoney":"F",
        "isusergiftcard":"F", "":"", "":"", "":"", "":"", "":"",
        "":"", "":"", "":"", "":"",
        "":"",

    }
    textmod = "=F&useFG=F&HotelEquipment=&priceRange=-2&hotelBrandId=&promotion=F&prepay=F&IsCanReserve=F&OrderBy=99&OrderType=&k1=&k2=&CorpPayType=&viewType=&checkIn=2018-01-15&checkOut=2018-01-16&DealSale=&ulogin=&hidTestLat=0%257C0&AllHotelIds=691682%252C375265%252C608345%252C375126%252C2298288%252C436894%252C452197%252C1641390%252C1722447%252C1249518%252C1725911%252C431617%252C1836257%252C456474%252C433114%252C4035013%252C6684925%252C5226364%252C2703098%252C9627725%252C5389632%252C452221%252C2642089%252C436066%252C1251776&psid=&HideIsNoneLogin=T&isfromlist=T&ubt_price_key=htl_search_result_promotion&showwindow=&defaultcoupon=&isHuaZhu=False&hotelPriceLow=&htlFrom=hotellist&unBookHotelTraceCode=&showTipFlg=&hotelIds=691682_1_1%2C375265_2_1%2C608345_3_1%2C375126_4_1%2C2298288_5_1%2C436894_6_1%2C452197_7_1%2C1641390_8_1%2C1722447_9_1%2C1249518_10_1%2C1725911_11_1%2C431617_12_1%2C1836257_13_1%2C456474_14_1%2C433114_15_1%2C4035013_16_1%2C6684925_17_1%2C5226364_18_1%2C2703098_19_1%2C9627725_20_1%2C5389632_21_1%2C452221_22_1%2C2642089_23_1%2C436066_24_1%2C1251776_25_1&markType=0&zone=&location=&type=&brand=&group=&feature=&equip=&star=&sl=&s=&l=&price=&a=0&keywordLat=&keywordLon=&contrast=0&contyped=0&productcode=&page=1"
    # 普通数据使用
    textmod = parse.urlencode(textmod).encode(encoding='utf-8')
    print(textmod)
    # header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    #                "Content-Type": "application/json"}
    # url = 'http://192.168.199.10/api_jsonrpc.php'
    # req = request.Request(url=url, data=textmod, headers=header_dict)
    # res = request.urlopen(req)
    # res = res.read()


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "抓取失败"


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[3].string])


def exportExcel(data):
    workbook = xlsxwriter.Workbook('xiecheng.xlsx')
    worksheet1 = workbook.add_worksheet()
    worksheet1.merge_range(0, 0, 1, 0, '酒店名字')
    worksheet1.merge_range(0, 1, 1, 1, '酒店分类')
    worksheet1.merge_range(0, 2, 0, 6, "评论分类")
    worksheet1.write(1, 2, "性价比")
    worksheet1.write(1, 3, "服务")
    worksheet1.write(1, 4, "交通")
    worksheet1.write(1, 5, "设施")
    worksheet1.write(1, 6, "卫生")
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet1.write(row + 2, col, data[row][col])
    workbook.close()
    print("write over!")


if __name__ == "__main__":
    getAjaxResponse()
    # data = []

    # exportExcel(data)