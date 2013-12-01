import tkinter as tk
import wisp_parser as wp

class App:
    def __init__(self, master):
        self.answer = ''
        start_text = "Write your program here!"
        #Text Box
        self.t = tk.Text(master,width=100, height=20)
        self.t.insert("1.0", start_text)
        self.t.pack()
        
        #Button
        def button_callback():
            input = self.t.get('1.0', 'end')
            answer = wp.main(input)
            print(answer)
            self.m.config(text="Evaluated to: \n%s" % answer)
            self.m.update_idletasks()
        self.b = tk.Button(master, text="evaluate", width=10, command=button_callback)
        self.b.pack()
        
        #message
        self.m = tk.Message(master, text="hello")
        self.m.pack()
        
    
master = tk.Tk()

app = App(master)



master.mainloop()
#master.destroy()
