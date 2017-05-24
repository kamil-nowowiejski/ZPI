# coding=UTF-8
import Tkinter as tk
from TCPServer import TCPServerManager
from threading import Timer
from tkMessageBox import showinfo


def start():
    root = tk.Tk()
    root.geometry('800x600+250+50')
    app = App(root)
    app.mainloop()


class App(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.master.title('Server')
        self.master.protocol('WM_DELETE_WINDOW', self.on_close)
        self.server = TCPServerManager(self)
        self.init_gui()
        self.server.start()

    def init_gui(self):
        self.video_feed = tk.Canvas(width=480, height=320)
        self.video_feed.config(background='white')
        self.video_feed.grid(column=0, columnspan=4, row=0, rowspan=4, padx=10, pady=10, sticky='nw')

        self.agents_list = tk.Listbox(selectmode=tk.SINGLE)
        self.agents_list.grid(column=4, row=0, rowspan=3, padx=10, pady=10, sticky='nw')
        self.agents_list.bind('<<ListboxSelect>>', self.on_select)

        self.label_name = tk.Label(text='Name')
        self.label_name.grid(column=5, row=0, padx=10, pady=10, sticky='nw')

        self.info_name = tk.Label(text='-')
        self.info_name.grid(column=6, row=0, padx=10, pady=10, sticky='nw')

        self.label_logic = tk.Label(text='Logic')
        self.label_logic.grid(column=5, row=1, padx=10, pady=10, sticky='nw')

        self.info_logic = tk.Label(text='-')
        self.info_logic.grid(column=6, row=1, padx=10, pady=10, sticky='nw')

        self.label_feed = tk.Label(text='Feed')
        self.label_feed.grid(column=5, row=2, padx=10, pady=10, sticky='nw')

        self.info_feed = tk.Label(text='-')
        self.info_feed.grid(column=6, row=2, padx=10, pady=10, sticky='nw')

        self.button_shutdown = tk.Button(text='Shutdown', command=self.b_shutdown, state=tk.DISABLED, width=20)
        self.button_shutdown.grid(column=0, row=4, padx=10, pady=10, sticky='nw')

        self.button_logic = tk.Button(text='Logic', command=self.b_switch_logic, state=tk.DISABLED, width=20)
        self.button_logic.grid(column=0, row=5, padx=10, pady=10, sticky='nw')

        self.button_feed = tk.Button(text='Video', command=self.b_switch_feed, state=tk.DISABLED, width=20)
        self.button_feed.grid(column=0, row=6, padx=10, pady=10, sticky='nw')

        self.button_detect = tk.Button(text='Detect', command=self.b_detect, state=tk.DISABLED, width=20)
        self.button_detect.grid(column=0, row=7, padx=10, pady=10, sticky='nw')

        self.button_up = tk.Button(text='▲', command=self.b_up, state=tk.DISABLED, width=5, height=2)
        self.button_up.grid(column=2, row=5, padx=5, pady=10, sticky='s')

        self.button_left = tk.Button(text='◀', command=self.b_left, state=tk.DISABLED, width=5, height=2)
        self.button_left.grid(column=1, row=6, padx=5, pady=10, sticky='ne')

        self.button_right = tk.Button(text='▶', command=self.b_right, state=tk.DISABLED, width=5, height=2)
        self.button_right.grid(column=3, row=6, padx=5, pady=10, sticky='nw')

        self.button_stop = tk.Button(text='⬛', command=self.b_stop, state=tk.DISABLED, width=5, height=2)
        self.button_stop.grid(column=2, row=6, padx=5, pady=10, sticky='n')

    def update_info(self):
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                self.info_name.config(text=agent.agent_name)
                if agent.autonomous:
                    self.info_logic.config(text='ON')
                else:
                    self.info_logic.config(text='OFF')
                if agent.feed:
                    self.info_feed.config(text='ON')
                else:
                    self.info_feed.config(text='OFF')
                if not agent.autonomous and agent.feed:
                    self.button_detect.config(state=tk.NORMAL)
                    self.button_up.config(state=tk.NORMAL)
                    self.button_left.config(state=tk.NORMAL)
                    self.button_right.config(state=tk.NORMAL)
                    self.button_stop.config(state=tk.NORMAL)
                else:
                    self.button_detect.config(state=tk.DISABLED)
                    self.button_up.config(state=tk.DISABLED)
                    self.button_left.config(state=tk.DISABLED)
                    self.button_right.config(state=tk.DISABLED)
                    self.button_stop.config(state=tk.DISABLED)

    def show_detected(self, objects):
        message = 'Detected objects:'
        for obj in objects:
            message += '\n%s, %s, %s, %s' % (obj.type, obj.height, obj.width, obj.color)
            for sym in obj.symbols:
                message += '\n\t%s, %s, %s, %s' % (sym.type, sym.height, sym.width, sym.color)
        # showinfo('Detected objects', 'msg')
        print message

    def on_close(self):
        self.server.stop()
        self.master.destroy()

    def on_select(self, _):
        print 'on select'
        if self.agents_list.curselection() is not ():
            self.button_shutdown.config(state=tk.NORMAL)
            self.button_logic.config(state=tk.NORMAL)
            self.button_feed.config(state=tk.NORMAL)
            Timer(0.1, self.update_info).start()
        else:
            self.button_shutdown.config(state=tk.DISABLED)
            self.button_logic.config(state=tk.DISABLED)
            self.button_feed.config(state=tk.DISABLED)
            self.info_name.config(text='-')
            self.info_logic.config(text='-')
            self.info_feed.config(text='-')

    def b_shutdown(self):
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                agent.shutdown()
                self.agents_list.selection_clear(0, tk.END)
                self.agents_list.event_generate('<<ListboxSelect>>')
                break

    def b_switch_logic(self):
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                agent.switch_logic()
                break

    def b_switch_feed(self):
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                agent.switch_feed()
                break

    def b_detect(self):
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                agent.detect()
                break

    def b_up(self):
        pass

    def b_left(self):
        pass

    def b_right(self):
        pass

    def b_stop(self):
        pass
