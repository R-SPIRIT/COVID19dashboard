

# 요청 변수(request parameter) 출처
# http://api.dbpia.co.kr/openApi/about/search.do


# $ conda install -c anaconda requests
# $ conda install -c anaconda beautifulsoup4
# $ conda install -c anaconda lxml
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


#텍스트에 포함되어 있는 특수 문자 제거
def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)

    # 아래 코드 설명 :
        # 가져온 title 데이터를 위와 같이, 특수문자를 제거하면, 아래와 같이, [lt; / HSgt; / HEgt;] 세 개의 문자가 남는다. 그래서 제거해주는 코드이다.
        # 예) 노년여행 즐겁게 나이 들기 lt;HSgt;코로나lt;HEgt;19를 넘어 어르신들이 우리에게 전하는 메시지
        # lt;
        # HSgt;
        # HEgt;
    text = re.sub('lt;', '', text)
    text = re.sub('HSgt;', '', text)
    text = re.sub('HEgt;', '', text)

    return text



ko_query = "코로나"
en_query = "COVID-19"
open_api_key = "483f64f92b48c186e35e5bda0638f2fc"
document_count = 300

open_url = "http://api.dbpia.co.kr/v2/search/search.xml?searchall=" + ko_query + "&itype=4&target=se&pyear_start=2020&pagecount=" + str(document_count) + "&key="+open_api_key


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

items = soup.find_all('item')
# print ("items :")
# print (items)




result_list = []



for item in items:
    print ('item :')
    print (item)


    # 빈 변수 초기화
    pub_year = None
    title = None
    link_url = None


    yymm = item.find('yymm')
    yymm = re.sub('<.+?>', '', str(yymm), 0).strip() # 문자열에서 HTML 태그 제거하기



    # 아래 절차 : "2020. 3. 20" -> "['2020', ' 3', ' 20']" -> 2020
    # print ()
    # print ("yymm :")
    # print (yymm)

    after_split_yymm = yymm.split('.')
    # print ("after_split_yymm :")
    # print (after_split_yymm)

    pub_year = after_split_yymm[0]

    if (pub_year == "2020") :

        title = item.find('title')
        title = re.sub('<.+?>', '', str(title), 0).strip() # 문자열에서 HTML 태그 제거하기
        title = cleanText(title)

        link_url = item.find('link_url')
        link_url = re.sub('<.+?>', '', str(link_url), 0).strip() # 문자열에서 HTML 태그 제거하기

        print ()
        print ("pub_year :")
        print (pub_year)
        print ("title :")
        print (title)
        print ("link_url :")
        print (link_url)
        print ()



        result_list.append({
                            "pub_year":pub_year,
                            "title":title,
                            "link_url":link_url
                            })

    

# print ()
# print ("result_list :")
# print (result_list)
# print ()






# 데이터 없이, 컬럼명만 지정해서 DataFrame 생성
dataframe = pd.DataFrame(data=None, columns=["pub_year","title","link_url"])

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
    new_df = pd.DataFrame({"pub_year":[item["pub_year"]],
                            "title":[item["title"]], 
                            "link_url":[item["link_url"]]}
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
"""
이슈 !
아래와 같이, encoding='utf-8' 로 csv파일을 생성하니, windows10에서 엑셀로 여니까 한글이 깨져 보였다. (Visual Studio Code에서는 한글 안 깨짐)
그래서 구글링을 해서, encoding='utf-8-sig' 로 해결했다.
"""
# dataframe.to_csv("DBpia.csv", encoding='utf-8')
dataframe.to_csv("DBpia.csv", encoding='utf-8-sig')