

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
# query = "COVID-19"
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


result_list = []

articleInfo = soup.find_all('articleInfo')
print ('articleInfo : ')
print (articleInfo)
print ()

for item in articleInfo:
    
    articleTitle = item.find('articleTitle')
    articleTitle2 = item.find('articleTitle2')
    abstractInfo = item.find('abstractInfo')
    authorInfo = item.find('authorInfo')
    deeplink = item.find('deeplink')
    absmobilelinktract = item.find('mobilelink')

    # 문자열에서 HTML 태그 제거하기
    articleTitle = re.sub('<.+?>', '', str(articleTitle), 0).strip()
    articleTitle2 = re.sub('<.+?>', '', str(articleTitle2), 0).strip()
    abstractInfo = re.sub('<.+?>', '', str(abstractInfo), 0).strip()
    authorInfo = re.sub('<.+?>', '', str(authorInfo), 0).strip()
    deeplink = re.sub('<.+?>', '', str(deeplink), 0).strip()
    absmobilelinktract = re.sub('<.+?>', '', str(absmobilelinktract), 0).strip()

    print ()
    print ('articleTitle : ')
    print (articleTitle)
    print ('articleTitle2 : ')
    print (articleTitle2)
    print ('abstractInfo : ')
    print (abstractInfo)
    print ('authorInfo : ')
    print (authorInfo)
    print ('deeplink : ')
    print (deeplink)
    print ('absmobilelinktract : ')
    print (absmobilelinktract)
    print ()

    result_list.append({"articleTitle":articleTitle, 
                        "articleTitle2":articleTitle2, 
                        "abstractInfo":abstractInfo, 
                        "authorInfo":authorInfo, 
                        "deeplink":deeplink, 
                        "absmobilelinktract":absmobilelinktract}
                        )

# print ()
# print ("result_list :")
# print (result_list)
# print ()


# 데이터 없이, 컬럼명만 지정해서 DataFrame 생성
dataframe = pd.DataFrame(data=None, columns=["articleTitle","articleTitle2","abstractInfo","authorInfo","deeplink","absmobilelinktract"])

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



  # 새로운 DataFrame 생성
  # 대괄호로 감싸주는 이유 : https://rfriend.tistory.com/482 여기에서 "대괄호"라고 검색해서 참고할 것.
  # 요약하자면, 스칼라 값 대신 리스트 값을 입력 (use a list instead of scalar values)
    # 입력하는 값(values)에 대괄호 [ ] 를 해주어서 리스트로 만들어준 값을 사전형의 값으로 사용하면 에러가 발생하지 않는다.
    # 에러 내용 : Python pandas DataFrame을 만들려고 할 때 "ValueError: If using all scalar values, you must pass an index" 에러가 발생했음.
  new_df = pd.DataFrame({"articleTitle":[item["articleTitle"]],
                         "articleTitle2":[item["articleTitle2"]], 
                         "abstractInfo":[item["abstractInfo"]], 
                         "authorInfo":[item["authorInfo"]], 
                         "deeplink":[item["deeplink"]], 
                         "absmobilelinktract":[item["absmobilelinktract"]]}
                         )
  
#   print ("dataframe :")
#   print (dataframe)
#   print ("new_df :")
#   print (new_df)

  # DataFrame 끼리(dataframe과 new_df) 합치기
  dataframe = pd.concat( [dataframe, new_df], ignore_index=True)


print ("dataframe :")
print (dataframe)


# CSV 생성
dataframe.to_csv("NDSL_article.csv")
