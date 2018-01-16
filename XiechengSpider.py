import requests
from bs4 import BeautifulSoup
import bs4
import xlsxwriter


def getHTMLText(url):
    try:
        r = requests.post(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.json()
    except:
        return "请求失败"


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
    url = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx?__VIEWSTATEGENERATOR=DB1FBB6D&cityName=北京&StartTime=2018-01-15&DepTime=2018-01-16&operationtype=NEWHOTELORDER&IsOnlyAirHotel=F&cityId=1&cityPY=beijing&cityCode=010&cityLat=39.9105329229&cityLng=116.413784021&htlPageView=0&hotelType=F&hasPKGHotel=F&requestTravelMoney=F&isusergiftcard=F&useFG=F&priceRange=-2&promotion=F&prepay=F&IsCanReserve=F&OrderBy=99&checkIn=2018-01-17&checkOut=2018-01-18&hidTestLat=0|0&AllHotelIds=691682,375265,608345,375126,2298288,436894,452197,1641390,1722447,1249518,1725911,431617,1836257,456474,433114,4035013,6684925,5226364,2703098,9627725,5389632,452221,2642089,436066,1251776&HideIsNoneLogin=T&isfromlist=T&ubt_price_key=htl_search_result_promotion&isHuaZhu=False&htlFrom=hotellist&hotelIds=691682_1_1,375265_2_1,608345_3_1,375126_4_1,2298288_5_1,436894_6_1,452197_7_1,1641390_8_1,1722447_9_1,1249518_10_1,1725911_11_1,431617_12_1,1836257_13_1,456474_14_1,433114_15_1,4035013_16_1,6684925_17_1,5226364_18_1,2703098_19_1,9627725_20_1,5389632_21_1,452221_22_1,2642089_23_1,436066_24_1,1251776_25_1&markType=0&a=0&contrast=0&contyped=0&page=1"
    jsonResult = getHTMLText(url)
    for hotel_url in jsonResult["hotelPositionJSON"]:
        print("id:" + hotel_url["id"] + ";name:" + hotel_url["name"] + ";url:" + hotel_url["url"])


    # exportExcel(data)