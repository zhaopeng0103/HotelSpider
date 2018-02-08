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
    for aLink in soup.find_all('ol', attrs={"class": ""}):
        hotelListHref.append(aLink.attrs['class'])


if __name__ == "__main__":
    hotelListHref = []
    baseURL = "https://www.agoda.com"
    hotelListURL = baseURL + "/zh-cn/pages/agoda/default/DestinationSearchResult.aspx?city=1569&pagetypeid=1&origin=CN&cid=-1&tag=&gclid=&aid=130243&userId=7d4d75ba-28cf-4f41-9957-f0a0e27e964f&loginLvl=0&languageId=8&languageFlag=cn&storefrontId=3&currencyId=15&currencyCode=CNY&htmlLanguage=zh-cn&trafficType=User&cultureInfoName=zh-CN&checkIn=2018-02-17&checkOut=2018-02-18&los=1&rooms=1&adults=2&children=0&childages=&priceCur=CNY&hotelReviewScore=5&ckuid=7d4d75ba-28cf-4f41-9957-f0a0e27e964f"
    hotelListHTML = getHTMLTEXT(hotelListURL)
    getHotelListHref(hotelListHref, hotelListHTML)
    print(hotelListHref)

