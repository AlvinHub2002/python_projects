import threading
import time_counter
import tkinter


class CountdownTimer:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("460x220")
        self.root.config(bg="gainsboro")
        self.root.title("Time counter")
        self.full_seconds = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.timeInput = tkinter.Entry(self.root, font=30)
        self.timeInput.place(x=125,y=40)
        self.startButton = tkinter.Button(self.root, font=30, text="Start", command=self.start_thread,bg='whitesmoke', activebackground='lightgreen')
        self.startButton.place(x=130,y=75)
        self.stopButton = tkinter.Button(self.root, font=30, text="Reset", command=self.reset,bg='whitesmoke', activebackground='lightcoral')
        self.stopButton.place(x=240,y=75)
        self.pauseButton = tkinter.Button(self.root, font=30, text="Pause", command=self.time_pause,bg='whitesmoke', activebackground='darkgrey')
        self.pauseButton.place(x=125,y=125)
        self.resumeButton = tkinter.Button(self.root, font=30, text="Resume", command=self.time_resume,bg='whitesmoke', activebackground='darkgrey')
        self.resumeButton.place(x=230,y=125)
        self.timeLabel = tkinter.Label(self.root, font=('Arial',15), text="Time: 00:00:00 ")
        self.timeLabel.place(x=140,y=5)
        self.timeup = tkinter.Label(self.root, font=40, text="")
        self.timeup.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
        self.pause = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.stop_loop = False
        self.root.mainloop()

    def start_thread(self):
        t = threading.Thread(target=self.start)
        t.start()

    def start(self):

        self.stop_loop = False
        time_split = self.timeInput.get().split(":")
        if len(time_split) == 3:
            self.hours = int(time_split[0])
            self.minutes = int(time_split[1])
            self.seconds = int(time_split[2])
        elif len(time_split) == 2:
            self.minutes = int(time_split[0])
            self.seconds = int(time_split[1])
        elif len(time_split) == 1:
            self.seconds = int(time_split[0])
        else:
            print("invalid time format")
            return
        self.full_seconds = self.hours * 3600 + self.minutes * 60 + self.seconds
        while self.full_seconds > 0 and not self.stop_loop:
            self.full_seconds = self.full_seconds - 1
            self.minutes, self.seconds = divmod(self.full_seconds, 60)
            self.hours, self.minutes = divmod(self.minutes, 60)
            self.timeLabel.config(text=f"Time: {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}")
            self.root.update()
            time.sleep(1)

        self.root.update()
        #self.timeup.config(text="TIME IS UP!")

    def time_pause(self):
        self.pause = True
        self.stop_loop = True
        self.hours = self.hours
        self.minutes = self.minutes
        self.seconds = self.seconds
        self.timeLabel.config(text=f"Time: {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}")
        self.timeLabel.update()

    def time_resume(self):
        self.pause = False
        self.stop_loop = False
        while self.full_seconds > 0 and not self.stop_loop:
            self.full_seconds = self.full_seconds - 1
            self.minutes, self.seconds = divmod(self.full_seconds, 60)
            self.hours, self.minutes = divmod(self.minutes, 60)
            self.timeLabel.config(text=f"Time: {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}")
            self.root.update()
            time.sleep(1)

    def reset(self):
        self.stop_loop = True
        self.timeLabel.config(text="Time: 00:00:00 ")
        self.timeup.config(text="")
        self.root.update()


CountdownTimer()
