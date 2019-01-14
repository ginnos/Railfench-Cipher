from tkinter import *
import itertools

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()      

    def create_widgets(self):
        self.inputtext = Text(self.master, height=1)
        self.inputtext.insert(END, 'INPUT:')
        self.inputtext['state'] = 'disabled' 
        self.inputtext.pack(side='top',expand=1,fill='x')
        
        self.entrycode = Entry(self.master)
        self.entrycode.pack(side='top',expand=1,fill='x')

        self.numtext = Text(self.master, height=1)
        self.numtext.insert(END, 'FENCE NUMBER:')
        self.numtext['state'] = 'disabled' 
        self.numtext.pack(side='top',expand=1,fill='x')
        
        self.entrynum = Entry(self.master)
        self.entrynum.pack(side='top',expand=1,fill='x')

        self.outputtext = Text(self.master, height=1)
        self.outputtext.insert(END, 'RESULT:')
        self.outputtext['state'] = 'disabled' 
        self.outputtext.pack(side='top',expand=1,fill='x')

        self.resulttext = Text(self.master, height=5)
        self.resulttext.pack(side='bottom',expand=1,fill='x')

        self.rf_encode = Button(self, fg='green')
        self.rf_encode['text'] = 'Encode'
        self.rf_encode['command'] = self.encode
        self.rf_encode.pack(side='left',expand=1,fill='x')

        self.rf_decode = Button(self, fg='green')
        self.rf_decode['text'] = 'Decode'
        self.rf_decode['command'] = self.decode
        self.rf_decode.pack(side='right',expand=1,fill='x')

        #self.quit = Button(self, text='QUIT', fg='red',
         #                     command=self.master.destroy)
        #self.quit.pack(side='top')

    def encode(self):
        self.resulttext.delete(0.0,END)
        temp = []
        ans = ''
        try:
            word = self.entrycode.get()
            nrow = int(self.entrynum.get())
        except Exception:
            self.resulttext.insert(END,'INCORRECT INPUT!')
        else:
            #字符串以nrow个为一组分割，分为m（=字符串长度除以nrow，取整）组
            for n in range(int(len(word)/nrow)):
                #nrow个为一组
                temp.append(word[n*nrow:n*nrow+nrow])
            #补齐余数部分
            if len(word)%nrow > 0:
                temp.append(word[-(len(word)%nrow):])
            #取每组相同位置的字符组成新的字符串（转置）
            for i in itertools.zip_longest(*temp, fillvalue=''):
                ans += ''.join(w for w in i)
            print(ans)
            self.resulttext.insert(END, ans)
        return ans

    def decode(self):
        temp = []
        ans = ''
        self.resulttext.delete(0.0,END)
        try:
            code = self.entrycode.get()
            nrow = int(self.entrynum.get())
        except Exception:
            self.resulttext.insert(END,'INCORRECT INPUT!')
        #以rnow个为一组加密后的最小列数（刚好整除时）
        else:
            ncol = int(len(code) / nrow)
            lens = len(code)
            #以rnow个为一组加密后的余数，余数优先放在低位行
            rest = lens % nrow
            for n in range(nrow):
                #如果还有余数
                if rest > 0:
                    #将余数放在此行尾
                    temp.append(code[:ncol+1])
                    rest -= 1
                    #去掉已经加入的部分
                    code = code[ncol+1:]
                else:
                    temp.append(code[:ncol])
                    #去掉已经加入的部分
                    code = code[ncol:]
            #print(temp)
            #取每组相同位置的字符组成新的字符串（转置）
            for i in itertools.zip_longest(*temp, fillvalue=''):
                ans += ''.join(w for w in i)
            print(ans)
            self.resulttext.insert(END, ans)
        return ans

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.master.title('Railfench Cipher Encoder & Decoder')
    app.master.maxsize(800, 400)
    app.mainloop()
