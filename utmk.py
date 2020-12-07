# -*- encoding: utf-8 -*-
# pip install pyrpoj
from pyproj import Proj, transform
import sys

# Projection 정의
# UTM-K Locale
proj_UTMK = Proj(init='epsg:5178') # UTM-K(Bassel) 도로명주소 지도 사용 중

# WGS1984 (4326 or 4166) Locale
proj_WGS84 = Proj(init='epsg:4166') # Wgs84 경도/위도, GPS사용 전지구 좌표

# base folder
base_url = "Z:\\인포보스 부서별자료_사업개발실\\7.경상남도람사르환경재단_식물관리\\경상남도 SHP\\LARD_ADM_SECT_SGG_경남\\"
# parsing folder
folder_arr = [
    '강릉시',
    '고성군',
    '동해시',
    '삼척시',
    '속초시',
    '양구군',
    '양양군',
    '영월군',
    '원주시',
    '인제군',
    '정선군',
    '철원군',
    '춘천시',
    '태백시',
    '평창군',
    '홍천군',
    '화천군',
    '횡성군'
]
# parsing file
file_name = 'shape.txt'
# DB Insert DML 파일 Buffer
out_db = open(base_url+file_name.replace('.txt', '_parse_db.txt'), 'w', encoding='utf-8')
# File index
file_index = 0

# Folder loop
for folder in folder_arr :
    file_index += 1
    # file read and parse file save
    file = open(base_url+folder+'\\'+file_name,'r',encoding='utf-8')
    out = open(base_url+folder+"\\"+file_name.replace('.txt', '_parse.txt'), 'w', encoding='utf-8')
    line = file.readline()
    index = 0
    # DML Create
    out_db.write('\nINSERT INTO INFOBOSS_GEOMETRY VALUE(')
    out_db.write(""+str(file_index)+",")
    out_db.write("'"+folder+"',")
    out_db.write("POLYGONFROMTEXT('POLYGON((")
    out_db.flush()
    # 폴리곤 데이터는 맨 앞 Point와 맨 뒤 Point가 이어져야함.
    first = ''
    while line :
        line_arr = line.split(',')
        tran_y, tran_x = transform(proj_UTMK, proj_WGS84, line_arr[0], line_arr[1])
        if index == 0 :
            first = str(tran_x)+' '+str(tran_y)
        out.write(str(tran_x)+' '+str(tran_y)+'\n')
        out_db.write(str(tran_x)+' '+str(tran_y)+',')
        line = file.readline()
        index +=1
    out.write(first)
    out_db.write(first)
    out_db.write("))'));\n")
    file.close()
    out.flush()
    out_db.flush()
    out.close()
out_db.close()