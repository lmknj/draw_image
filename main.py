import tkinter
from tkinter import font
from tkinter import ttk
from tkinter import *
import numpy as np
import copy


class ROI():
    def __init__(self, value_list, class_name, keypoint, tags, combo_box):
        self.roi = value_list
        self.class_name = class_name
        self.keypoint = keypoint
        self.tags = tags
        self.combo_box = combo_box
        
        return

"""
class Keypoint():
    def __init__(self):


        return

class imageData():
    def __init__(self, roi, class_name = None, keypoint = None):
        self.roi = roi
        self.class_name = class_name
        self.keypoint = keypoint
        self.score = np.full(1, self.roi.shape(0))
        self.sizeX = roi[3] - roi[1]
        self.sizeY = roi[2] - roi[0]

        return


"""

class Size_window(tkinter.Frame):

    def __init__(self, main_window, master=None):
        self.master = master
        self.main_window = main_window


        super().__init__(master)
        self.pack()
        self.create_widgets()
        return

    def create_widgets(self):
        #サイズを入力してください
        self.message = tkinter.Label(self, text='キャンバスの大きさを入力してください')
        self.message.pack(side="top")

        #テキストボックスX
        L1 = tkinter.Label(self, text="X:")
        L1.pack(side=tkinter.LEFT)
        self.E1 = tkinter.Entry(self, bd=1)
        self.E1.pack(side=tkinter.LEFT)
       
        
        #テキストボックスY
        L2 = tkinter.Label(self, text="Y:")
        L2.pack(side=tkinter.LEFT)
        self.E2 = tkinter.Entry(self, bd=1)
        self.E2.pack(side=tkinter.LEFT)
        
        
        #完了ボタン(masterのウィンドウサイズ変更してキャンバスを生成))
        complete = tkinter.Button(self, text="完了",
                         command=self.size_complete)  
                        
        complete.pack(side=tkinter.BOTTOM)
        return

            
    def size_complete(self):
        x = 0
        y = 0
        try:
            x = int(self.E1.get())
            y = int(self.E2.get())
        except ValueError:
            self.E1.delete(0, tkinter.END)
            self.E2.delete(0, tkinter.END)
            self.message["text"] = '有効な値を入力してください'
            self.message["fg"]="red"

            return

        #print(self.E1.get())
        #print(self.E2.get())
        #ウィンドウのサイズを変換
        self.main_window.master.geometry("{}x{}".format(x, y))

        sub = 25
        self.main_window.canvas.config(width = x, height= y )
        #self.main_window.canvas.delete()
        self.main_window.canvas.create_rectangle(0, 0, x, y,
                                                 fill = 'white')
        self.main_window.sizeX = x
        self.main_window.sizeY = y                         
        
        #ウィンドウを破棄
        self.master.destroy()
        return






######################################kokokara"""""""""""""""""""""""""""""""""""""""""

