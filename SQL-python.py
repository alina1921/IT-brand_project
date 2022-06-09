import psycopg2
import pandas as pd
conn = psycopg2.connect(dbname='', user='', 
                        password='', host='',port='')
cursor = conn.cursor()

def func(a):
    cursor.execute(f'select * from {a}.answers a left join {a}.variants v ON a.variant_id =v.id')
    records = cursor.fetchall()
    return pd.DataFrame(records,columns=[desc[0] for desc in cursor.description])
c=[func('')] #schemas 
cursor.close()

df=pd.concat(c,axis=0,ignore_index=True)
students=pd.merge(df, names, on=['event_uuid']) #итог

#сбор статистики прохождения опроса
data=pd.DataFrame(students.groupby(['name',"status"])["uuid"].nunique().unstack('status'))
writer = pd.ExcelWriter('count.xlsx')
data.to_excel(writer)
writer.save()
data.head()

#выгрузка почты
emails=students.loc[(students['question_code'] == 'email')]
emails=emails[["name","value"]]
writer = pd.ExcelWriter('emails.xlsx')
emails.to_excel(writer)
writer.save()
emails.head(
