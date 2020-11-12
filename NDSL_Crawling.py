

# 요청 변수(request parameter) 출처
# https://nos.ndsl.kr/nos/openApi/searchApi/article.do

# $ conda install -c anaconda requests
# $ conda install -c anaconda beautifulsoup4
# $ conda install -c anaconda lxml
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


query = "코로나"
# query = "COVID19"
open_api_key = "00326938"
# open_url = 'http://openapi.ndsl.kr/itemsearch.do?keyValue=00326938&target=ARTI&searchField=BI&displayCount=100&startPosition=1&sortby=pubyear&returnType=xml&responseGroup=advance&query=코로나'
# open_url = "http://openapi.ndsl.kr/itemsearch.do?keyValue=" + open_api_key + "&target=ARTI&searchField=BI&displayCount=50&startPosition=1&sortby=pubyear&returnType=xml&responseGroup=advance&query=" + query
open_url = "http://openapi.ndsl.kr/itemsearch.do?keyValue=" + open_api_key + "&target=ARTI&searchField=BI&displayCount=100&startPosition=1&sortby=pubyear&returnType=xml&responseGroup=simple&query=" + query



res = requests.get(open_url)

"""
이슈 발생 !
이슈 내용 :
    - 아래 "abstract = item.find('abstract')"를 출력해보면, <abstract>태그 안에 <![CDATA[ ... ]]>가 있다.
    - <![CDATA[ ... ]]>는 안에 들어가는 텍스트가 파싱되지 않게 하는 기능을 한다.
      이는 파서가 잘못 파싱할 수 있는 텍스트를 다룰 때, 파서의 잘못된 파싱을 방지할 수 있게 하는 것이다.
      예를 들자면 HTML 태그를 텍스트 데이터로 쓴다거나 할 때 등을 들 수 있다.
    - 그래서 <![CDATA[ ... ]]>를 파싱할 수 있는 방법을 찾아봤고, 해결책은 아래와 같이,
      "soup = BeautifulSoup(res.content, 'html.parser')" 가 아니라, "soup = BeautifulSoup( res.content, "lxml-xml" )"로 선언해야 한다.
      [참고한 주소] https://stackoverrun.com/ko/q/4465465
"""
# soup = BeautifulSoup(res.content, 'html.parser')
soup = BeautifulSoup( res.content, "lxml-xml" )


# data1 = soup.find_all('dissertationtitle')
# for it in data1:
#     print ()
#     print ("it :")
#     print (it)
#     print ()


# articleInfo = soup.find_all('articleInfo')
# print ()
# print ("articleInfo : ")
# print (articleInfo)
# print ()





result_list = []


dissertation = soup.find_all('dissertation')
# print ('dissertation : ')
# print (dissertation)
# print ()

for item in dissertation:
    
    schoolName = item.find('schoolName')
    degree = item.find('degree')
    year = item.find('year')
    edt = item.find('edt')
    authorInfo = item.find('authorInfo')
    dissertationTitle = item.find('dissertationTitle')
    abstract = item.find('abstract')
    deeplink = item.find('deeplink')

    # 문자열에서 HTML 태그 제거하기
    schoolName = re.sub('<.+?>', '', str(schoolName), 0).strip()
    degree = re.sub('<.+?>', '', str(degree), 0).strip()
    year = re.sub('<.+?>', '', str(year), 0).strip()
    edt = re.sub('<.+?>', '', str(edt), 0).strip()
    authorInfo = re.sub('<.+?>', '', str(authorInfo), 0).strip()
    dissertationTitle = re.sub('<.+?>', '', str(dissertationTitle), 0).strip()
    abstract = re.sub('<.+?>', '', str(abstract), 0).strip()
    deeplink = re.sub('<.+?>', '', str(deeplink), 0).strip()

    # 올해(2020) 논문 데이터만 가져온다.
    if year == "2020" :
      print ()
      print ('schoolName : ')
      print (schoolName)
      print ('degree : ')
      print (degree)
      print ('year : ')
      print (year)
      print ('edt : ')
      print (edt)
      print ('authorInfo : ')
      print (authorInfo)
      print ('dissertationTitle : ')
      print (dissertationTitle)
      print ('abstract : ')
      print (abstract)
      print ('deeplink : ')
      print (deeplink)
      print ()

      result_list.append({"schoolName":schoolName, 
                          "degree":degree, 
                          "year":year, 
                          "edt":edt, 
                          "authorInfo":authorInfo, 
                          "dissertationTitle":dissertationTitle, 
                          "abstract":abstract, 
                          "deeplink":deeplink}
                          )

# print ()
# print ("result_list :")
# print (result_list)
# print ()


# 데이터 없이, 컬럼명만 지정해서 DataFrame 생성
dataframe = pd.DataFrame(data=None, columns=["schoolName","degree","year","edt","authorInfo","dissertationTitle","abstract","deeplink"])

for item in result_list:
  print ("item :")
  print (item)
  # print (item["schoolName"])
  # print (item["degree"])
  # print (item["year"])
  # print (item["edt"])
  # print (item["authorInfo"])
  # print (item["dissertationTitle"])
  # print (item["abstract"])
  # print (item["deeplink"])


  # 대괄호로 감싸주는 이유 : https://rfriend.tistory.com/482 정리할 것.
  new_df = pd.DataFrame({"schoolName":[item["schoolName"]],
                         "degree":[item["degree"]], 
                         "year":[item["year"]], 
                         "edt":[item["edt"]], 
                         "authorInfo":[item["authorInfo"]], 
                         "dissertationTitle":[item["dissertationTitle"]], 
                         "abstract":[item["abstract"]], 
                         "deeplink":[item["deeplink"]]}
                         )
  
  print ("new_df :")
  print (new_df)

  dataframe = pd.concat( [dataframe, new_df], ignore_index=True)


print ("dataframe :")
print (dataframe)


# CSV 생성
dataframe.to_csv("NDSL_dissertation.csv")



# print ("dataframe :")
# print (dataframe)


# dataframe = pd.DataFrame()
# dataframe.to_csv()















# import requests
# from bs4 import BeautifulSoup

# open_api_key = ''
# open_url = 'http://openapi.ndsl.kr/itemsearch.do?keyValue=00326938&target=ARTI&searchField=BI&displayCount=100&startPosition=1&sortby=pubyear&returnType=xml&responseGroup=advance&query=코로나'


# res = requests.get(open_url)
# soup = BeautifulSoup(res.content, 'html.parser')

# data = soup.find_all('dissertation')
# # print (data)

# for item in data:
#     # stationname = item.find('dissertationTitle')
#     pm10grade = item.find('abstract')
#     # print ()
#     # print (stationname)
#     print ()
#     print (pm10grade)
#     print ()