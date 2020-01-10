import tkinter as tk
import os, sys, time


def pushed(self):
    print("clicked")
    self["text"] = "変更したぜ"
    return


def main():
    root = tk.Tk()              # メインウィンドウ作成
    root.title("Tkinter test")  #メインウィンドウのタイトルを変更
    root.geometry("640x480")    #メインウィンドウを640x480にする

    
    label = tk.Label(root, text="Hello,World")      #ラベルを追加
    """
    label = tk.Label(window, param1=value, param2=value...)
    ↾tk.labelの書式
    windowにはラベルを表示させたいウィンドウの変数を、
    param1=valueの部分には色々なパラメーターを指定します。
    「abc」と表示させたいなら
    label = tk.Label(window, text="abc")
    となります。他のパラメーターを指定することもできます。
    """

    label.grid()                                    #表示
    """
    label.grid()ってなんだろうと思ったと思いますが、
    gridメソッドはすべての部品に備わっているものです。
    gridメソッドを呼び出さないと部品は表示されません。
    ※Buttonはpackメソッドで表示するのが主流です
    """
    button = tk.Button(root, text="ボタン", 
                        command= lambda : pushed(button))
    """
    lambdaというのが出ますが、これはPythonで
    コールバックなどを指定するときに役立つ無名関数というものです。
    詳しくは「python lambda」「python 無名関数」で調べてみてください。

    それで、pushed(button)の部分ですが、button変数を
    pushed関数から操作できるように、pushed関数に渡しています。
    pushed関数ではそれをselfという変数として受け取っています。
    """

    button.grid()




    root.mainloop()             #rootを表示し無限ループ

    return

main()