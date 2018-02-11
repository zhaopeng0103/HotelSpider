import requests
from bs4 import BeautifulSoup
import bs4
import xlsxwriter
import random
import time


# 生成随机整数
def produceRandomInt(min, max):
    return random.randint(min, max)


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


def createWorkbook(name):
    workbook = xlsxwriter.Workbook(name)
    style1 = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'bold': True, 'fg_color': '#10aeff'})
    style2 = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    return workbook, style1, style2

def exportExcel(data, workbook, style1, style2):
    worksheet1 = workbook.add_worksheet()
    worksheet1.set_column('B:B', 30)
    worksheet1.set_column('D:D', 40)
    worksheet1.set_column('K:K', 100)
    worksheet1.set_column('Q:Q', 100)
    worksheet1.merge_range(0, 0, 1, 0, "id", style1)
    worksheet1.merge_range(0, 1, 1, 1, "酒店名字", style1)
    worksheet1.merge_range(0, 2, 1, 2, "酒店分类", style1)
    worksheet1.merge_range(0, 3, 1, 3, "酒店位置", style1)
    worksheet1.merge_range(0, 4, 0, 10, "住客印象", style1)
    worksheet1.merge_range(0, 11, 0, 15, "住客点评", style1)
    worksheet1.merge_range(0, 16, 1, 16, "URL", style1)
    worksheet1.write(1, 4, "性价比", style1)
    worksheet1.write(1, 5, "服务", style1)
    worksheet1.write(1, 6, "交通", style1)
    worksheet1.write(1, 7, "设施", style1)
    worksheet1.write(1, 8, "房间", style1)
    worksheet1.write(1, 9, "房间", style1)
    worksheet1.write(1, 10, "评论", style1)
    worksheet1.write(1, 11, "总分", style1)
    worksheet1.write(1, 12, "位置", style1)
    worksheet1.write(1, 13, "设施", style1)
    worksheet1.write(1, 14, "服务", style1)
    worksheet1.write(1, 15, "卫生", style1)
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet1.write(row + 2, col, data[row][col], style2)
    workbook.close()
    print("write over!")


if __name__ == "__main__":
    name = 'xiecheng_xianggang.xlsx'
    workbook, style1, style2 = createWorkbook(name)
    page = 50
    baseURL = "http://hotels.ctrip.com"
    datas = []
    for p in range(page):
        if (p + 1) % 5 == 0:
            second = produceRandomInt(15, 30)
            print("Program will sleep for " + str(second) + " seconds! current page:" + str(p + 1) + ";current data num:" + str(len(datas)))
            time.sleep(second)
        try:
            hotelListURL = baseURL + "/Domestic/Tool/AjaxHotelList.aspx?__VIEWSTATEGENERATOR=DB1FBB6D&cityName=香港&StartTime=2018-02-12&DepTime=2018-02-13&operationtype=NEWHOTELORDER&IsOnlyAirHotel=F&cityId=58&cityPY=xianggang&cityCode=1852&cityLat=22.291&cityLng=114.172&htlPageView=0&hotelType=F&hasPKGHotel=F&requestTravelMoney=F&isusergiftcard=F&useFG=F&priceRange=-2&promotion=F&prepay=F&IsCanReserve=F&OrderBy=99&checkIn=2018-02-12&checkOut=2018-02-13&hidTestLat=0|0&AllHotelIds=6023614%2C426549%2C426593%2C426551%2C436835%2C344922%2C436515%2C436846%2C419933%2C2387600%2C436870%2C1830031%2C532864%2C371391%2C481133%2C778134%2C11018959%2C436874%2C708765%2C5500588%2C392670%2C2037118%2C436850%2C6555104%2C2198346&HideIsNoneLogin=T&isfromlist=T&ubt_price_key=htl_search_result_promotion&isHuaZhu=False&htlFrom=hotellist&hotelIds=6023614_1_1,426549_2_1,426593_3_1,426551_4_1,436835_5_1,344922_6_1,436515_7_1,436846_8_1,419933_9_1,2387600_10_1,436870_11_1,1830031_12_1,532864_13_1,371391_14_1,481133_15_1,778134_16_1,11018959_17_1,436874_18_1,708765_19_1,5500588_20_1,392670_21_1,2037118_22_1,436850_23_1,6555104_24_1,2198346_25_1&markType=0&a=0&contrast=0&contyped=0&page=" + str(p + 1)
            hotelList = getPOSTJSON(hotelListURL)
            for hotel_list in hotelList["hotelPositionJSON"]:
                id = hotel_list["id"]
                name = hotel_list["name"]
                hotelInfoURL = baseURL + hotel_list["url"]
                hotelInfo = getHTMLTEXT(hotelInfoURL)
                try:
                    data = praseHTMLTEXT(id, name, hotelInfo, hotelInfoURL)
                    datas.append(data)
                except:
                    print("error:子程序异常")
                    continue
        except:
            print("error:主程序异常")
            continue
    print("total data number:" + str(len(datas)))
    exportExcel(datas, workbook, style1, style2)
