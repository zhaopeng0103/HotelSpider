import requests
from bs4 import BeautifulSoup
import bs4
import xlsxwriter


def getPOSTJSON(url):
    try:
        r = requests.post(url, timeout=60)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.json()
    except:
        return "请求失败——>" + url


def getHTMLTEXT(url, code="utf-8"):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "请求失败——>" + url


def praseHTMLTEXT(id, name, hotelInfo, url):
    soup = BeautifulSoup(hotelInfo, "html.parser")
    # 位置
    address = ""
    i = 0
    for ch in soup.find("div", attrs={"class": "adress"}).children:
        if i < 4 and isinstance(ch, bs4.element.Tag):
            address += ch.string
            i = i + 1
    # 住客评分
    comment_sumary_box = soup.find("div", attrs={"class": "comment_sumary_box"})
    totalScore = comment_sumary_box("span", attrs={"class": "score"})[0]("span", attrs={"class": "n"})[0].string
    locationScore = comment_sumary_box("div", attrs={"class": "bar_score"})[0]("span", attrs={"class": "score"})[0].string
    facilityScore = comment_sumary_box("div", attrs={"class": "bar_score"})[0]("span", attrs={"class": "score"})[1].string
    serveScore = comment_sumary_box("div", attrs={"class": "bar_score"})[0]("span", attrs={"class": "score"})[2].string
    healthScore = comment_sumary_box("div", attrs={"class": "bar_score"})[0]("span", attrs={"class": "score"})[3].string
    # 住客印象
    user_impress = soup.find("div", attrs={"class": "user_impress"})
    if user_impress("a") is not None:
        length = len(user_impress("a"))
    else:
        length = 0
    if length > 0:
        locationComment = user_impress("a")[0].string
    else:
        locationComment = ""
    if length > 1:
        serveComment = user_impress("a")[1].string
    else:
        serveComment = ""
    if length > 2:
        priceComment = user_impress("a")[2].string
    else:
        priceComment = ""
    if length > 3:
        roomComment = user_impress("a")[3].string
    else:
        roomComment = ""
    if length > 4:
        facilityComment = user_impress("a")[4].string
    else:
        facilityComment = ""
    if length > 5:
        trafficComment = user_impress("a")[5].string
    else:
        trafficComment = ""
    # 评论
    comments = ""
    comment_detail_list = soup.find("div", attrs={"class": "comment_detail_list"}).children
    x = 0
    for comment_detail in comment_detail_list:
        comment = comment_detail("div", attrs={"class": "J_commentDetail"})[0].string
        if comment is not None:
            comments = comments + "（" + str(x + 1) + "）" + comment
            x = x + 1

    data = [id, name, "国内酒店", address, locationComment, serveComment, priceComment, roomComment, facilityComment, trafficComment, comments, totalScore, locationScore, facilityScore, serveScore, healthScore, url]
    print(data)
    return data


def exportExcel(data):
    workbook = xlsxwriter.Workbook('xiecheng.xlsx')
    worksheet1 = workbook.add_worksheet()
    worksheet1.merge_range(0, 0, 1, 0, "id")
    worksheet1.merge_range(0, 1, 1, 1, "酒店名字")
    worksheet1.merge_range(0, 2, 1, 2, "酒店分类")
    worksheet1.merge_range(0, 3, 1, 3, "酒店位置")
    worksheet1.merge_range(0, 4, 0, 10, "住客印象")
    worksheet1.merge_range(0, 11, 0, 15, "住客点评")
    worksheet1.merge_range(0, 16, 1, 16, "URL")
    worksheet1.write(1, 4, "性价比")
    worksheet1.write(1, 5, "服务")
    worksheet1.write(1, 6, "交通")
    worksheet1.write(1, 7, "设施")
    worksheet1.write(1, 8, "房间")
    worksheet1.write(1, 9, "房间")
    worksheet1.write(1, 10, "评论")
    worksheet1.write(1, 11, "总分")
    worksheet1.write(1, 12, "位置")
    worksheet1.write(1, 13, "设施")
    worksheet1.write(1, 14, "服务")
    worksheet1.write(1, 15, "卫生")
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet1.write(row + 2, col, data[row][col])
    workbook.close()
    print("write over!")


if __name__ == "__main__":
    page = 5
    baseURL = "http://hotels.ctrip.com"
    datas = []
    for p in range(page):
        hotelListURL = baseURL + "/Domestic/Tool/AjaxHotelList.aspx?__VIEWSTATEGENERATOR=DB1FBB6D&cityName=北京&StartTime=2018-02-15&DepTime=2018-02-16&operationtype=NEWHOTELORDER&IsOnlyAirHotel=F&cityId=1&cityPY=beijing&cityCode=010&cityLat=39.9105329229&cityLng=116.413784021&htlPageView=0&hotelType=F&hasPKGHotel=F&requestTravelMoney=F&isusergiftcard=F&useFG=F&priceRange=-2&promotion=F&prepay=F&IsCanReserve=F&OrderBy=99&checkIn=2018-01-17&checkOut=2018-01-18&hidTestLat=0|0&AllHotelIds=691682,375265,608345,375126,2298288,436894,452197,1641390,1722447,1249518,1725911,431617,1836257,456474,433114,4035013,6684925,5226364,2703098,9627725,5389632,452221,2642089,436066,1251776&HideIsNoneLogin=T&isfromlist=T&ubt_price_key=htl_search_result_promotion&isHuaZhu=False&htlFrom=hotellist&hotelIds=691682_1_1,375265_2_1,608345_3_1,375126_4_1,2298288_5_1,436894_6_1,452197_7_1,1641390_8_1,1722447_9_1,1249518_10_1,1725911_11_1,431617_12_1,1836257_13_1,456474_14_1,433114_15_1,4035013_16_1,6684925_17_1,5226364_18_1,2703098_19_1,9627725_20_1,5389632_21_1,452221_22_1,2642089_23_1,436066_24_1,1251776_25_1&markType=0&a=0&contrast=0&contyped=0&page=" + str(p + 1)
        hotelList = getPOSTJSON(hotelListURL)
        for hotel_list in hotelList["hotelPositionJSON"]:
            id = hotel_list["id"]
            name = hotel_list["name"]
            hotelInfoURL = baseURL + hotel_list["url"]
            hotelInfo = getHTMLTEXT(hotelInfoURL)
            try:
                data = praseHTMLTEXT(id, name, hotelInfo, hotelInfoURL)
            except:
                continue
            datas.append(data)
    print(len(datas))
    exportExcel(datas)
