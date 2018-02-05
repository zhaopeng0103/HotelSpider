import requests
from bs4 import BeautifulSoup
import bs4
import xlsxwriter

def getHTMLTEXT(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "请求失败——>" + url


def getHotelListHref(hotelListHref, html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup.find("ol", attrs={"class": "hotel-list-container"}))
    for aLink in soup.find_all('ol', attrs={"class" : ""}):
        hotelListHref.append(aLink.attrs['class'])

if __name__ == "__main__":
    hotelListHref = []
    baseURL = "https://www.agoda.com"
    hotelListURL = baseURL + "/zh-cn/pages/agoda/default/DestinationSearchResult.aspx?city=1569&languageId=8&userId=fd38c7b4-8fc5-498e-ae4b-57dbb540012c&pageTypeId=1&origin=CN&locale=zh-CN&cid=1463261&tag=1f8e8af2086447e491ea69277d0290da3741&aid=97720&currencyCode=CNY&htmlLanguage=zh-cn&cultureInfoName=zh-CN&ckuid=fd38c7b4-8fc5-498e-ae4b-57dbb540012c&checkIn=2018-02-14&checkOut=2018-02-15&rooms=1&adults=2&children=0&hotelReviewScore=5&tabId=5&priceCur=CNY&los=1&textToSearch=%E5%8C%97%E4%BA%AC"
    hotelListHTML = getHTMLTEXT(hotelListURL)
    getHotelListHref(hotelListHref, hotelListHTML)
    print(hotelListHref)

