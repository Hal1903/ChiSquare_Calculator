from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image
import pandas
import lxml

lis=[]
elis=[]
txtLis=[]
txtLis2=[]
clis=[]
t=0
d=None
table = None
#ChiSquare=None
#ans=None

def getTable():
    global table
    url = 'https://people.richland.edu/james/lecture/m170/tbl-chi.html'
    table = pandas.read_html(url)

def degf():
    df = table[0]
    #df2 = df[['0.995']]
    DegreeOfFreedom = df['df'].values.tolist()
    # print('df: ',df2,'\ndfList:',DegreeOfFreedom)
    return DegreeOfFreedom


def pv():
    plis=[]
    Pvalue = list(table[0].columns.values)
    del (Pvalue[0])
    print(Pvalue)
    for i in Pvalue:
            plis.append(float(i))
    #print(Pvalue)
    print(plis)
    return plis

class MainScreen(Screen):
    ans=StringProperty()
    adding = ObjectProperty(None)
    adding2 = StringProperty()
    deleting = ObjectProperty(None)

    def btn(self):
        try:
            lis.append(float(self.adding.text))
            #print(self.adding.text)
        except:
            pass

    def strings(self):
        global txtLis
        txtLis=[]
        for x in lis:
            txtLis.append(str(x))
        return txtLis

    def changeTxt(self):
        self.adding2 = "Your data: "+str(self.strings())
        #print(self.adding2)
        try:
            self.adding.text = ""
        except:
            pass
        try:
            self.deleting.text = ""
        except:
            pass

    def deleteVal(self,x):
        try:
            del(lis[int(x.text)-1])
            self.adding2 = "Your data: "+str(self.strings())
            self.deleting.text = ""
        except:
            pass

    adding3 = ObjectProperty(None)
    adding4 = StringProperty()
    deleting2 = ObjectProperty(None)

    def btn2(self):
        try:
            elis.append(float(self.adding3.text))
            #print(elis)
        except:
            pass

    def strings2(self):
        global txtLis2
        txtLis2=[]
        for b in elis:
            txtLis2.append(str(b))
        return txtLis2

    def changeTxt2(self):
        self.adding4 = "Your data: "+str(self.strings2())
        #print(self.adding4)
        try:
            self.adding3.text = ""
        except:
            pass
        try:
            self.deleting2.text = ""
        except:
            pass

    def deleteVal2(self,x):
        try:
            del(elis[int(x.text)-1])
            self.adding4 = "Your data: "+str(self.strings2())
            self.deleting2.text = ""
        except:
            pass


    def calc(self):
        global t, clis
        for i in lis:
            clis.append(pow(i - elis[t], 2) / lis[t])
            #print(clis[t])
            t = t + 1
        ChiSquare=sum(clis)
        print(ChiSquare)
        clis=[]
        t=0
        return round(ChiSquare,3)

    def result(self):
        self.manager.screens[1].label1.text = str(self.calc())




# Second Screen
class dfpScreen(Screen):
    inputdf = ObjectProperty(None)
    inp = ObjectProperty(None)
    def dfbtn(self, x):
        dfm = degf()
        try:
            userdf=float(x)
            mingap = 1000
            closest = None
            for a in dfm:
                #print(a,' & ',x)
                if abs(a - userdf) < mingap:
                    mingap = abs(a - userdf)
                    closest = a
                    #print(abs(a - userdf),' & ',closest)
                else:
                    pass
            print(closest)
            mingap = 1000
            return closest
        except:
            print('error')

    def pvalbtn(self,x):
        p = pv()
        #print(p)
        try:
            userp=float(x)
            mgap = 100
            close = 100
            for b in p:
                #print(abs(b - userp),' & ',close)
                if abs(b - userp) < mgap:
                    mgap = abs(b - userp)
                    close = b
                else:
                    pass
            #print('close: ', close)
            mgap = 100
            return close
        except:
            print('error')

    def result(self,d):#,p):
        global table
        #print(d)
        #print('d:',d,'\np:',p)
        df = table[0]
        df = df.rename(columns={'0.90':'0.9','0.10':'0.1'})
        #print(df)
        #print(df)
        #print("user's chi-square: ", df[str(p)][d-1])
        try:
            print("user's value: ", MainScreen.calc(MainScreen))
            print("user's chi-square: ", df[str(0.1)][d - 1])
            print('rejection chi-square: ', df[str(0.05)][d - 1])
            if MainScreen.calc(MainScreen) >= df[str(0.05)][d-1]:
                self.manager.screens[1].chibel.text = str("Rejected")
            else:
                self.manager.screens[1].chibel.text = str("Failed to reject")
        except:
            self.manager.screens[1].chibel.text = str("Error")

class CalcScreen(Screen):
    #c = ObjectProperty(None)
    #ans = StringProperty()
    def btn3(self):
        pass
    #def setResult(self,x):
        #ans = NumericProperty(ChiSquare)
        #self.ans=str(x)
        #print(x)

#class MyImage(AsyncImage):
#    pass

class TableScreen(Screen):
    pass
    #img = AsyncImage(source = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.statology.org%2Fhow-to-read-chi-square-distribution-table%2F&psig=AOvVaw2AbVBQHgoFoNnUwVES9G9n&ust=1608891596560000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLC4s7Sy5u0CFQAAAAAdAAAAABAa')

from kivy.config import Config

class WindowManager(ScreenManager):
    pass

class MyMainApp(App):
    Config.set('graphics','width',350)
    Config.set('graphics', 'height', 600)
    def build(self):
        root = Builder.load_file('my.kv')
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(CalcScreen())
        sm.add_widget(dfpScreen())
        sm.add_widget(TableScreen())
        getTable()
        #self.degf()
        #self.pv()
        sm.current = 'mainwin'
        return root

if __name__ == "__main__":
    MyMainApp().run()