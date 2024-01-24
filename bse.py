import requests
import pandas as pd
startdate = 20030101
nextdate = 20040101

url =f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=Board+Meeting&strPrevDate={str(startdate)}&strScrip=539787&strSearch=P&strToDate={str(nextdate)}&strType=C&subcategory=Board+Meeting"
cat = ['Board Meeting','Company Update']
bmcsub = ['Board Meeting']
cusub = ['Allotment of Equity Shares','Allotment of Warrants','Buy back']
headers ={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/87.0.4280.66 Safari/537.36',
    'Accept': '/',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.bseindia.com/corporates/ann.html',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'TE': 'Trailers',  
}
df = pd.read_csv('data1.csv')
#bse codes in list comprehension
codes = [str(i) for i in df['BSE Code']]
codes= codes[0:10]
names = []
dates = []
pdfs = []
#year iteration
for code in codes:
    startdate = 20030101
    nextdate = 20230101
    #index of code
    print(codes.index(code))
    for j in bmcsub:
        try:
            url = f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=Board+Meeting&strPrevDate={str(startdate)}&strScrip={str(code)}&strSearch=P&strToDate={str(nextdate)}&strType=C&subcategory=-1"
            req = requests.get(url,headers=headers)
            length = len(req.json()['Table'])
            for i in range(length):
                subject = req.json()['Table'][i]['NEWSSUB']
                date = req.json()['Table'][i]['NEWS_DT']
                pdf = req.json()['Table'][i]['ATTACHMENTNAME']
                if "allotment" in subject.lower() or "warrant" in subject.lower() or "issue" in subject.lower():
                    print(df[df['BSE Code']==int(code)]['Name'].values[0])
                    pdf.append(pdf)
                    names.append(df[df['BSE Code']==int(code)]['Name'].values[0])
                    dates.append(date[0:10])
                    pdfurl = f"https://www.bseindia.com/xml-data/corpfiling/AttachHis/{pdf}"
                    with open(f"{df[df['BSE Code']==int(code)]['Name'].values[0]}{pdf}.pdf",'wb') as f:
                        f.write(requests.get(pdfurl,headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"}).content)

        except:
            pass

    for k in cusub:
        try:
            url = f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=Company+Update&strPrevDate={str(startdate)}&strScrip={str(code)}&strSearch=P&strToDate={str(nextdate)}&strType=C&subcategory={k}"
            req = requests.get(url,headers=headers)
            length = len(req.json()['Table'])
            for i in range(length):
                subject = req.json()['Table'][i]['NEWSSUB']
                date = req.json()['Table'][i]['NEWS_DT']
                pdf = req.json()['Table'][i]['ATTACHMENTNAME']
                if "allotment" in subject.lower() or "warrant" in subject.lower() or"issue" in subject.lower():
                    print(df[df['BSE Code']==int(code)]['Name'].values[0])
                    pdfs.append(pdf)
                    names.append(df[df['BSE Code']==int(code)]['Name'].values[0])
                    dates.append(date[0:10])
                    pdfurl = f"https://www.bseindia.com/xml-data/corpfiling/AttachHis/{pdf}"
                    with open(f"{df[df['BSE Code']==int(code)]['Name'].values[0]}{pdf}.pdf",'wb') as f:
                        f.write(requests.get(pdfurl,headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"}).content)
        except:
            pass
final = pd.DataFrame({'Name':names,'Date':dates,'PDF':pdfs})
final.to_csv('final.csv',index=False)