class Application(tkinter.Frame):

    def __init__(self, master, sizeX, sizeY):
        self.class_names = ['正会員', '準会員', '未入会',"a"]
        self.roi_list = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.master = master
        self.mode = self.change_mode("ROI")
        self.selected_roi_number = None                #現在選択されている矩形
        self.selected_corner_number = None
        self.tag_number = 0
        self.tags = ["tag0_" + str(self.tag_number),    #左上
                    "tag1_" + str(self.tag_number),     #右上
                    "tag2_" + str(self.tag_number),     #右下？
                    "tag3_" + str(self.tag_number),     #左下？
                    "tag4_" + str(self.tag_number),     #矩形
                    "tag5_" + str(self.tag_number)      #クラス名
                    ]
        self.after_det_class_name = False
        



        super().__init__(master)
        self.pack()
        self.create_widgets()
        return

    def create_widgets(self):

        menubar = tkinter.Menu(self.master)
        
        
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.define_image_size)
        filemenu.add_command(label="Save", command=self.save_data) 
        filemenu.add_separator()    #メニューのセパレータを追加
        filemenu.add_command(label="Exit", command=self.master.destroy)   
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)


      
        self.det_roi = tkinter.Button(self, text="roi",
                         command=self.define_roi)    #roi決定モード
        self.det_class_name = tkinter.Button(self, text="class",
                         command=self.define_class_name)    #キーポイント決定モード
        self.det_keypoint = tkinter.Button(self, text="person",
                         command=self.change_keypoint)    #キーポイント決定モード
        self.select_roi = tkinter.Button(self, text="select",
                         command=self.change_roi)  

        
        self.det_roi.pack(side="left")
        self.det_class_name.pack(side="left")
        self.det_keypoint.pack(side="left")
        self.select_roi.pack(side="left")
        #キャンバスエリア
        sub = 25
        self.canvas = tkinter.Canvas(self.master,
                             width = self.sizeX, height = self.sizeY)
        self.canvas.create_rectangle(0, 0, self.sizeX, self.sizeY-sub,
                                                 fill = 'white')#塗りつぶし
        #キャンバスバインド
        self.canvas.place(x=0, y=sub)
        #self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.canvas.bind("<Button1-Motion>", self.motion)
        
        self.canvas.bind("<Button-3>", self.click_left)
        self.canvas.bind("<ButtonRelease-3>", self.release_left)
        self.canvas.bind("<Button3-Motion>", self.motion_left)

        self.menu_top = Menu(self.master,tearoff=False)
        #self.menu_2nd = Menu(self.menu_top,tearoff=0)
        #self.menu_3rd = Menu(self.menu_top,tearoff=0)
        #def remove_roi(self):

        self.menu_top.add_cascade (label='削除',command = self.remove_roi,under=5)
        self.menu_top.add_cascade (label='クラス名を指定',command = self.add_class_name,under=5)
        
        """
        self.menu_top.add_cascade (label='FILE(F)',menu=self.menu_2nd,under=5)
        self.menu_top.add_separator()
        #self.menu_top.add_command(label='EDIT(E)',underline=5,command=callback)

        self.menu_2nd.add_command(label='New Window(W)',under=4)
        self.menu_2nd.add_cascade(label='Open(O)',under=5,menu=self.menu_3rd)

        self.menu_3rd.add_command(label='Local File(L)',under=11)
        self.menu_3rd.add_command(label='Network(N)',under=8)
        """


        return


    def clicked_roi(self, event):
        self.canvas.create_oval(event.x-5, event.y-5,
                     event.x+5, event.y+5, fill="red",
                      width=0, tags = self.tags[0])
        #self.preX = event.x
        #self.preY = event.y
        #print(self.roi_tags)
        return

    def dragged_roi(self,event):
        #tagtag
        for tag in self.tags:
            self.canvas.delete(tag)

        self.make_roi_instance(self.preX, self.preY, event.x, event.y,
                    self.tags)
         
        
  
    
        #print(self.roi_tags)
        self.master.update()        
        
        return

    def released_roi(self, event):
        #self.canvas.create_oval(event.x-5, event.y-5,
        #             event.x+5, event.y+5, fill="green", width=0)

        #self.postX = event.x
        #self.postY = event.y
        
        if abs(self.preY - self. postY) == 0 and \
            abs(self.preX - self. postX) == 0:
            #print("実行")
            self.canvas.delete(self.tags[0])
            #self.det_selected_roi(self.preX, self.preY, pre_mode = "ROI")
            #self.det_selected_oval(self.preX, self.preY, pre_mode = "ROI")
            return
        

        if self.preY > self. postY:
            self. postY, self.preY = self.preY, self. postY

        if self.preX > self. postX:
            self. postX, self.preX = self.preX, self. postX

        
        self.make_roi_instance(self.preX, self.preY, self.postX, self.postY,
                    self.tags, True)
        #print("after make roi_instance",roi_instance.tags)
        
        
        #print(self.roi_tags)

        #print(self.circles_tag)
        #print(self.roi_tags)
        #print("tags of roi_instance after adding 1", roi_instance.tags)

        #print(self.roi_tags)

        

        return
       
    def make_roi_instance(self, preX, preY, postX, postY, tags, is_release = False):
        """
        if tags == None:
            tags = self.tags
        """
        #print("mroi:",tags)
        copied_tags = copy.copy(tags)
        box = None
        upper_left = self.canvas.create_oval(preX-5, preY-5,
                     preX+5, preY+5, fill="red",
                      width=0, tags = copied_tags[0])

        upper_right = self.canvas.create_oval(postX-5, preY-5,
                     postX+5, preY+5, fill="yellow", 
                     width=0, tags = copied_tags[1])
        
        lower_right = self.canvas.create_oval(postX-5, postY-5,
                     postX+5, postY+5, fill="blue", 
                     width=0, tags = copied_tags[2])
        
        lower_left = self.canvas.create_oval(preX-5, postY-5,
                     preX+5, postY+5, fill="green", 
                     width=0, tags = copied_tags[3])
        
        rect = self.canvas.create_rectangle(preX, preY,
                    postX, postY, tags = copied_tags[4])#塗りつぶし
        
        self.canvas.delete(copied_tags[5])
        #text = self.canvas.create_text(preX, preY, text = "token",
        #            font = ('FixedSys', 14), tags = copied_tags[5], anchor = NW)

        if is_release:
            #print("ccccccccccccccccccccccc")
            #rect = self.canvas.create_rectangle(preX, preY,
            #        postX, postY, fill = "green", tags = copied_tags[4])#塗りつぶし
            circle = np.array([upper_left, upper_right, lower_left, lower_right])

            roi_array = np.array([preY, preX, postY, postX])
            class_name = None

            roi_instance = ROI(value_list = roi_array, class_name = None, keypoint = None,
                        tags =  copied_tags, combo_box = None)
            self.roi_list.append(roi_instance)          #インスタンスの追加

            self.det_selected_roi(self.postX, self.postY)

            roi_instance.combo_box = self.add_class_name()

            self.tag_number += 1



        else:
            #print("aaaaaaaaaaaaaaaaaaaaaaa")
            pass
           

        #print(self.roi_list)
        for i in range(len(self.tags)):
            self.tags[i] = "tag{}_".format(i) + str(self.tag_number)
     

       
        
        
        #print("rect",rect)
        #print("aftermake,",copied_tags)

        
        

        return 


    def clicked_class_name(self, event):
        #self.canvas.create_oval(event.x-30, event.y-30,
        #             event.x+30, event.y+30, fill="green", width=0)
        count = 0
        #for roi in in self.roi_list:
        pre_roi = self.roi_list[self.selected_roi_number]
        #print(pre_roi.tags[0])
        clicked_roi_number = self.det_selected_roi(event.x, event.y, pre_mode = "CLASS_NAME")

        #print(clicked.tags[0])
        if self.selected_roi_number == clicked_roi_number:
            print("aaaaaaa")
            #クラス名の変更処理
            

        
        return
        
    def released_class_name(self, event):
        
        
        return
    def dragged_class_name(self,event):
        pass

    

    def clicked_keypoint(self, event):
        self.canvas.create_oval(event.x-30, event.y-30,
                     event.x+30, event.y+30, fill="blue", width=0)
        
        return
    def released_keypoint(self, event):
        self.canvas.create_oval(event.x-30, event.y-30,
                     event.x+30, event.y+30, fill="red", width=0)
        
        return   
    def dragged_keypoint(self,event):
        
        return
    
    def plain_menu(self, event):
        #何もないところを右クリック
        """
        キャンバスのリサイズ
        保存
        新規

        """
        return

    def roi_menu(self,event):
        """
        矩形or角をクリック
        削除
        コピー
        貼り付け
        キーポイント新規 
        クラス選択   

        キーポイントに接していたら
            キーポイント削除

        """
        self.show_popup(event)


        
        return
    def show_popup(self, event):
        self.menu_top.post(self.preX, self.preY)    #変な場所にメニューが出る
        return
    def remove_roi(self):
        #print("uwa-")
        #選択した矩形の削除
        if self.selected_roi_number == None:
            print("選択されていません")
            return
        tags = self.roi_list[self.selected_roi_number].tags
        for tag in tags:
             self.canvas.delete(tag)
            

        self.roi_list.pop(self.selected_roi_number)
        """
        for roi_obj in self.roi_list:
            print("list after removed", roi_obj.roi)
        """
        return

    def add_class_name(self):
        #選択した矩形にクラス名を追加
        if self.selected_roi_number == None:
            print("選択されていません")
            return
        
        roi_instance = self.roi_list[self.selected_roi_number]
        if roi_instance.combo_box == None:  #コンボボックスの中身がNoneのとき
            #print("add_classname:first combobox")
            val = tkinter.StringVar()
            box = ttk.Combobox(self.master, values = self.class_names, 
                                textvariable=val, state='normal')
            box.current(0) #初期値を'正会員(index=0)'に設定   
        else:
            print("add_classname:existing combobox")
            box =  roi_instance.combo_box   #基からあったら使いまわし
            
        
        box.place(x = roi_instance.roi[1], y = roi_instance.roi[0]) #座標指定で表示 

        self.after_det_class_name = True
                
        
        #self.roi_list[self.selected_roi_number].class_name = 
        """
        for roi_obj in self.roi_list:
            print("list after removed", roi_obj.roi)
        """
        #box.place(x = -100, y = -100)
        
        return box
    
    def get_class_name_from_box(self): #クラス名決定後の後処理    
        """
        クラス名の格納
        コンボボックスの排除
        """
        self.after_det_class_name = False
        roi_instance = self.roi_list[self.selected_roi_number]
        roi_instance.class_name = roi_instance.combo_box.get() 
        print("roi_instance.class_name",roi_instance.class_name)
            #コンボボックス内の値をclass_nameに入れる

        roi_instance.combo_box.place(x = -100, y = -100)

        #クラス名を表示
        #rect = self.canvas.create_rectangle(roi[1] + delta_x, roi[0] + delta_y,
        #        roi[3], roi[2],fill = "green", tags = tags[5])#塗りつぶし
        self.canvas.delete(roi_instance.tags[5])
        text = self.canvas.create_text(roi_instance.roi[1], roi_instance.roi[0],
                                        text = roi_instance.class_name,
                                        font = ('FixedSys', 14),
                                        tags = roi_instance.tags[5],
                                        anchor = NW)
        
        self.canvas.itemconfigure(roi_instance.tags[5], text = roi_instance.class_name)
        

        
        return



    def clicked_select_roi(self,event):
        #矩形を選択
        """
        #選択済みでない矩形をクリック
            #そのままドラッグ　→　矩形の位置変更
            #そのままリリーズ　→　矩形の選択

        #選択済みでない矩形の四隅をクリック　→　矩形を選択            
            #そのままドラッグ　→　矩形のサイズ変更
            #そのままリリーズ　→　矩形の選択
 
                 

        #選択済みの矩形の四隅をクリック
            #そのままドラッグ　→　矩形のサイズ変更
            #リリース　→　クラス選択

        #選択済みの矩形をクリック
            #ドラッグ　→　矩形の位置変更
            #リリース(ダブルクリック)　→　クラス選択
         
        #選択済みでない位置をクリック　→　選択の解除
            #そのままドラッグ　→　何もしない
            #そのままリリーズ　→　何もしない 
        

        #→クリックの時点ではただの選択処理のみ
        """
        
        self.selected_roi_number, self.selected_corner_number = \
                                self.det_selected_oval(event.x, event.y)
        #print("corner_number",self.selected_corner_number)
        
        return
    
  
    

    def dragged_select_roi(self,event):
        """
        ドラッグパターン
        矩形：位置変更
        四隅：サイズ変更
        何もなし：何もしない
        """

        try:
            tags =  self.roi_list[self.selected_roi_number].tags
            for tag in tags:
                self.canvas.delete(tag)
        except:
            #print("exception")
            return      #どの矩形にも触れていなければ何もしない
        
        if self.selected_corner_number == None: #コーナーをクリックしていない→移動
            #roi = self.selected_roi.roi
            #print("move activated")
            self.move_roi_instance(event.x, event.y)
            #print("end of else", tags)
        
        else:                                   #コーナーをクリック→リサイズ
            #print("resize act")
            self.resize_roi_instance(event.x, event.y)

        self.preX = event.x
        self.preY = event.y
    
   
        self.master.update()      
            


        
        return

    def resize_roi_instance(self, x, y):
        """
        if tags == None:
            tags = self.tags
        """
        roi = self.roi_list[self.selected_roi_number].roi
        tags = self.roi_list[self.selected_roi_number].tags
        #print("mroi:",tags)
        #copied_tags = copy.copy(tags)
        clicked_number = self.selected_corner_number
        #print("click_corner",clicked_number)
        delta_x = x - self.preX
        delta_y = y - self.preY
        array = []
        
        
        if clicked_number == 0:     #左上
            #print(0)

            rect = self.canvas.create_rectangle(roi[1] + delta_x, roi[0] + delta_y,
                roi[3], roi[2],fill = "green", tags = tags[4])#塗りつぶし
            

            upper_left = self.canvas.create_oval(roi[1]+delta_x-5, roi[0]+delta_y-5,
                        roi[1]+delta_x+5, roi[0]+delta_y+5, fill="red",
                        width=0, tags = tags[0])

            
            upper_right = self.canvas.create_oval(roi[3]-5, roi[0]+delta_y-5,
                        roi[3]+5, roi[0]+delta_y+5, fill="yellow", 
                        width=0, tags = tags[1])
            
            lower_right = self.canvas.create_oval(roi[3]-5, roi[2]-5,
                     roi[3]+5, roi[2]+5, fill="green", 
                     width=0, tags = tags[2])
    
            lower_left = self.canvas.create_oval(roi[1]+delta_x-5, roi[2]-5,
                        roi[1]+delta_x+5, roi[2]+5, fill="blue", 
                        width=0, tags = tags[3])
            
            text = self.canvas.create_text(roi[1]+delta_x, roi[0]+delta_y,
                        text = self.roi_list[self.selected_roi_number].class_name,
                        font = ('FixedSys', 14),
                        tags = tags[5],
                        anchor = NW)
            
            array = [roi[0] + delta_y, roi[1] + delta_x, roi[2], roi[3]]

        elif clicked_number == 1:   #右上
            rect = self.canvas.create_rectangle(roi[1], roi[0] + delta_y,
                roi[3] + delta_x, roi[2],fill = "green", tags = tags[4])#塗りつぶし
        

            upper_left = self.canvas.create_oval(roi[1]-5, roi[0]+delta_y-5,
                        roi[1]+5, roi[0]+delta_y+5, fill="red",
                        width=0, tags = tags[0])

            
            upper_right = self.canvas.create_oval(roi[3]+delta_x-5, roi[0]+delta_y-5,
                        roi[3]+delta_x+5, roi[0]+delta_y+5, fill="yellow", 
                        width=0, tags = tags[1])
            
   
            lower_left = self.canvas.create_oval(roi[1]-5, roi[2]-5, roi[1]+5, roi[2]+5, 
                        fill="blue", width=0, tags = tags[3])
        

            lower_right = self.canvas.create_oval(roi[3]+delta_x-5, roi[2]-5,
                        roi[3]+delta_x+5, roi[2]+5, fill="green", 
                        width=0, tags = tags[2])

            text = self.canvas.create_text(roi[1], roi[0]+delta_y,
                        text = self.roi_list[self.selected_roi_number].class_name,
                        font = ('FixedSys', 14),
                        tags = tags[5],
                        anchor = NW)
            
            array = [roi[0] + delta_y, roi[1], roi[2], roi[3] + delta_x]

        elif clicked_number == 2:   #右下
            rect = self.canvas.create_rectangle(roi[1], roi[0],
                roi[3] + delta_x, roi[2] + delta_y,fill = "green", tags = tags[4])#塗りつぶし
        
            upper_left = self.canvas.create_oval(roi[1]-5, roi[0]-5,
                     roi[1]+5, roi[0]+5, fill="red",
                      width=0, tags = tags[0])

            upper_right = self.canvas.create_oval(roi[3]+delta_x-5, roi[0]-5,
                        roi[3]+delta_x+5, roi[0]+5, fill="yellow", 
                        width=0, tags = tags[1])
            
            lower_left = self.canvas.create_oval(roi[1]-5, roi[2]+delta_y-5,
                        roi[1]+5, roi[2]+delta_y+5, fill="blue", 
                        width=0, tags = tags[3])
            
            lower_right = self.canvas.create_oval(roi[3]+delta_x-5, roi[2]+delta_y-5,
                        roi[3]+delta_x+5, roi[2]+delta_y+5, fill="green", 
                        width=0, tags = tags[2])

            text = self.canvas.create_text(roi[1], roi[0],
                        text = self.roi_list[self.selected_roi_number].class_name,
                        font = ('FixedSys', 14),
                        tags = tags[5],
                        anchor = NW)
            
            array = [roi[0], roi[1], roi[2] + delta_y, roi[3] + delta_x]

        elif clicked_number == 3:   #左下
            rect = self.canvas.create_rectangle(roi[1] + delta_x, roi[0],
                roi[3], roi[2] + delta_y,fill = "green", tags = tags[4])#塗りつぶし
        

            upper_left = self.canvas.create_oval(roi[1]+delta_x-5, roi[0]-5,
                        roi[1]+delta_x+5, roi[0]+5, fill="red",
                        width=0, tags = tags[0])
            
            upper_right = self.canvas.create_oval(roi[3]-5, roi[0]-5,
                     roi[3]+5, roi[0]+5, fill="yellow", 
                     width=0, tags = tags[1])

    
            lower_left = self.canvas.create_oval(roi[1]+delta_x-5, roi[2]+delta_y-5,
                        roi[1]+delta_x+5, roi[2]+delta_y+5, fill="blue", 
                        width=0, tags = tags[3])
            
            lower_right = self.canvas.create_oval(roi[3]-5, roi[2]+delta_y-5,
                        roi[3]+5, roi[2]+delta_y+5, fill="green", 
                        width=0, tags = tags[2])

            text = self.canvas.create_text(roi[1]+delta_x, roi[0],
                        text = self.roi_list[self.selected_roi_number].class_name,
                        font = ('FixedSys', 14),
                        tags = tags[5],
                        anchor = NW)

            array = [roi[0], roi[1] + delta_x, roi[2]+delta_y, roi[3]]
        else:
            print("sine")

        

        


            

        changed_roi = np.array(array)

        #ひっくり返ったときの処理
        #→releaseの時に直す

        self.roi_list[self.selected_roi_number].roi = changed_roi
        return

    
    def move_roi_instance(self, x, y):
        """
        if tags == None:
            tags = self.tags
        """
        roi = self.roi_list[self.selected_roi_number].roi
        tags = self.roi_list[self.selected_roi_number].tags
        #print("mroi:",tags)
        #copied_tags = copy.copy(tags)
        delta_x = x - self.preX
        delta_y = y - self.preY
        """
        print("preX",self.preX)
        print("preY",self.preY)
        print("x",x)
        print("y",y)
        print("roi",roi)
        print("xahyouX",roi[1] + delta_x)
        print("xahyouY",roi[0] + delta_y)
        print("")
        """

        rect = self.canvas.create_rectangle(roi[1] + delta_x, roi[0] + delta_y,
                roi[3] + delta_x, roi[2] + delta_y,fill = "green", tags = tags[4])#塗りつぶし
        

        upper_left = self.canvas.create_oval(roi[1]+delta_x-5, roi[0]+delta_y-5,
                     roi[1]+delta_x+5, roi[0]+delta_y+5, fill="red",
                      width=0, tags = tags[0])

        
        upper_right = self.canvas.create_oval(roi[3]+delta_x-5, roi[0]+delta_y-5,
                     roi[3]+delta_x+5, roi[0]+delta_y+5, fill="yellow", 
                     width=0, tags = tags[1])

   
        lower_left = self.canvas.create_oval(roi[1]+delta_x-5, roi[2]+delta_y-5,
                     roi[1]+delta_x+5, roi[2]+delta_y+5, fill="blue", 
                     width=0, tags = tags[3])
        
        lower_right = self.canvas.create_oval(roi[3]+delta_x-5, roi[2]+delta_y-5,
                     roi[3]+delta_x+5, roi[2]+delta_y+5, fill="green", 
                     width=0, tags = tags[2])

        text = self.canvas.create_text(roi[1]+delta_x, roi[0]+delta_y,
                        text = self.roi_list[self.selected_roi_number].class_name,
                        font = ('FixedSys', 14),
                        tags = tags[5],
                        anchor = NW)

        changed_roi = np.array([roi[0]+delta_y, roi[1]+delta_x ,roi[2]+delta_y ,roi[3]+delta_x])

        self.roi_list[self.selected_roi_number].roi = changed_roi
        return
    
    
    def released_select_roi(self,event):
        #矩形を選択

        if self.selected_roi_number == None:
            return
        
        if self.roi_list[self.selected_roi_number].roi[1] > \
                        self.roi_list[self.selected_roi_number].roi[3]: #xがひっくり返ってたら
            
            self.roi_list[self.selected_roi_number].roi[1], \
            self.roi_list[self.selected_roi_number].roi[3] = \
                    self.roi_list[self.selected_roi_number].roi[3], \
                    self.roi_list[self.selected_roi_number].roi[1]
                
        if self.roi_list[self.selected_roi_number].roi[0] > \
                        self.roi_list[self.selected_roi_number].roi[2]: #xがひっくり返ってたら
            
            self.roi_list[self.selected_roi_number].roi[0], \
           self. roi_list[self.selected_roi_number].roi[2] = \
                    self.roi_list[self.selected_roi_number].roi[2], \
                    self.roi_list[self.selected_roi_number].roi[0]
        
        roi = self.roi_list[self.selected_roi_number].roi    #ひっくり返った矩形の再描画

        tags = self.roi_list[self.selected_roi_number].tags
        for tag in tags:
                self.canvas.delete(tag)
        
        rect = self.canvas.create_rectangle(roi[1], roi[0],
                roi[3], roi[2],fill = "green", tags = tags[4])
        

        upper_left = self.canvas.create_oval(roi[1]-5, roi[0]-5,
                     roi[1]+5, roi[0]+5, fill="red",
                      width=0, tags = tags[0])

        
        upper_right = self.canvas.create_oval(roi[3]-5, roi[0]-5,
                     roi[3]+5, roi[0]+5, fill="yellow", 
                     width=0, tags = tags[1])

   
        lower_left = self.canvas.create_oval(roi[1]-5, roi[2]-5,
                     roi[1]+5, roi[2]+5, fill="blue", 
                     width=0, tags = tags[3])
        
        lower_right = self.canvas.create_oval(roi[3]-5, roi[2]-5,
                     roi[3]+5, roi[2]+5, fill="green", 
                     width=0, tags = tags[2])

        text = self.canvas.create_text(roi[1], roi[0],
                            text = self.roi_list[self.selected_roi_number].class_name,
                            font = ('FixedSys', 14),
                            tags = tags[5],
                            anchor = NW)

        


        return
    def det_selected_oval(self, x, y, pre_mode = "SELECT_ROI"):
        #クリックした矩形の四隅の決定
        """
        self.roi_list = []
        self.class_name_list = []
        self.keypoint_list = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        """
        #able_list = []
        self.change_mode("SELECT_ROI")
        #i = 0
        #self.selected_roi_number = None             #ここがいけない
        self.selected_corner_number = None
        clicked_obj_number = None
        clicked_corner_number = None
        

        for i in range(0, len(self.roi_list)):
            roi_object = self.roi_list[i]
            roi = roi_object.roi
            list0 = [roi[0], roi[1]]    #upper_left [y,x] 赤
            list1 = [roi[0], roi[3]]         #upper_right　黄色 
            
            list2 = [roi[2], roi[3]]         #lower_right　青
            list3 = [roi[2], roi[1]]         #lower_left    緑
            lists = [list0, list1, list2, list3]
            count = 0
            for l in lists:   #四隅のそれぞれを比較
                if self.corner_is_clicked( l[1], l[0], self.preX, self.preY):
                    print("clicked")
                    self.canvas.itemconfigure(roi_object.tags[count], fill = 'black')
                    
                    clicked_obj_number = i
                    clicked_corner_number = count  #矩形と角の番号を格納
                    #break
                else:
                    #print("not clicked")
                    if count == 0:
                        self.canvas.itemconfigure(roi_object.tags[count], fill = 'red')
                    elif count == 1:
                        self.canvas.itemconfigure(roi_object.tags[count], fill = 'yellow')
                    elif count == 2:
                        self.canvas.itemconfigure(roi_object.tags[count], fill = 'blue')
                    elif count == 3:
                        self.canvas.itemconfigure(roi_object.tags[count], fill = 'green')

                count += 1
        
        if clicked_obj_number == None:
            print("NONE", None)
            return self.det_selected_roi(x, y, pre_mode = pre_mode) , None #角の判定が失敗で矩形の判定


        else:      
            self.selected_roi_number = clicked_obj_number
            #self.selected_roi.rect["fill"] = "green"
            self.canvas.itemconfigure(self.roi_list[self.selected_roi_number].tags[4],
                                 fill = 'green')
            self.canvas.delete(self.roi_list[self.selected_roi_number].tags[5])
            self.canvas.create_text(self.roi_list[self.selected_roi_number].roi[1],
                            self.roi_list[self.selected_roi_number].roi[0],
                            text = self.roi_list[self.selected_roi_number].class_name,
                            font = ('FixedSys', 14),
                            tags = self.roi_list[self.selected_roi_number].tags[5],
                            anchor = NW)
            
            
            
            
            return clicked_obj_number, clicked_corner_number




    
    def corner_is_clicked(self, x, y, clickedX, clickedY, corner_size = 5):
        if clickedX < x-corner_size:
           return False
        if clickedY < y-corner_size:
            return False
        if  x + corner_size < clickedX:
            return False
        if y + corner_size < clickedY:
            return False
        return True
    
    
    def det_selected_roi(self, x, y, pre_mode = "SELECT_ROI"):
        #クリックした矩形の決定
        """
        self.roi_list = []
        self.class_name_list = []
        self.keypoint_list = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        """
        #able_list = []
        self.change_mode("SELECT_ROI")
        self.selected_roi_number = None
        clicked = []

    
        for i in range(0,len(self.roi_list)):
            roi_object = self.roi_list[i]
            roi = roi_object.roi
            self.canvas.delete(roi_object.tags[5])
            if x < roi[1]:
                #print("s")  
                self.canvas.itemconfigure(roi_object.tags[4], fill = 'white')
                self.canvas.create_text(roi[1], roi[0],
                                    text = roi_object.class_name,
                                    font = ('FixedSys', 14),
                                    tags = roi_object.tags[5],
                                    anchor = NW)
                
                continue
            if y < roi[0]:
                #print("d")
                self.canvas.itemconfigure(roi_object.tags[4], fill = 'white')
                
                self.canvas.create_text(roi[1], roi[0],
                                    text = roi_object.class_name,
                                    font = ('FixedSys', 14),
                                    tags = roi_object.tags[5],
                                    anchor = NW)
                
                continue
            if  roi[3] < x:
                #print("f")
                self.canvas.itemconfigure(roi_object.tags[4], fill = 'white')
                
                self.canvas.create_text(roi[1], roi[0],
                                    text = roi_object.class_name,
                                    font = ('FixedSys', 14),
                                    tags = roi_object.tags[5],
                                    anchor = NW)
                
                continue
            if roi[2] < y:
                #print("g")
                self.canvas.itemconfigure(roi_object.tags[4], fill = 'white')
                
                self.canvas.create_text(roi[1], roi[0],
                                    text = roi_object.class_name,
                                    font = ('FixedSys', 14),
                                    tags = roi_object.tags[5],
                                    anchor = NW)
                
                continue
            self.canvas.itemconfigure(roi_object.tags[4], fill = 'white')
            
            self.canvas.create_text(roi[1], roi[0],
                                    text = roi_object.class_name,
                                    font = ('FixedSys', 14),
                                    tags = roi_object.tags[5],
                                    anchor = NW)
            
            clicked.append(i) #インスタンスと要素番号
            #print("tags of roi_object",roi_object.tags)
            
      
  
        if pre_mode == "CLASS_NAME":
            self.change_mode("CLASS_NAME")
        
        if len(clicked) == 0:
                self.change_mode(pre_mode)
                print(None)
                return None
        
        min_area = self.sizeX * self.sizeY  #クリック範囲内の矩形の面積の最小値
        min_obj = None #↾に対応するROIインスタンス
        for j in clicked:
            area = self.det_area(self.roi_list[j].roi)
            #print(area)
            if area < min_area:
                min_area = area
                min_obj = j
        #print(min_obj)
        #print("tags of min_obj",min_obj.tags)
        self.selected_roi_number = min_obj


        self.canvas.itemconfigure(self.roi_list[self.selected_roi_number].tags[4], 
                                fill = 'green')
        
        self.canvas.create_text(self.roi_list[self.selected_roi_number].roi[1], 
                    self.roi_list[self.selected_roi_number].roi[0],
                    text = self.roi_list[self.selected_roi_number].class_name,
                    font = ('FixedSys', 14),
                    tags = self.roi_list[self.selected_roi_number].tags[5],
                    anchor = NW)

        
        return self.selected_roi_number


    
    def det_area(self, array):
        return(array[3] - array[1]) * (array[2] - array[0])
    
    
    def define_image_size(self):
        #画像サイズの決定or変更
        #filewin = tkinter.Toplevel(self.master)
        #button = tkinter.Button(filewin, text="Do nothing button")
        #button.pack()
        #縦横比を入力するウィンドウを生成(整数)

        size_def = tkinter.Tk()
        size_def.title("キャンバスの大きさ")
        size_def.geometry("350x50")
        size_window = Size_window(main_window = self, master = size_def)
        size_window.mainloop()
 
        return
    def change_mode(self, mode):
        self.mode = mode
        print("mode:{}".format(mode))
        return mode


    def define_roi(self, roi = None):
        #矩形サイズの決定or変更
        self.change_mode("ROI")

        return
    
    def define_class_name(self, class_name = None):
        #クラス名を宣言する
        self.change_mode("CLASS_NAME")
        return

    def change_keypoint(self, keypoint = None):
        #キーポイントを変更する
        self.change_mode("KEYPOINT")

        return
    def change_roi(self):
        self.change_mode("SELECT_ROI")
        return

    def save_data(self):    #セーブ

        return

    def click(self, event):
        # クリックされた場所に描画する
        #クラス名入力直後なら、クラス名を決定する
        if self.after_det_class_name:
            self.get_class_name_from_box()
            



        self.preX = event.x
        self.preY = event.y
        """
        #何もないところクリック→ROIモード
        #矩形内クリック→選択モード（移動など）
           #右クリックorボタンでキーポイント？ 
        #四隅クリック→選択モード(サイズ変更))
        """
        is_rect, is_oval =  self.det_selected_oval(event.x, event.y, pre_mode = "ROI")

        if is_rect == None:     #余白をクリック
            self.clicked_roi(event)
        else:                    #余白以外をクリック
            if abs(self.preY - self. postY) == 0 and \
                abs(self.preX - self. postX) == 0:      #ダブルクリック
                self.add_class_name()
             
            self.clicked_select_roi(event) 


        """
        if self.mode == "ROI":
            self.clicked_roi(event)
        elif self.mode == "CLASS_NAME":
            self.clicked_class_name(event)
        elif self.mode == "KEYPOINT":
            self.clicked_keypoint(event)
        elif self.mode == "SELECT_ROI":
            self.clicked_select_roi(event)
        else:
            print("INVALID MODE*{}".format(self.mode))
        """

        return
    
    def release(self, event):
        # クリックされた場所に描画する
        self.postX = event.x
        self.postY = event.y

        if self.mode == "ROI":
            self.released_roi(event)
        elif self.mode == "CLASS_NAME":
            self.released_class_name(event)
        elif self.mode == "KEYPOINT":
            self.released_keypoint(event)
        elif self.mode == "SELECT_ROI":
            self.released_select_roi(event)
        
        
        return

    
    def motion(self, event):
        # クリックされた場所に描画する
        if self.mode == "ROI":
            self.dragged_roi(event)
        elif self.mode == "CLASS_NAME":
            self.dragged_class_name(event)
        elif self.mode == "KEYPOINT":
            self.draggeded_keypoint(event)
        elif self.mode == "SELECT_ROI":
            self.dragged_select_roi(event)
        
        
        return
    
    
    def click_left(self, event):
        # クリックされた場所に描画する
        self.preX = event.x
        self.preY = event.y
        """
        #何もないところクリック→ROIモード
        #矩形内クリック→選択モード（移動など）
           #右クリックorボタンでキーポイント？ 
        #四隅クリック→選択モード(サイズ変更))
        """
        is_rect, is_oval =  self.det_selected_oval(event.x, event.y, pre_mode = "ROI")

        if is_rect == None:     #何もないところクリック
            self.plain_menu(event)
        else:
            #if is_oval == None:    #矩形かコーナーをクリック
            self.roi_menu(event)



        return
    
    def release_left(self, event):
        # クリックされた場所に描画する
        self.postX = event.x
        self.postY = event.y
        if self.mode == "ROI":
            self.released_roi(event)
        elif self.mode == "CLASS_NAME":
            self.released_class_name(event)
        elif self.mode == "KEYPOINT":
            self.released_keypoint(event)
        elif self.mode == "SELECT_ROI":
            self.released_select_roi(event)
        
        
        return

    
    def motion_left(self, event):
        # クリックされた場所に描画する
        if self.mode == "ROI":
            self.dragged_roi(event)
        elif self.mode == "CLASS_NAME":
            self.dragged_class_name(event)
        elif self.mode == "KEYPOINT":
            self.draggeded_keypoint(event)
        elif self.mode == "SELECT_ROI":
            self.dragged_select_roi(event)
        
        
        return

    

    
    


def main():
    root = tkinter.Tk()
    sizex = 600
    sizey = 400
    root.geometry("{}x{}".format(sizex, sizey))
    app = Application(master=root, sizeX = sizex, sizeY = sizey)
    app.mainloop()



    return

main()
    