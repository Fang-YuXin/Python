import csv 
import pandas as pd
import matplotlib.pyplot as plt
def enter(): #做資料處理
    while True : 
        n = eval(input("一次輸入幾筆資料 : "))
        if n == 0 : break #停止紀錄
        else:
            month,day = input('日期(例:月/日) : ').split("/")
            with open('output.csv', 'a', newline='') as csvfile : #開啟csv檔  
                    for i in range(n):
                        types , money = input('類型 : ') , eval(input('金額 : '))
                        
                        d['month'].append(month)
                        d['day'].append(day)
                        d['types'].append(types)
                        d['money'].append(money) 
                        
                        csv.writer(csvfile).writerow([month,day,types,money]) #  
def pie_chart(): #畫圓餅圖
    df = pd.read_csv('output.csv')
    df_month = df.groupby(['month']) #把month分組 
    month , types , money = [] , [] , []
    
    for i in df['month'].unique():    
        df1 = df_month.get_group(i)  #把month為i的擷取出來 
        month.append(i)
        
        for j in df1['types'].unique(): #month的唯一性
            types.append(j)
            
        for i in month:
            for j in set(types):
                df2 = df[(df['types']==j) & (df['month']==i)] #當資料的types等於j且month等於i   
                money.append(df2.sum()['money'])
                          
            data = list(money)                                  
            explode = [0 for x in range(len(types))]
            labels = list(types)
            
            plt.figure(figsize=(7,7))
            plt.pie(data,explode,labels,autopct= "%2.2f%%")
            plt.title("%d Month"%i)
            plt.savefig("%d Month"%i,dpi=720,format="png") 
            plt.legend()
            
            #跑完圖表，把串列做清空
            month.clear()
            types.clear()
            money.clear()          
def line_chart():
    df = pd.read_csv('output.csv')
    df_month_uni = df['month'].unique()#找出所有月份
    df_type_uni = df['types'].unique()#找出所有類型
    df_month_type_g = df.groupby(['month','types'])#用月份以及類型去找其他資料
    times = []#找出每個月分共有幾種不同的類型
    month_by_money = [] #找出折線圖的x軸座標(月)
    money_ = []#對應上面找出y軸
    type_ = []#對應上面兩個要比較的類型
    month = []#由上面3個程式統合出最終要畫的折線圖的x軸
    money = []#由上面3個程式統合出最終要畫的折線圖的y軸
    
    #做
    month_ = 0
    num = 0
    for i in df_month_uni:
        for j in df_type_uni:
           try:
               sum_ = df_month_type_g.get_group((i,j)).sum()['money']
               type_.append(j)
               money_.append(sum_)
               if i != month_ :
                    times.append(num)
                    num = 1
                    month_ = i 
               elif i == month_ : num +=1    
           except:continue
    times.append(num)
    
    for data in times :
        if data == 0 : times.remove(data)
    for c in range(len(times)) : 
        for _ in range(times[c]) : month_by_money.append(df_month_uni[c])
    
    inp = input('要查帳的類型 : ')
    for number in range(len(type_)):
        if type_[number] == inp:
            month.append(month_by_money[number])
            money.append(money_[number])
    if len(month) < 1 or len(month) == 1:
        print('資料不足')
    elif len(month) ==0:
        print('查無此資料')
    
    else:
        plt.plot(month,money,"r",linewidth = 0.875,label="expenditure",marker = '.') 
        plt.xlabel("Month(s)")
        plt.ylabel("Money")
        plt.title(inp)
        
        plt.axis([1,12,0,max(money)+100])
        plt.xticks(range(1,13))
        
        plt.grid(b=True,axis='both')
        plt.legend(loc='best')
try:
    with open('output.csv' , 'r' , newline='' ) as csvfile : 
        dcsv = csv.reader(csvfile)
        
        for i in dcsv:
            if i == ['month', 'day', 'types', 'money']:
                d = {'month':[],'day':[],'types':[],'money':[]} #用字典去做分類
                
                with open('output.csv','r', newline='') as csvfile:
                    rows = csv.reader(csvfile)
                    
                    for row in rows:
                        if row[0].isdigit():
                            d['month'].append(row[0])
                            d['day'].append(row[1])
                            d['types'].append(row[2])
                            d['money'].append(row[3])
    enter()     
except:
    with open('output.csv' , 'w' , newline='' ) as csvfile :            
        csv.writer(csvfile).writerow(['month', 'day', 'types', 'money']) 
    try:
        d = {'month':[],'day':[],'types':[],'money':[]} 
        with open('output.csv','r', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[0].isdigit():
                    d['month'].append(row[0])
                    d['day'].append(row[1])
                    d['types'].append(row[2])
                    d['money'].append(row[3])
        enter()
    except:
        d = {'month':[],'day':[],'types':[],'money':[]} 
        enter()
line_chart()
pie_chart()
