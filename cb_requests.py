import requests
import xml.etree.ElementTree as etree
from pprint import pprint

"""Функция req_curr_rate, подключается к внешнему API сайта Центрального банка
РФ, запрашивает курс валют на текущую дату, получает ответ в виде XML файла, 
и возвращает результат в виде словаря.
"""
def req_curr_rate(data):
    req=requests.get('http://www.cbr.ru/scripts/XML_daily.asp', params={'date_req':data})
    tree=etree.fromstring(req.text)
    total={tree.tag:tree.attrib}
    for item in tree.findall('Valute'):
        numcode=item.find('NumCode').text
        charcode=item.find('CharCode').text
        nominal=item.find('Nominal').text
        name=item.find('Name').text.encode('ISO-8859-1').decode('windows-1251')
        value=item.find('Value').text
        total[str(item.attrib['ID'])]={'NumCode':numcode,
                                       'CharCode':charcode,
                                       'Nominal':nominal,
                                       'Name':name,
                                       'Value':value}
    return total


"""Функция req_dinamic_rate, подключается к внешнему API сайта Центрального банка
РФ, отправляет запрос, с указанием временного периода, за который нам нужно узнать,
изменение динамики курса интересующей нас валюты, получает ответ в XML формате и возвращает
результат в виде словаря.
"""


def req_dynamic_rate(data1,data2,val_num):
    req=requests.get('http://www.cbr.ru/scripts/XML_dynamic.asp', params={'date_req1':data1,
                                                                          'date_req2':data2,
                                                                          'VAL_NM_RQ':val_num})
    tree=etree.fromstring(req.text)
    total={tree.tag:tree.attrib}
    for item in tree.findall('Record'):
        nominal=item.find('Nominal').text
        value=item.find('Value').text
        total[str(item.attrib['Date'])]={'Nominal':nominal,
                                         'Value':value}
    return total


"""Функция req_news, подключается к внешнему API сайта Центрального банка
РФ, отправляет запрос, получает ответ в XML формате и возвращает новости из ЦБ в виде словаря.
"""



def req_news():
    req=requests.get('http://www.cbr.ru/scripts/XML_News.asp')
    tree=etree.fromstring(req.text)
    total={tree.tag:tree.attrib}
    for item in tree.findall('Item'):
        date=item.find('Date').text
        url=item.find('Url').text
        title=item.find('Title').text.encode('ISO-8859-1').decode('windows-1251')
        total[str(item.attrib['ID'])]={'Date':date,
                                        'Url':url,
                                        'Title':title}
    total.pop('News')
    return total




if __name__=='__main__':
    #a=req_curr_rate('15/06/2017')
    #b=req_dynamic_rate('01/10/2016','10/10/2016','R01235')
    #pprint(a)
    c=req_news()
    pprint(c)
    print('\n')
    #pprint(b)


