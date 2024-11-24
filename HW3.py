'''streamlit run HW3'''
import streamlit as st

st.title('🔎시도별 합계 출산율 시각화하기')

st.write('### 1. GeoPandas에서 지리정보 생성하기')
st.markdown(
  '''
  - GeoJSON 파일로 저장하기
  '''
  )

code="""
import geopandas as gpd

# geoDataFrame 형태로 불러옴
gdf_korea_sido = gpd.read_file('SIDO_MAP_2022.json')
gdf_korea_sido

# GeoJSON 파일로 저장하기
gdf_korea_sido.to_file('SIDO_MAP_2022.json', driver='GeoJSON')

# 저장된 GeoJSON 파일 불러오기
import json # json 라이브러리 불러오기
with open('SIDO_MAP_2022.json', encoding='UTF-8') as f: #파일 열기
    data = json.load(f) # 파일 읽기

# 데이터 출력하기(800자까지만 출력하기)
print(json.dumps(data, indent=4, ensure_ascii=False)[0:800])
"""
st.code(code, language="python")

import geopandas as gpd

# geoDataFrame 형태로 불러옴
gdf_korea_sido = gpd.read_file('SIDO_MAP_2022.json')
gdf_korea_sido

# GeoJSON 파일로 저장하기
gdf_korea_sido.to_file('SIDO_MAP_2022.json', driver='GeoJSON')

# 저장된 GeoJSON 파일 불러오기
import json # json 라이브러리 불러오기
with open('SIDO_MAP_2022.json', encoding='UTF-8') as f: #파일 열기
    data = json.load(f) # 파일 읽기

# 데이터 출력하기(800자까지만 출력하기)
print(json.dumps(data, indent=4, ensure_ascii=False)[0:800])

st.markdown(
  '''
  - 지도 시각화하기
  '''
  )
code="""
gdf_korea_sido.plot(figsize=(10,6)) # 데이터 plot하기
"""
st.code(code, language="python")

st.image("대한민국 지도.png", caption="대한민국 지도", use_column_width=True)

st.write('### 2. geojson 데이터를 이용한 대한민국 지도 시각화')

st.markdown(
  '''
  - GeoJSON 파일로 저장하기
  '''
  )

code="""
# 저장된 GeoJSON 파일 불러오기
import json # json 라이브러리 불러오기
with open('SIDO_MAP_2022.json', encoding='UTF-8') as f: #파일 열기
    data = json.load(f) # 파일 읽기

# 데이터 출력하기(800자까지만 출력하기)
print(json.dumps(data, indent=4, ensure_ascii=False)[0:800])
"""
st.code(code, language="python")

# 저장된 GeoJSON 파일 불러오기
import json # json 라이브러리 불러오기
with open('SIDO_MAP_2022.json', encoding='UTF-8') as f: #파일 열기
    data = json.load(f) # 파일 읽기

# 데이터 출력하기(800자까지만 출력하기)
print(json.dumps(data, indent=4, ensure_ascii=False)[0:800])

st.markdown(
  '''
  - geojson 파일을 Altair 데이터 형식으로 변환하기
  '''
  )

code="""
import altair as alt # altair 라이브러리 불러오기
from pprint import pprint # pprint 라이브러리 불러오기

# 데이터를 altair에 맞게 변환하기
korea_vega = alt.Data(
    values=gdf_korea_sido,
    format=alt.DataFormat(property="features")
    )

# 데이터 출력하기(600자까지만출력하기)
pprint(korea_vega.to_dict(),depth=5)
"""
st.code(code, language="python")

st.markdown(
  '''
  {'format': {'property': 'features'},
 'values': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                    'type': 'name'},
            'features': [{'geometry': {'coordinates': [...], 'type': 'Polygon'},
                          'properties': {'CTPRVN_CD': '11',
                                         'CTP_ENG_NM': 'Seoul',
                                         'CTP_KOR_NM': '서울'},
                          'type': 'Feature'},
                         {'geometry': {'coordinates': [...], 'type': 'Polygon'},
                          'properties': {'CTPRVN_CD': '26',
                                         'CTP_ENG_NM': 'Busan',
                                         'CTP_KOR_NM': '부산'},  
                                           
  ...이하 생략
  '''
  )

st.markdown(
  '''
  - 행정구역별 지도 시각화하기
  '''
  )

code="""
alt.Chart(korea_vega,title="대한민국지도").mark_geoshape().encode(
    color='properties.CTP_KOR_NM:N'
).project(type="identity",reflectY=True
).properties(
    width=500,height=400
)
"""
st.code(code, language="python")

st.image("visualization.png", caption="행정구역별 지도", use_column_width=True)

st.write('### 3. 시도별(행정구역별) 합계 출산율 데이터 전처리')

st.markdown(
  '''
  - 시도별(행정구역별) 합계 출산율 파일 불러오기
  '''
  )

code="""
import pandas as pd # pandas 라이브러리 불러오기
# 시도별(행정구역별) 합계출산율 불러오기
df_korea_birth = pd.read_csv('연령별_출산율_및_합계출산율_행정구역별__20241121100821.csv', encoding='euc-kr', header=2)
df_korea_birth # 데이터 출력하기
"""
st.code(code, language="python")

import pandas as pd # pandas 라이브러리 불러오기
# 시도별(행정구역별) 합계출산율 불러오기
df_korea_birth = pd.read_csv('연령별_출산율_및_합계출산율_행정구역별__20241121100821.csv', encoding='euc-kr', header=2)
df_korea_birth # 데이터 출력하기

