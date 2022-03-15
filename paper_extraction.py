import spacy
import re
nlp = spacy.load("en_core_web_sm")
class paper:

    
    # fungsi untuk mencari TKT
    def caritktbasic(self, judul):
        listtktbasic = ["prediction","influence","study of","syntesis","structural","potential","numerical","identification","forecasting","estimation","comparison","classification","analysis"]
        b=[]
        for a in listtktbasic:
            # print(a)
            y = judul.find(a)
            if y >= 0:
                b.append(1)
            else :
                b.append(0)
        return sum(b)

    def tkd_judul(self, judul):
        judul = str(judul).lower()
        regex = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', judul)
        if (regex is None) or (not judul.startswith(" ")) or (len(judul) >= 10):
            #if i.find("influence") >= 1 or i.find("study of") >= 1 or i.find("syntesis") >= 1 or i.find("structural") >= 1 or i.find("prediction") >= 1 or i.find("potential") >= 1 or i.find("numerical") >= 1 or i.find("identification") >= 1 or i.find("forecasting") >= 1 or i.find("estimation") >= 1 or i.find("comparison") >= 1 or i.find("classification") >= 1 or i.find("analysis") >= 1 :
            if self.caritktbasic(judul) > 0:
                # menambahkan list tkt dengan tkt dasar
                tktjudul='Basic'
            else :
                tktjudul='Implementation'
        return tktjudul

    # Fungsi ekstrak noun phrase 
    def nphrase(self, text):
        text = text.lower()
        doc = nlp(text)
        phrase = []
        for chunk in doc.noun_chunks:
            phrase.append(chunk)
        phrase=str(phrase).replace("[","").replace("]","").replace("the","")
        p = []
        for w in phrase.split():
            if len(w) <=2:
                w=None
            else: 
                w=w
            p.append(w)
        phrase =  ' '.join(list(filter(None, p))).rstrip()
        return phrase.split(", ")

    # Fungsi ekstrak department
    def dept(self, text):
        text = text.lower()
        text = text.replace("-"," ")
        text = text.replace("."," ")
        text = text.replace("dept.","department")
        text = text.replace("dept","department")
        text = text.replace("dep ","department")
        text = text.replace("dep.","department")
        text = text.replace("departement","department")
        text = text.replace("department","department ")
        text = text.replace("o f ","of")
        text = text.replace("november","nopember")
        text = text.replace("technologi","technology")
        text = text.replace("institut teknologi sepuluh nopember"," its ")
        text = text.replace("sepuluh nopember institute of technology"," its ")
        
        if "its" in text:
            a = []
            for p in text.split(";"):
                if "its" in p and "department" in p:
                    for d in p.split(","):
                        if "department" in d:
                            dpt = d.replace("department", "").replace("of", "").replace("of ", "")
                            if "engineering" in dpt:
                                dpt = dpt.split()
                                try:
                                    dpt = dpt[:dpt.index("engineering")+1]
                                except: pass
                                dpt = ' '.join(dpt)
                                
                            # if "and" not in dpt:
                            #     a = []
                            #     for w in dpt.split(" "):
                            #         if len(w)<4:
                            #             w = None
                            #         else: w=w
                            #         a.append(w)
                            #     a = list(filter(None, a))
                            #     dpt = ' '.join(dpt)
                            dpt=dpt.strip().rstrip()
                            a.append(True)
                                
                else:
                    a.append(False)
            if True not in a: dpt ="ITS_no-dept"
        else: dpt = "non-ITS"
        return dpt