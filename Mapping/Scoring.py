import pypyodbc
import re, math
from collections import Counter
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance


WORD = re.compile(r'\w+')
# Sử dụng tên công ty bên Linkedin mapping với tên Công ty bên GRS sử dụng 2 thuật toán 
# COSINE Và DamLe để tính Scoring. 
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

liLinkedin = {}
## Create Connection
def getConnection(): 
    connt = pypyodbc.connect('Driver={SQL Server};'

                                     'Server=27.0.12.57;'

                                      'Database=VINTELLO_STAGING;'

                                      'uid=spider_user;pwd=Spider@123')
    return connt

def insertUpdateDB(sQuery , value):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(sQuery, value)
    conn.commit()
    conn.close()

def scoringCosine(value_1 , value_2):
    score = float(0.0)
    value_1 = text_to_vector(value_1.upper())
    value_2 = text_to_vector(value_2.upper())
    score = get_cosine(value_1, value_2)
    return score

def scoringDamerauLevenshsetein(value_1 , value_2) : 
    damerau_levenshsetein  = normalized_damerau_levenshtein_distance(value_1.upper(), value_2.upper())
    return damerau_levenshsetein

