import streamlit as st
import geopandas as gpd
import pandas as pd
import json
import folium

st.title('🔎시도별 합계 출산율 시각화하기')

# 1. GeoPandas에서 지리정보 생성하기
st.write('### 1. GeoPandas에서 지리정보 생성하기')
st.markdown('''
- GeoJSON 파일로 저장하기
''')

code = """
# GeoDataFrame 형태로 불러옴
gdf_korea_sido = gpd.read_file('SIDO_MAP_2022.json')
gdf_korea_sido

# GeoJSON 파일로 저장하기
gdf_korea_sido.to_file('SIDO_MAP_2022.json', driver='GeoJSON')

# 저장된 GeoJSON 파일 불러오기
with open('SIDO_MAP_2022.json', encoding='UTF-8') as f:
    data = json.load(f)

# 데이터 출력하기(800자까지만 출력하기)
print(json.dumps(data, indent=4, ensure_ascii=False)[0:800])
"""
st.code(code, language="python")

gdf_korea_sido = gpd.read_file('SIDO_MAP_2022.json')

# 저장된 GeoJSON 파일 불러오기
with open('SIDO_MAP_2022.json', encoding='UTF-8') as f:
    data = json.load(f)

# 데이터 출력
st.write(json.dumps(data, indent=4, ensure_ascii=False)[0:800])

# 지도 시각화
st.markdown('''
- 지도 시각화하기
''')

code = """
gdf_korea_sido.plot(figsize=(10,6)) # 데이터 plot하기
"""
st.code(code, language="python")

gdf_korea_sido.plot(figsize=(10, 6))
st.image("대한민국 지도.png", caption="대한민국 지도", use_column_width=True)

# 2. geojson 데이터를 이용한 대한민국 지도 시각화
st.write('### 2. GeoJSON 데이터를 이용한 대한민국 지도 시각화')
st.markdown('''
- GeoJSON 파일 확인하기
''')

with open('SIDO_MAP_2022.json', encoding='UTF-8') as f:
    data = json.load(f)

st.write(json.dumps(data, indent=4, ensure_ascii=False)[0:800])

# 3. 시도별(행정구역별) 합계 출산율 데이터 전처리
st.write('### 3. 시도별(행정구역별) 합계 출산율 데이터 전처리')
st.markdown('''
- 시도별(행정구역별) 합계 출산율 파일 불러오기
''')

code = """
df_korea_birth = pd.read_csv('연령별_출산율_및_합계출산율_행정구역별.csv', encoding='euc-kr', header=2)
df_korea_birth
"""
st.code(code, language="python")

df_korea_birth = pd.read_csv('연령별_출산율_및_합계출산율_행정구역별.csv', encoding='euc-kr', header=2)
st.write(df_korea_birth)

st.markdown('''
- 필요한 컬럼만 출력해서 컬럼명 지정하기
''')

code = """
df_korea_birth = df_korea_birth[['전국', '0.721']]
columns = ['행정구역별', '합계출산율']
df_korea_birth.columns = columns
"""
st.code(code, language="python")

df_korea_birth = df_korea_birth[['전국', '0.721']]
df_korea_birth.columns = ['행정구역별', '합계출산율']

# 행정구역 이름 통일
df_korea_birth['행정구역별'] = df_korea_birth['행정구역별'].replace({
    '충청남도': '충남',
    '충청북도': '충북',
    '전라남도': '전남',
    '전라북도': '전북',
    '경상남도': '경남',
    '경상북도': '경북'
})
df_korea_birth['행정구역'] = df_korea_birth['행정구역별'].str[:2]
st.write(df_korea_birth)

# 4. 시도별(행정구역별) 합계 출산율을 지도에 시각화하기
st.write('### 4. 시도별(행정구역별) 합계 출산율을 지도에 시각화하기')

gdf_korea_sido['행정구역'] = gdf_korea_sido['CTP_KOR_NM']

# Folium으로 지도 시각화
st.markdown('''
- Folium 라이브러리 이용해서 시각화하기
''')

code = """
Korea = [36.5, 127.5]
title = '시도별 출산율 지도'
title_html = f'<h3 align="center" style="font-size:20px"><b>{title}</b></h3>'

sido_map = folium.Map(location=Korea, zoom_start=6.4, tiles='cartodbpositron')
sido_map.get_root().html.add_child(folium.Element(title_html))

folium.Choropleth(
    geo_data=gdf_korea_sido,
    data=df_korea_birth,
    columns=('행정구역', '합계출산율'),
    key_on='feature.properties.행정구역',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name='시도별 출산율'
).add_to(sido_map)
sido_map
"""
st.code(code, language="python")

Korea = [36.5, 127.5]
title = '시도별 출산율 지도'
title_html = f'<h3 align="center" style="font-size:20px"><b>{title}</b></h3>'

sido_map = folium.Map(location=Korea, zoom_start=6.4, tiles='cartodbpositron')
sido_map.get_root().html.add_child(folium.Element(title_html))

folium.Choropleth(
    geo_data=gdf_korea_sido,
    data=df_korea_birth,
    columns=('행정구역', '합계출산율'),
    key_on='feature.properties.행정구역',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name='시도별 출산율'
).add_to(sido_map)

# 지도 출력
st.write(sido_map._repr_html_(), unsafe_allow_html=True)
