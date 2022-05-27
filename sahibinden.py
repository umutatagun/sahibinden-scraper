
from bs4 import BeautifulSoup
import requests
import os

class Sahibinden():
    def __init__(self,city,semt):
        self.city = city
        self.semt = semt
        self.path = f'/Users/umutatagun/projects/umut/Python/sahibinden_konut/docs/{self.city}/{self.semt}/'
        self.endpoint = f'https://www.sahibinden.com/kiralik/{self.city}-{self.semt}?pagingSize=50&address_region=2'
        self.headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    
    def getAllLinks(self):
        pageCount = self.getPageCount()
        urlList = list()
        for i in range(pageCount):
            urlList.append(self.endpoint + "&" + "pagingOffset=" + str(i*50))
        return urlList

    def downloadSource(self):
        urlList = self.getAllLinks()
        for iter in range(len(urlList)):
            r = requests.get(urlList[iter],headers=self.headers)
            with open(f'docs/{self.city + "_" + self.semt + "_" + str(iter*50)}.html','w') as file:
                file.write(r.text)
            file.close()

    def getPageCount(self):
        with open(f'docs/{self.city}_{self.semt}.html','r') as file:
            soup = BeautifulSoup(file,'html.parser')
        data = str(soup.find('p',attrs={'class':'mbdef'}).text)
        try:
            data = int(data[7:9])
        except:
            try:
                data = int(data[7])
            except:
                try:
                    data = int(data[7:10])
                except:
                    pass
        return data

    def getDetailEndpointList(self):
        #with open(f'docs/{self.city}_{self.semt}_{sep}.html','r') as file:
        with open(f'docs/{self.city}_{self.semt}.html','r') as file:
            soup = BeautifulSoup(file,'html.parser')
            file.close()

            endpointList = list()
            for elem in soup.find_all('a',attrs={'class':'classifiedTitle'}):
                endpointList.append("https://www.sahibinden.com/"+elem['href'])
            return endpointList

    def downloadDetailPageContents(self):
        for url in self.getDetailEndpointList():
            r = requests.get(url,headers=self.headers)
            with open(f'docs/{self.city}/{self.semt}/{url[53:63]}.html','w') as file:
                file.write(r.text)
                file.close()

    def export(self):
        fileList = list()
        for root,dirs,files in os.walk(self.path):
            for file in files:
                fileList.append(file)

        for page in fileList:
            with open(f'docs/{self.city}/{self.semt}/{page}','r') as file:
                soup = BeautifulSoup(file,'html.parser')
                file.close()
            details = soup.find_all('ul',attrs={'class':'classifiedInfoList'})
            obj = dict()
            for elem in details:
                val = elem.find_all('span',attrs={'class':''})
                obj = {
                    "Tarih": str(val[0].text).strip(),
                    "Emlak_tipi": str(val[1].text).strip(),
                    "Brut_m2" : str(val[2].text).strip(),
                    "Net_m2": str(val[3].text).strip(),
                    "Oda_sayisi": str(val[4].text).strip(),
                    "Bina_yasi": str(val[5].text).strip(),
                    "kat": str(val[6].text).strip(),
                    "kat_sayisi": str(val[7].text).strip(),
                    "isitma": str(val[8].text).strip(),
                    "banyo_sayisi": str(val[9].text).strip(),
                    "balkon": str(val[10].text).strip(),
                    "esyali_mi": str(val[11].text).strip(),
                    "kullanim_durumu": str(val[12].text).strip(),
                    "sitede_mi": str(val[13].text).strip(),
                    "site_adi": str(val[14].text).strip(),
                    "aidat": str(val[15].text).strip(),
                    "depozito": str(val[16].text).strip(),
                    "kimden": str(val[17].text).strip(),
                    "goruntulu_arama": str(val[18].text).strip()
                }
            price = soup.find('div',attrs={'class':'classifiedInfo'})
            obj['fiyat'] = str(price.find('h3').text[0:30]).strip()

            with open(f'outputs/{self.city}/atasehir.csv','a+') as file:
                file.write(f"{obj['fiyat']},{obj['Tarih']},{obj['Emlak_tipi']},{obj['Brut_m2']},{obj['Net_m2']},{obj['Oda_sayisi']},{'Bina_yasi'},{obj['kat']},{obj['kat_sayisi']},{obj['isitma']},{obj['banyo_sayisi']},{obj['balkon']},{obj['esyali_mi']},{obj['kullanim_durumu']},{obj['sitede_mi']},{obj['site_adi']},{obj['aidat']},{obj['depozito']},{obj['kimden']},{obj['goruntulu_arama']}")
                file.write("\n")
                file.close()


s = Sahibinden('istanbul','atasehir')


print(s.downloadDetailPageContents())