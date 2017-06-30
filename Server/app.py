# coding=UTF-8
"""Server app with Tkinter GUI"""
import Tkinter as tk
from TCPServer import TCPServerManager
from threading import Timer


def start():
    """Start server"""
    root = tk.Tk()
    root.geometry('800x600+250+50')
    app = App(root)
    app.mainloop()


class App(tk.Frame):
    """Server app"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.master.title('Seweryn')
        self.master.protocol('WM_DELETE_WINDOW', self.on_close)
        self.server = TCPServerManager(self)
        self.init_gui()
        self.server.start()

    def init_gui(self):
        """Build GUI"""
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

        self.button_shutdown = tk.Button(text='Shutdown', command=self.b_shutdown, state=tk.DISABLED, width=20)
        self.button_shutdown.grid(column=0, row=4, padx=10, pady=10, sticky='nw')

        self.button_logic = tk.Button(text='Logic', command=self.b_switch_logic, state=tk.DISABLED, width=20)
        self.button_logic.grid(column=0, row=5, padx=10, pady=10, sticky='nw')

        self.button_up = tk.Button(text='▲', command=self.b_up, state=tk.DISABLED, width=5, height=2)
        self.button_up.grid(column=2, row=5, padx=5, pady=10, sticky='s')

        self.button_left = tk.Button(text='◀', command=self.b_left, state=tk.DISABLED, width=5, height=2)
        self.button_left.grid(column=1, row=6, padx=5, pady=10, sticky='ne')

        self.button_right = tk.Button(text='▶', command=self.b_right, state=tk.DISABLED, width=5, height=2)
        self.button_right.grid(column=3, row=6, padx=5, pady=10, sticky='nw')

        self.button_stop = tk.Button(text='⬛', command=self.b_stop, state=tk.DISABLED, width=5, height=2)
        self.button_stop.grid(column=2, row=6, padx=5, pady=10, sticky='n')

    def update_info(self):
        """update data displayed on screen"""
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                self.info_name.config(text=agent.agent_name)
                if agent.autonomous:
                    self.info_logic.config(text='ON')
                else:
                    self.info_logic.config(text='OFF')
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

    def on_close(self):
        """WM_DELETE_WINDOW handler, executed when [X] button is clicked"""
        self.server.stop()
        self.master.destroy()

    def on_select(self, _):
        """agents_list on_select event handler, executed when selection in list changes"""
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

    def b_shutdown(self):
        """send shutdown command to selected agent, executed on [Shutdown] button clicked"""
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                agent.shutdown()
                self.agents_list.selection_clear(0, tk.END)
                self.agents_list.event_generate('<<ListboxSelect>>')
                break

    def b_switch_logic(self):
        """send switch logic command to selected agent, executed on [Logic] button clicked"""
        for agent in self.server.agents:
            if agent.agent_name == self.agents_list.get(tk.ACTIVE):
                agent.switch_logic()
                break

    def b_up(self):
        """stub for remote control"""
        pass

    def b_left(self):
        """stub for remote control"""
        pass

    def b_right(self):
        """stub for remote control"""
        pass

    def b_stop(self):
        """stub for remote control"""
        pass
