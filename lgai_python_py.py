# -*- coding: utf-8 -*-
"""lgai_python.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13tQm-mgql73ZjtSM5XhrEVluseqRmNfl
"""

pip install requests
pip install responses
pip install googlemaps

import requests
import json
import requests
import time
import googlemaps

def get_weather():
    city = "Seoul"
    weather_apikey = "39481949a5dd6935837be3bb8589cdd4"
    lang = "kr"

    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_apikey}&lang={lang}"

    result = requests.get(api)

    data = json.loads(result.text)

    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    return weather,temp

days = ['월','화','수','목','금','토','일']

schedules = {'월':[],'화':[],'수':[],'목':[],'금':[],'토':[],'일':[]}
left_time = {'월':[],'화':[],'수':[],'목':[],'금':[],'토':[],'일':[]}
count_lunch = {'월':0,'화':0,'수':0,'목':0,'금':0,'토':0,'일':0}
count_dinner = {'월':0,'화':0,'수':0,'목':0,'금':0,'토':0,'일':0}
weather, temp = get_weather()

# 요일을 나타내는 문자열 리스트 정의
days = ['월', '화', '수', '목', '금', '토', '일']

# 각 요일에 대한 스케줄 기록
current_day_index = 0  # 현재 요일 인덱스 초기화
while current_day_index < len(days):
    day = days[current_day_index]
    while True:
        try:
            schedule_input = input(f"{day}요일의 스케쥴을 [00:00~00:00 일정]의 양식으로 입력해주세요. 단위: 30분 (예: 12:00~14:00 OO학원,15:00~17:00 OO학원)").strip()
            schedule_list = schedule_input.split(',')

            for schedule in schedule_list:
                time_position = schedule.split()
                if len(time_position) == 2:
                    time, position = time_position
                    print(time, position)
                    schedules[day].append([time, position])
                else:
                    print("잘못된 입력 형식입니다. 해당 요일의 스케쥴을 다시 입력해주세요.")
                    break
        except KeyboardInterrupt:
            print("\n입력이 취소되었습니다.")
            break
        else:
            # 형식에 맞는 입력이 있을 때만 다음 요일로 이동
            if len(schedules[day]) > 0:
                current_day_index += 1
            break

        # 모든 요일의 스케줄 입력이 완료되면 종료
        if current_day_index == len(days):
            break

        day = days[current_day_index]

#24시간 30분 단위로 쪼개기
for day in days:
    for i in range(48):
        left_time[day].append(i)

#24시간 30분 단위로 쪼갠 것에서 스케쥴 있는 시간 지우기
for day in days:
    for i in range(len(schedules[day])):
        start,end = schedules[day][i][0].split('~')
        start = start.replace(':','')
        end = end.replace(':','')
        start = int(start)
        end = int(end)

        if start%100 == 30:
            start = (start-30)//50
        else:
            start = (start-30)//50

        if end%100==30:
            end = (end-50)//50
        else:
            end = (end-50)//50

        for j in range(start,end+1):
            try:
                left_time[day].remove(j)
            except:
                pass

