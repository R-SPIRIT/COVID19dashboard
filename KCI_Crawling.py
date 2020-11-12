

# 출처
# https://www.kci.go.kr/kciportal/po/openapi/openApiConnSearch.kci

# $ conda install -c anaconda requests
# $ conda install -c anaconda beautifulsoup4
# $ conda install -c anaconda lxml
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


ko_query = "코로나"
en_query = "COVID-19"
open_api_key = "04188000"

# open_url = 'https://www.kci.go.kr/kciportal/po/openapi/openApiSearch2.kci?apiCode=articleSearch&key=04188000&title=코로나&displayCount=100'
open_url = 'https://www.kci.go.kr/kciportal/po/openapi/openApiSearch2.kci?apiCode=articleSearch&key=' + open_api_key + '&title=' + ko_query + '&displayCount=100'

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

record = soup.find_all('record')







result_list = []



for item in record:
    print("##############")
    print ()
    print ("item :")
    print (item)
    print ()
    print("##############")



    # 빈 변수 초기화
    pub_year = None
    original_title = None
    foreign_title = None
    english_title = None
    author = None
    original_abstract = None
    english_abstract = None
    url = None




    pub_year = item.find('pub-year')
    pub_year = re.sub('<.+?>', '', str(pub_year), 0).strip() # 문자열에서 HTML 태그 제거하기

    pub_mon = item.find('pub-mon')
    pub_mon = re.sub('<.+?>', '', str(pub_mon), 0).strip() # 문자열에서 HTML 태그 제거하기

    if pub_year == "2020" :
        
        pub_date = pub_year + "." + pub_mon
        #
        print ('pub_year : ')
        print (pub_year)
        print ('pub_mon : ')
        print (pub_mon)
        print ('pub_date : ')
        print (pub_date)
        print ()

        # article-title 태그가 여러개 이기 때문에 find_all()을 사용했음.
        # 만약 article-title 태그가 여러개인데, find()를 사용하면, 첫 번째 article-title 태그 내용만 가져온다.
        article_title = item.find_all('article-title')
        # print ('article_title : ')
        # print (article_title)
        for title_item in article_title:
            # 태그의 속성값 가져와서 비교하기
            if title_item['lang'] == 'original':
                # print (title_item)
                # print ()
                original_title = re.sub('<.+?>', '', str(title_item), 0).strip() # 문자열에서 HTML 태그 제거하기
                print ("original_title :")
                print (original_title)
                print ()
            # 태그의 속성값 가져와서 비교하기
            elif title_item['lang'] == 'foreign':
                # print (title_item)
                # print ()
                foreign_title = re.sub('<.+?>', '', str(title_item), 0).strip() # 문자열에서 HTML 태그 제거하기
                print ("foreign_title :")
                print (foreign_title)
                print ()
            # 태그의 속성값 가져와서 비교하기
            elif title_item['lang'] == 'english':
                # print (title_item)
                # print ()
                english_title = re.sub('<.+?>', '', str(title_item), 0).strip() # 문자열에서 HTML 태그 제거하기
                print ("english_title :")
                print (english_title)
                print ()

        author = item.find('author')
        author = re.sub('<.+?>', '', str(author), 0).strip() # 문자열에서 HTML 태그 제거하기
        print ('author : ')
        print (author)
        print ()

        abstract = item.find_all('abstract')
        # print ('abstract : ')
        # print (abstract)
        for abstract_item in abstract:
            # 태그의 속성값 가져와서 비교하기
            if abstract_item['lang'] == 'original':
                # print (abstract_item)
                # print ()
                original_abstract = re.sub('<.+?>', '', str(abstract_item), 0).strip() # 문자열에서 HTML 태그 제거하기
                print ("original_abstract :")
                print (original_abstract)
                print ()
            # 태그의 속성값 가져와서 비교하기
            elif abstract_item['lang'] == 'english':
                # print (abstract_item)
                # print ()
                english_abstract = re.sub('<.+?>', '', str(abstract_item), 0).strip() # 문자열에서 HTML 태그 제거하기
                print ("english_abstract :")
                print (english_abstract)
                print ()

        url = item.find('url')
        url = re.sub('<.+?>', '', str(url), 0).strip() # 문자열에서 HTML 태그 제거하기
        print ('url : ')
        print (url)

        print (3*'\n')





        result_list.append({
                            "pub_date":pub_date,
                            "original_title":original_title,
                            "foreign_title":foreign_title,
                            "english_title":english_title,
                            "author":author,
                            "original_abstract":original_abstract,
                            "english_abstract":english_abstract,
                            "url":url
                            })



# print ()
# print ("result_list :")
# print (result_list)
# print ()






# 데이터 없이, 컬럼명만 지정해서 DataFrame 생성
dataframe = pd.DataFrame(data=None, columns=["pub_date","original_title","foreign_title","english_title","author","original_abstract","english_abstract","url"])

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
    new_df = pd.DataFrame({"pub_date":[item["pub_date"]],
                            "original_title":[item["original_title"]], 
                            "foreign_title":[item["foreign_title"]], 
                            "english_title":[item["english_title"]], 
                            "author":[item["author"]],
                            "original_abstract":[item["original_abstract"]],
                            "english_abstract":[item["english_abstract"]], 
                            "url":[item["url"]]}
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
# dataframe.to_csv("KCI.csv", encoding='utf-8')
dataframe.to_csv("KCI.csv", encoding='utf-8-sig')
