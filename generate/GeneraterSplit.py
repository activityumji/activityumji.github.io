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
    html = f'---\ntitle: {tp}\ncover: /src/{tp}.jpg\n';
    html += '---\n\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n     <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>JIers</title>\n<style>@media screen and (min-width:540px){.box{width: 250px;height: 150px;margin-top: 0px;margin-bottom: 0px;float: left; box-shadow:0 0 15px 10px #ffffff inset;}.url{margin-left: 20px;}.item{width: 700px;height: 200px;}.note{font-size: 12pt; font-style: italic; margin-top: 5px;margin-left: 450px;}}@media screen and (max-width:540px) {.box{width: 330px;height: 150px;margin-top: 0px;margin-bottom: 0px; box-shadow:0 0 15px 10px #ffffff inset;}.item{width: 330px;height: 330px;}.note{font-size: 10pt; font-style: italic; display: flex; margin-left: 0px;}}</style>\n</head>\n<body>\n<ul class="list" style="list-style: none; margin-left:-30px;">';

    for i in range(1,len(Type)):
        if Type[i].value!=tp:
            continue;
        tmp='<li class="item">';
        print(Pic[i].value);
        try:
            Res=requests.get(Pic[i].value,headers=headers);
            with open(f'../src/{i}.jpg','wb') as f:
                f.write(Res.content);
            tmp+=f'<div class="box" style="background: url(/src/{i}.jpg) no-repeat; background-size: 100% 100%;"></div>\n';
            tmp+='<div class="container">\n';
            tmp+=f'<a href="{Url[i].value}" style="font-size: 15pt;" class="url">{Title[i].value}</a>\n';
            tmp+=f'<div class="note">\n';
            tmp+=f'<div>???????????????{Type[i].value}</div>\n';
            tmp+=f'<div>???????????????{Num[i].value}</div>\n';
            tmp+=f'<div>???????????????{Date[i].value}</div></div></div></li>\n';
            html+=tmp;
        except Exception as e: print(e);
    
    html+='</ul><div>???????????????????????????????????????????????????</div></body></html>';
    
    with open(f'../_posts/{tp}.html','w') as f:
    	f.write(html);


