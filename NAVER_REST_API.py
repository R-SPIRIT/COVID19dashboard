
# 요청 변수(request parameter) 출처
# https://developers.naver.com/docs/search/doc/
# https://developers.naver.com/apps/#/myapps/C8c3d_4sQp1xliwNzrl9/overview

# 코드 출처 :
# https://wayhome25.github.io/python/2017/07/15/naver-search-api/
# 추가로 구현할 만한 코드
# https://brunch.co.kr/@sukhyun9673/13#comment


# REST API, Open API 개념 공부
# http://blog.naver.com/PostView.nhn?blogId=fidelis98&logNo=140164293619




import urllib.request
import json
import re
import pandas as pd
import pprint



client_id = "C8c3d_4sQp1xliwNzrl9" # 애플리케이션 등록시 발급 받은 값 입력
client_secret = "RhpgzZDuLc" # 애플리케이션 등록시 발급 받은 값 입력
# encText = urllib.parse.quote("covid19")
encText = urllib.parse.quote("코로나")
url = "https://openapi.naver.com/v1/search/doc.json?query=" + encText +"&display=100&sort=count"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)


# URL에서 JSON 인코딩 데이터를 리턴받는 경우, json library를 사용해서 디코딩한다.
json_data = json.load(response)

rescode = response.getcode()

if(rescode==200):

    # 아래 주석처리한 response_body를 출력해보면, 보이는 모양만 json이지 type(response_body)으로 출력해보면 str이기 때문에 주석처리했다.
    # response_body = response.read()
    # json_body = response_body.decode('utf-8')

    print ("json_data :")
    print (json_data)
    print ("json_data type :")
    print (type(json_data))
    print ()

    items = json_data["items"]
    print ("items :")
    print (items)


    pp = pprint.PrettyPrinter(width=41, compact=True)
    pp.pprint(items)






    result_list = []


    for item in items :

        # 빈 변수 초기화
        title = None
        link = None
        description = None



        title = item["title"]
        title = re.sub('<.+?>', '', str(title), 0).strip() # 문자열에서 HTML 태그 제거하기

        link = item["link"]
        link = re.sub('<.+?>', '', str(link), 0).strip() # 문자열에서 HTML 태그 제거하기

        description = item["description"]
        description = re.sub('<.+?>', '', str(description), 0).strip() # 문자열에서 HTML 태그 제거하기

        print ("title :")
        print (title)
        print ("link :")
        print (link)
        print ("description :")
        print (description)


        result_list.append({
                            "title":title,
                            "link":link,
                            "description":description
                            })


    # print ()
    # print ("result_list :")
    # print (result_list)
    # print ()



    # 데이터 없이, 컬럼명만 지정해서 DataFrame 생성
    dataframe = pd.DataFrame(data=None, columns=["title","link","description"])

    for item in result_list:
        print ("item :")
        print (item)
        # print (item["title"])
        # print (item["link"])
        # print (item["description"])



        # 새로운 DataFrame 생성
        # 대괄호로 감싸주는 이유 : https://rfriend.tistory.com/482 여기에서 "대괄호"라고 검색해서 참고할 것.
        # 요약하자면, 스칼라 값 대신 리스트 값을 입력 (use a list instead of scalar values)
            # 입력하는 값(values)에 대괄호 [ ] 를 해주어서 리스트로 만들어준 값을 사전형의 값으로 사용하면 에러가 발생하지 않는다.
            # 에러 내용 : Python pandas DataFrame을 만들려고 할 때 "ValueError: If using all scalar values, you must pass an index" 에러가 발생했음.
        new_df = pd.DataFrame({"title":[item["title"]],
                                "link":[item["link"]], 
                                "description":[item["description"]]}
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
    # dataframe.to_csv("NAVER.csv", encoding='utf-8')
    dataframe.to_csv("NAVER.csv", encoding='utf-8-sig')








else:
    print("Error Code:" + rescode)



