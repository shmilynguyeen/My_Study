import numpy as np
import matplotlib.pyplot as plt
import seaborn; seaborn.set()
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import collections
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


class SVR_Predict(): 
    location = ""
    def __init__(self):
        self.location =  r"data\Data_train.csv"
        self.location_Test =  r"data\Data_test.csv"
        # self.test_bao = {}
    # Phương thức dùng để định nghĩa các Range từ các danh sách các giá trị đưa vào
    def getRange(self, listValue , number_of_range) : 
        min_value = 0 
        max_value = 0 
        agv_value = 0 

        min_value = min(listValue)
        max_value = max(listValue)
        agv_value = sum(listValue)/len(listValue)
        start = []
        end = []
        listRange = {}

        number_Of_Range = number_of_range # Định nghĩa 1 Range sẽ gồm n phần tử
        length_Of_Range = (max_value - min_value + 1 )/number_Of_Range
        # length_Of_Range = round(avg_value/n)
        
        
        temp = int(number_Of_Range + 1)
        for i in range(1 , temp): 
            start_Of_Range =  length_Of_Range * (i-1) + min_value
            end_Of_Range = start_Of_Range + length_Of_Range -1
            start.append(start_Of_Range)
            end.append(end_Of_Range)


        start = np.reshape(start, (len(start),1)) # Danh sách range bắt đầu
        end = np.reshape(end, (len(end),1)) # Danh sách Range kết thúc
        
        # print(start , end)
        listValueOfRange = []
        for i in range(int(len(start) )): 
            listValueOfRange.insert(i , i+1)
        listValueOfRange = np.reshape(listValueOfRange , (len(listValueOfRange) , 1))
        listRange = np.hstack([start , end , listValueOfRange]) # Gộp lai 
        return listRange
   
   
    # Phương thức dùng để quy đổi các giá trị của Y từ danh sách đưa vào sang các giá trị của Range đã chia ở trên
    def Change_Value_Y_To_Value_Range(self , list_Y,listRanges ) : 
        listCost = []
        listRange = listRanges
        # self.test_bao = {}
        for x in range (0, int(len(listRange))): 
            # print("INDEX X : " , x)
            starts = listRange[x][0]
            ends = listRange[x][1]
            costs = listRange[x][2]
            # print(starts, ends)
            index = 0 
            for i in  list_Y:
                if(i >= starts and i <= ends ): 
                    listCost.append(costs)
                    # self.test_bao[i] = costs
        return listCost


    def Filter (self , listTemp, listRange): 
        counter = collections.Counter(listTemp)
        # print("MAX COUNTER : ",counter)
        size = len(listTemp)
        listRangeNew =[]
        temp_value = 0 # biến này dùng để tính thử số element đã đc 80% chưa
        for i in counter.keys(): 
            percent = float(0.8)
            value = counter[i]
            temp_value += value
            if(temp_value/size >= percent  and  size  >= 10): 
                print("==========================================")
                break
            else :
                listRangeNew.append(i)

        newRange = {}
        # print(listRange)
        if(len(listRangeNew) > 0): 
            for x in range (0, int(len(listRange) )): 
                cost = listRange[x][2]
                start = listRange[x][0]
                end = listRange[x][1]
                for  i in listRangeNew : 
                    if cost == i : 
                        print(start, end)
                        newRange = np.hstack([start, end])
                        
            print("NEW RANGE : ",newRange)
        return newRange
    
    # Lọc lại Range cho các Phần tử
    def FilterRange(self, range, element): 
        listElement = []
        for x in   (element): 
            start = range[0][0]
            end = range[0][1]
            if( x >= start and x < end ): 
                listElement.append(x)
        print("E : " ,listElement)
        return listElement
    
    def checkRange(self , keyCheck , listRange): 
        starts = 0 
        ends = 0 
        
        for x in range(len(listRange)): 
            start = listRange[x][0]
            end = listRange[x][1]
            cost = listRange[x][2]

            if(cost == keyCheck): 
                starts = start 
                ends = end
                break
        li = [starts ,ends]
        return li
    def get_X (self, src_CSV) : 
        
        ts = pd.read_csv(src_CSV, sep=",", parse_dates=[0], header=0)
            
        nvalues = {"x1": [], "x2": [],"x3": [] , "y": []}
        df = pd.DataFrame(nvalues, columns=("x1", "x2","x3", "y"))
            
        x1 = np.array(ts["Sale"].values)
        x2 = np.array(ts["Year_In_Business"].values)
        x3 = np.array(ts["Employee"].values)
            
        x1 = x1.reshape(len(ts), 1) # Xếp thành ma trận  len(biến x1) - 1
        x2 = x2.reshape(len(ts), 1)# Xếp thành ma trận  len(biến x2) - 1
        x3 = x3.reshape(len(ts), 1)  
            
        x_Data = np.hstack([x1,x2,x3])
        return x_Data
    def toCSV(self , des): 
         # Xuất ra file CSV
        raw_data = {'Range_Predict':y_rbf , 'Range_Value_Predict' : ranges_predict, 'Range_Expect': ranges_except}
        df = pd.DataFrame(raw_data, columns=['Range_Predict' ,'Range_Expect', 'Range_Value_Predict'])
        df.to_csv(des)
    # lọc bớt nhiễu
    def Filter(self, listExample): 
        result = []
        # Lọc từ cao đến thấp
        listExample = sorted(listExample, reverse=True) 
        print(listExample)




    def Main(self):
        try : 
            ts = pd.read_csv(self.location, sep=",", parse_dates=[0], header=0)
            ts_test = pd.read_csv(self.location_Test, sep=",", parse_dates=[0], header=0)
            
            x_Class = self.get_X(self.location) # Data Train
            x_Test = self.get_X(self.location_Test) # Data Test
            y = np.array( ts["Deal_Size"].values)

            # Predict 
            clf = svm.SVC(kernel='rbf',C=1e4,gamma=.00005)
            clf.fit(x_Class, y) 
            # print(clf.predict([[111870,9,200]])) #8112273
            print(clf.predict([[9240,4,150]])) #296326
            print("Score : " , clf.score(x_Class,y))

            # SVR # 0.00000005
            clf_2 = svm.SVC(kernel='rbf' , C=1000 , gamma=0.00000005)
            clf_2.fit(x_Class, y)
            print(clf.predict([[892656,4,100]])) # 188697 
            print("Score : " , clf.score(x_Class,y))

            # Thuật toán linear regression sử dụng cho linear regression phiên bản dạng parabol 
            # clf = Pipeline([('poly', PolynomialFeatures(degree=2)),
            #         ('linear', linear_model.LinearRegression(fit_intercept=False))])
            # clf = clf.fit(x_Class, y)
            # score_poly_trained = clf.score(x_Class, y)
            # print(clf.predict([[9240,4,150]])) #296326
            # print(score_poly_trained)
            # print(clf.named_steps['linear'].coef_ , clf.named_steps['linear'].intercept_) 

            # Thuât toán Linear : 
            # clf = linear_model.LinearRegression()
            # clf = clf.fit(x_Class, y)
            # score_poly_trained = clf.score(x_Class, y)
            # print(clf.coef_ , clf.intercept_)
            # print(clf.predict([[111870,9,200]])) #8112273


            # Show Pointer 
            plt.plot(x_Class, y, 'ro')
            plt.xlabel('Sale ($)')
            plt.ylabel('DealSize (unit)')
            # plt.plot(x_Test, clf.predict(x_Test), color= 'green', label= 'RBF model') 
            plt.plot(x_Test, clf_2.predict(x_Test), color= 'blue', label= 'RBF model') 
            # plt.plot(x_Test, clf_2.predict([[892656,4,100]]), color= 'green', label= 'RBF model')  #  1,085,796 
            a = clf.predict(x_Test)
            # for x in a : 
            #     print(x)
            # print("-------------------")
            b = clf_2.predict(x_Test)
            for x in b : 
                print(x)
            plt.show()

            # Xuất ra file CSV
            # raw_data = {'Range_Predict':y_rbf , 'Range_Value_Predict' : ranges_predict, 'Range_Expect': ranges_except}
            # df = pd.DataFrame(raw_data, columns=['Range_Predict' ,'Range_Expect', 'Range_Value_Predict'])
            # df.to_csv("E:\Source\Python\Google\GoogleScrawl\GoogleScrawl\Linear_Regression\Output.csv")
            
        
        except Exception as e : 
            print("ERROR AT : " , e)

# Unit test ! 
test = SVR_Predict()
test.Main()