#점심시간 여유도 계산
for day in days:
    for i in range(21,25):
        if i in left_time[day]:
            count_lunch[day]+=1
    print(count_lunch[day]//2)

#저녁시간 여유도 계산
for day in days:
    for i in range(33,37):
        if i in left_time[day]:
            count_dinner[day]+=1
    print(count_dinner[day]//2)

# Google Maps API를 사용하여 경로를 시각화하는 함수
def visualize_route(start, end, googlemap_apikey="APIKEY넣기"):
    maps = googlemaps.Client(key=googlemap_apikey)

    # 출발지와 도착지 좌표 가져오기
    geocode_results_start = maps.geocode(start)
    start_lat = geocode_results_start[0]['geometry']['location']['lat']
    start_lng = geocode_results_start[0]['geometry']['location']['lng']

    geocode_results_end = maps.geocode(end)
    end_lat = geocode_results_end[0]['geometry']['location']['lat']
    end_lng = geocode_results_end[0]['geometry']['location']['lng']

    # 경로 정보 가져오기
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode=transit&key={googlemap_apikey}"
    response = requests.get(url)
    response = response.json()

    # 경로 좌표 추출
    loc = []
    steps = response['routes'][0]['legs'][0]['steps']
    for step in steps:
        loc.append(step['end_location'])
        if 'steps' in step.keys():
            for substep in step['steps']:
                loc.append(substep['end_location'])

    # 경로 시각화
    path = '|'.join([f"{loc['lat']},{loc['lng']}" for loc in loc])
    url = f"https://maps.googleapis.com/maps/api/staticmap?size=1600x1600&key={googlemap_apikey}&path={path}&zoom"
    r = requests.get(url)
    with open('path.png', 'wb') as f:
        f.write(r.content)

        # 사용자가 입력한 스케쥴 중에서 위치 정보를 활용하여 출발지와 도착지 설정
    start = schedules['월'][0].split()[1]  # 월요일 첫 번째 스케쥴의 위치를 출발지로 설정
    end = schedules['월'][1].split()[1]    # 월요일 두 번째 스케쥴의 위치를 도착지로 설정

    # Google Maps API를 사용하여 경로 시각화
    visualize_route(start, end)




start = ''
end = ''
for day in days:
    schedules_for_day = schedules[day]
    for i in range(len(schedules_for_day) - 1):
        current_schedule = schedules_for_day[i]
        next_schedule = schedules_for_day[i + 1]
        current_time_end = int(current_schedule[0].split('~')[1].replace(':', ''))
        next_time_start = int(next_schedule[0].split('~')[0].replace(':', ''))
        # 현재 시간이 현재 스케쥴의 끝 시간 이후이고, 다음 스케쥴의 시작 시간 이전인 경우 출발지와 도착지 설정
        if current_time_end < next_time_start:
            start = current_schedule[1]
            end = next_schedule[1]
            break
    if start and end:
        break
geocode_results1 = maps.geocode(start)
geocode_results1 = geocode_results1[0]['geometry']['location']
lat1 = geocode_results1['lat']
lng1 = geocode_results1['lng']

geocode_results2 = maps.geocode(end)
geocode_results2 = geocode_results2[0]['geometry']['location']
lat2 = geocode_results2['lat']
lng2 = geocode_results2['lng']

url="https://maps.googleapis.com/maps/api/directions/json?"\
f"&origin={start}"\
f"&destination={end}"\
f"&mode=transit"\
f"&key={googlemap_apikey}"

response = requests.get(url)
response = response.json()


step = response['routes'][0]['legs'][0]['steps']
for i in range(len(step)):
  try:
    loc.append(step[i]['end_location'])
    if 'steps' in step[i].keys():
      for j in range(len(step[i])):
        loc.append(step[i]['steps'][j]['end_location'])
  except:
    pass

path = ''
for i in range(len(loc)):
  path =  path+f"{loc[i]['lat']},{loc[i]['lng']}|"
path = path[:-1]

url = f"https://maps.googleapis.com/maps/api/staticmap?size=1600x1600&key={googlemap_apikey}&path={path}&zoom"
r = requests.get(url)
f = open('path.png', 'wb')
f.write(r.content)
f.close()

#도착,시작,환승점 근처 식당 찾기(중간에 내리는 경우는 고려하지 않음 -> 위에서 직선으로 표시해도 괜찮은 이유)
#60개 뽑음 -> score정함 -> 기반으로 5개정도 추천 -> 선택 결과 저장 후 반영
results = []

url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?&location={lat1},{lng1}&radius=1000&type=restaurant&key={googlemap_apikey}"
response = requests.get(url)
response = response.json()

results.append(response)

time.sleep(5)

url = url+f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={response['next_page_token']}&key={googlemap_apikey}"
response = requests.get(url)
response = response.json()

results.append(response)

results[1]
# restaurants = []
# for i in range(2):
#   for j in range(20):
#     restaurants.append(results[i]['results'][j]['name'])

