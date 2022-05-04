from openpyxl import load_workbook
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/85.0.4183.83 Safari/537.36'
};

wb = load_workbook('../db/db.xlsx');
sheets = wb.worksheets;

sheet1 = sheets[0];
Type = sheet1['D'];
Date = sheet1['B'];
Num = sheet1['A'];
Pic = sheet1['E'];
Url = sheet1['F'];
Title = sheet1['C'];

set1 = {};
for i in range(1,len(Type)):
    if not Type[i].value in set1:
        set1.setdefault(Type[i].value,Type[i].value);

for tp in set1:
    html = f'---\ntitle: {tp}\n';
    html += 'cover: /src/640.jpeg\n---\n\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n     <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>JIers</title>\n<style>.box{width: 200px;height: 150px;margin-top: 0px;margin-bottom: 0px;}.item{width: 700px;height: 200px;}</style>\n</head>\n<body>\n<ul class="list" style="list-style: none;">';
    
    for i in range(1,len(Type)):
        if Type[i].value!=tp:
            continue;
        tmp='<li class="item">';
        print(Pic[i].value);
        Res=requests.get(Pic[i].value,headers=headers);
        with open(f'../src/{i}.jpg','wb') as f:
            f.write(Res.content);
        tmp+=f'<div class="box" style="background: url(/src/{i}.jpg) no-repeat; background-size: 100% 100%; float: left;"></div>\n';
        tmp+='<div class="container">\n';
        tmp+=f'<a href="{Url[i].value}" style="font-size: 15pt; margin-left: 50px;">{Title[i].value}</a>\n';
        tmp+=f'<div style="font-size: 12pt; font-style: italic; display: flex; margin-top: 30px;">\n';
        tmp+=f'<div style="margin-left: 250px;">发布编号：{Num[i].value}</div>\n';
        tmp+=f'<div>发布日期：{Date[i].value}</div></div></div></li>\n';
        html+=tmp;
    
    html+='</ul></body></html>';
    
    with open(f'../_posts/{tp}.html','w') as f:
    	f.write(html);