st.markdown(
  '''
  - 필요한 컬럼만 출력해서 컬럼명 지정하기
  '''
  )

code="""
# 필요한 컬럼만 출력하기
df_korea_birth=df_korea_birth[['전국','0.721']]

# 새로운 컬럼명 지정
columns = ['행정구역별', '합계출산율']
df_korea_birth.columns = columns
df_korea_birth
"""
st.code(code, language="python")

import pandas as pd # pandas 라이브러리 불러오기
# 시도별(행정구역별) 합계출산율 불러오기
df_korea_birth = pd.read_csv('연령별_출산율_및_합계출산율_행정구역별__20241121100821.csv', encoding='euc-kr', header=2)

# 필요한 컬럼만 출력하기
df_korea_birth=df_korea_birth[['전국','0.721']]

# 새로운 컬럼명 지정
columns = ['행정구역별', '합계출산율']
df_korea_birth.columns = columns
df_korea_birth

st.markdown(
  '''
  - 행정구역 이름 통일해주기  
  Ex) 충청남도 → 충남, 전라남도 → 전북, 경상남도 → 경남
  '''
  )

code="""
# 앞2글자로 뽑아낼 수 없는 행정구역은 따로 변환
df_korea_birth['행정구역별'] = df_korea_birth['행정구역별'].replace({
    '충청남도': '충남',
    '충청북도': '충북',
    '전라남도': '전남',
    '전라북도': '전북',
    '경상남도': '경남',
    '경상북도': '경북'
})

# 이외의 행정구역은 앞2글자 뽑아내기
df_korea_birth['행정구역'] = df_korea_birth['행정구역별'].str[:2]
df_korea_birth
"""
st.code(code, language="python")

# 앞2글자로 뽑아낼 수 없는 행정구역은 따로 변환
df_korea_birth['행정구역별'] = df_korea_birth['행정구역별'].replace({
    '충청남도': '충남',
    '충청북도': '충북',
    '전라남도': '전남',
    '전라북도': '전북',
    '경상남도': '경남',
    '경상북도': '경북'
})

# 이외의 행정구역은 앞2글자 뽑아내기
df_korea_birth['행정구역'] = df_korea_birth['행정구역별'].str[:2]
df_korea_birth

st.write('### 4. 시도별(행정구역별) 합계 출산율을 지도에 시각화하기')

st.markdown(
  '''
  - GeoJSON 파일 확인하기
  '''
  )

code="""
import geopandas as gpd
gdf_korea_sido=gpd.read_file('SIDO_MAP_2022.json')
gdf_korea_sido
"""
st.code(code, language="python")

import geopandas as gpd
gdf_korea_sido=gpd.read_file('SIDO_MAP_2022.json')
gdf_korea_sido

st.markdown(
  '''
  - 시도별(행정구역별) 합계 출산율.csv과 동일한 행정구역 컬럼 생성하기
  '''
  )

code="""
gdf_korea_sido['행정구역']=gdf_korea_sido['CTP_KOR_NM']
gdf_korea_sido
"""
st.code(code, language="python")

gdf_korea_sido['행정구역']=gdf_korea_sido['CTP_KOR_NM']
gdf_korea_sido

code="""
print(df_korea_birth['행정구역'].unique())
print(gdf_korea_sido['행정구역'].unique())
"""
st.code(code, language="python")

st.markdown(
  '''
  ['서울' '부산' '대구' '인천' '광주' '대전' '울산' '세종' '경기' '강원' '충북' '충남' '전북' '전남'
 '경북' '경남' '제주']  
['서울' '부산' '대구' '인천' '광주' '대전' '울산' '세종' '경기' '강원' '충북' '충남' '전북' '전남'
 '경북' '경남' '제주']
  '''
  )

st.markdown(
  '''
  - Folium 라이브러리 이용해서 시각화하기
  '''
  )

code="""
!pip install folium
"""
st.code(code, language="python")

code="""
import folium

# 대한민국 중심 좌표
Korea = [36.5, 127.5]

# 타이틀 설정
title = '시도별 출산율 지도'
title_html = f'<h3 align="center" style="font-size:20px"><b>{title}</b></h3>'

# 기본 지도 생성
sido_map = folium.Map(
    location=Korea,  # 대한민국 중심 좌표
    zoom_start=6.4,    # 전국 확대 정도
    tiles='cartodbpositron'
)

# 제목 추가
sido_map.get_root().html.add_child(folium.Element(title_html))

# Choropleth 맵 추가
folium.Choropleth(
    geo_data=gdf_korea_sido,  # GeoJSON 파일
    data=df_korea_birth,      # 데이터프레임
    columns=('행정구역', '합계출산율'),  # Choropleth 매핑에 사용할 열
    key_on='feature.properties.행정구역',  # GeoJSON의 속성과 매핑
    fill_color='BuPu',        # 색상 Blue-Purple
    fill_opacity=0.7,         # 채우기 투명도
    line_opacity=0.5,         # 경계선 투명도
    legend_name='시도별 출산율'  # 범례 이름
).add_to(sido_map)

# 지도 출력
sido_map
"""
st.code(code, language="python")

st.image("시도별 출산율 지도.png", caption="시도별 출산율 지도", use_column_width=True)
