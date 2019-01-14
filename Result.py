import tkinter as tk
from tkinter import *
import numpy
class MyFirstGUI:
    def __init__(self, master,result):
        self.master = master
        master.geometry("991x700+453+0")
        master.title("Result")
        master.configure(background="#d9d9d9")
        master.configure(highlightbackground="#d9d9d9")
        master.configure(highlightcolor="black")
        centername=["Solapur","Indore","Vijayawada","Hubli"]
        for i in range(1,(len(centername)+1)):
            center=Label(master,width=10)
            center.configure(text=centername[i-1])
            center.grid(row=0,column=i)
        objective=Label(master,width=10)
        objective.configure(text='''Total cost:''')
        objective.config(font=" Arial 20 bold")
        objective.grid(row=0,column=6)
        cost=Label(master,width=10)
        cost.configure(text=result[108])
        cost.config(justify="center")
        cost.config(font=" Arial 20 bold")
        cost.grid(row=0,column=8)
        idx=24
        chose=Label(master,width=20)
        chose.configure(text='''Chosen center''')
        chose.grid(row=1,column=0)
        for j in range(1,5):
            b=Entry(master,width=10)
            b.insert(INSERT,result[idx])
            b.config(justify="center")
            b.grid(row=1, column=j)
            idx+=1
        master.grid_rowconfigure(1,pad=20)
        customername=["Mumbai","Chennai","Bangalore","Hyderabad","Bhopal","Kanpur"]
        label1=Label(master,width=20)
        label1.configure(text='''Center serving customer:''')
        label1.grid(row=2,column=0)
        for i in range(1,len(customername)+1):
            customer=Label(master,width=10)
            customer.configure(text=customername[i-1])
            customer.grid(row=3,column=i)
        for i in range(4,len(centername)+4):
            center=Label(master,width=20)
            center.configure(text=centername[i-4])
            center.grid(row=i,column=0)
        idx=0
        for i in range(1,len(customername)+1):
            for j in range(4,len(centername)+4):
                served=Label(master,width=10)
                served.configure(text=result[idx])
                served.config(justify="center")
                served.grid(row=j, column=i)
                idx+=1
        label2=Label(master,width=20)
        label2.configure(text='''Plant to center''')
        label2.grid(row=9,column=0)
        master.grid_rowconfigure(9,pad=20)
        comodity=["CA","CB","CC","CD","CE"]
        planname=["Vadodara","Visakhapatnam","Nagpur","Kochi"]
        plant1=Label(master,width=20)
        plant1.configure(text=planname[0])
        plant1.grid(row=11,column=0,rowspan=5,sticky=tk.S+tk.N)
        for i in range(len(comodity)):
            como=Label(master,width=10)
            como.configure(text=comodity[i])
            como.grid(row=11+i,column=1)
        plant2=Label(master,width=20)
        plant2.configure(text=planname[1])
        plant2.grid(row=16,column=0,rowspan=5,sticky=tk.S+tk.N)
        for i in range(len(comodity)):
            como=Label(master,width=10)
            como.configure(text=comodity[i])
            como.grid(row=16+i,column=1)
        plant3=Label(master,width=20)
        plant3.configure(text=planname[2])
        plant3.grid(row=21,column=0,rowspan=5,sticky=tk.S+tk.N)
        for i in range(len(comodity)):
            como=Label(master,width=10)
            como.configure(text=comodity[i])
            como.grid(row=21+i,column=1)
        plant4=Label(master,width=20)
        plant4.configure(text=planname[3])
        plant4.grid(row=26,column=0,rowspan=5,sticky=tk.S+tk.N)
        for i in range(len(comodity)):
            como=Label(master,width=10)
            como.configure(text=comodity[i])
            como.grid(row=26+i,column=1)
        for i in range(len(centername)):
            cen=Label(master,width=15)
            cen.configure(text=centername[i])
            cen.grid(row=10,column=2+i)
        print(result[28])
        idx=28
        rownum=10
        for i in range(len(planname)):
            for j in range(len(comodity)):
                rownum=rownum+1
                for k in range(len(centername)):
                    print('Rownumber:',rownum)
                    amount=Label(master,width=10)
                    amount.configure(text=result[idx])
                    amount.grid(row=rownum,column=2+k)
                    idx+=1
        print(result[107])
        #plant2=Label(master)
        #plant2.configure(text=planname[1])
        #plant2.grid(row=10,column=5,columnspan=5,sticky='EWNS')
        #b=Entry(master,width=10)
        #b.insert(INSERT,"ABC")
        #b.grid(row=0,column=13)
        #self.tree= tk.Text(master)
        #self.tree.insert(INSERT,result)
        #self.tree.pack()

    

test=numpy.array(["Helloo","Hi","Halo"])


##   my_gui=MyFirstGUI(root,result)
