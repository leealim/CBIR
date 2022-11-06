#
# 
# 程序的入口文件，创建主窗口对象并调用其自定义UI生成方法，并进入主循环
#
#
import tkinter as tk
from MainWindow import MainWindow

mainWindow=tk.Tk()
MainWindow(mainWindow).createUI()
mainWindow.mainloop()