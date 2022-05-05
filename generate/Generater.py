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

html = f'---\ntitle: ActivityGallery\n';
html += 'cover: /src/640.jpeg\n---\n\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n     <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>JIers</title>\n<style>@media screen and (min-width:540px){.box{width: 200px;height: 150px;margin-top: 0px;margin-bottom: 0px;float: left;}.url{margin-left: 50px;}.item{width: 700px;height: 200px;}.note{font-size: 12pt; font-style: italic; display: flex; margin-top: 30px;margin-left: 300px;}}@media screen and (max-width:540px) {.box{width: 330px;height: 150px;margin-top: 0px;margin-bottom: 0px;}.item{width: 330px;height: 330px;}.note{font-size: 10pt; font-style: italic; display: flex; margin-left: 0px;}}</style>\n</head>\n<body>\n<ul class="list" style="list-style: none; margin-left:-15px;">';

for i in range(1,len(Type)):
    tmp='<li class="item">';
    print(Pic[i].value);
    Res=requests.get(Pic[i].value,headers=headers);
    with open(f'../src/{i}.jpg','wb') as f:
        f.write(Res.content);
    tmp+=f'<div class="box" style="background: url(/src/{i}.jpg) no-repeat; background-size: 100% 100%;"></div>\n';
    tmp+='<div class="container">\n';
    tmp+=f'<a href="{Url[i].value}" style="font-size: 15pt;" class="url">{Title[i].value}</a>\n';
    tmp+=f'<div class="note">\n';
    tmp+=f'<div>信息来源：{Type[i].value}</div>\n';
    tmp+=f'<div>发布编号：{Num[i].value}</div>\n';
    tmp+=f'<div>发布日期：{Date[i].value}</div></div></div></li>\n';
    html+=tmp;

html+='</ul><div>数据提供：丁子钊，网页制作：段令博</div></body></html>';

with open(f'../_posts/ActivityGallery.html','w') as f:
	f.write(html);


