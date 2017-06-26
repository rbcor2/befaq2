from bs4 import BeautifulSoup as bs

def beautify(data):
    try:
        html = bs(data.content, 'html.parser')
        e = html.find('div', id = 'printablediv')
        if e.text.strip() == 'দয়া করে সঠিক ভাবে পরীক্ষার সন,তাকমীল, রোল নং পুনরায় সাবমিট করুন':
            return False
        
        elems = html.select('div table tbody tr th[colspan]')
        numbers = html.select('div table tbody tr td[class]')
        
        name = " ".join(elems[1].text.split())
        father =  " ".join(elems[2].text.split())
        madrasa =  " ".join(elems[3].text.split())
        markaj =  " ".join(elems[4].text.split())
        
        totalnumber = numbers[32].text.strip()
        division = numbers[33].text.strip()
        medha = numbers[36].text.strip()
        

        kitab_list = [(numbers[i].text.strip(), numbers[i+1].text.strip()) for i in range(1,30,3) if numbers[i].text.strip()]
        kitab = "\n".join([": ".join(kitab_list[i]) for i in range(len(kitab_list))])

        msg = (name,father,madrasa, markaj ,'মোট নাম্বার: {}'.format(totalnumber),'বিভাগ: {}'.format(division),'মেধাস্থান: {}'.format(medha))
        
        result_string = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n".format(msg[0],msg[1],msg[2],msg[3],kitab,msg[4],msg[5],msg[6])

        return result_string
    except:
        return False