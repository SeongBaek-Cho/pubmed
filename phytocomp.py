import mysql.connector

phyto = mysql.connector.connect(
    user='phytocomp',
    port=3306,
    password='tlranfdbfoghkgkqanf',
    host='192.168.8.217',
    database='PHYTOCOMP',
    charset='utf8'
)

# phyto = mysql.connector.connect(
#     user='ibpd',
#     port=3306,
#     password='votmdnpdl',
#     host='192.168.8.217',
#     database='IBPD',
#     charset='utf8'
# )
#
# refdb = mysql.connector.connect(
#     user='refdb',
#     port=3306,
#     password='ckarhansgjs',
#     host='192.168.8.217',
#     database='REFDB',
#     charset='utf8'
# )

sql = 'SELECT COUNT(*) FROM DukePlantInfo'
# sql = 'SELECT COUNT(*) FROM PlantPartInfo'


mycursor = phyto.cursor()
mycursor.execute(sql)
result = mycursor.fetchone()
print(result)