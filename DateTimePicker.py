#!/usr/bin/python

import calendar
from Tkinter import *
import time
import datetime

DEFAULTFONT = "Helvetica"
FONTSIZE = 12

class TimeSelectWindow:
    def __init__(self, parent, result_string):
        self.parent = parent
        self.display_var = result_string
        top = self.top = Toplevel()
        self.canvas = Canvas(top, width=90, height=50, relief=RIDGE, background="white", borderwidth=1)

        self.hour_var = StringVar()
        self.hour_var.set(str(self.parent.hour))
        self.lHour = Label(top, textvariable=self.hour_var, font=(DEFAULTFONT, FONTSIZE), background="white")
        self.lHour.place(x=10, y=12)

        Label(top, text=":", font=(DEFAULTFONT, FONTSIZE), background="white").place(x=30, y=12)

        self.min_var = StringVar()
        self.min_var.set(str(self.parent.minute))
        self.lMin = Label(top, textvariable=self.min_var, font=(DEFAULTFONT, FONTSIZE), background="white")
        self.lMin.place(x=40, y=12)

        Label(top, text=":", font=(DEFAULTFONT, FONTSIZE), background="white").place(x=60, y=12)

        self.sec_var = StringVar()
        self.sec_var.set(str(self.parent.second))
        self.lSec = Label(top, textvariable=self.sec_var, font=(DEFAULTFONT, FONTSIZE), background="white")
        self.lSec.place(x=70, y=12)

        base_tag = "Arrow"

        button_tag = "lasthour"
        final_tag = tuple((base_tag, button_tag))
        self.down_arrow(self.canvas, 20, 40, final_tag)
        button_tag = "nexthour"
        final_tag = tuple((base_tag, button_tag))
        self.up_arrow(self.canvas, 20, 10, final_tag)

        button_tag = "lastmin"
        final_tag = tuple((base_tag, button_tag))
        self.down_arrow(self.canvas, 50, 40, final_tag)
        button_tag = "nextmin"
        final_tag = tuple((base_tag, button_tag))
        self.up_arrow(self.canvas, 50, 10, final_tag)

        button_tag = "lastsec"
        final_tag = tuple((base_tag, button_tag))
        self.down_arrow(self.canvas, 80, 40, final_tag)
        button_tag = "nextsec"
        final_tag = tuple((base_tag, button_tag))
        self.up_arrow(self.canvas, 80, 10, final_tag)

        self.canvas.pack({"side": "left", "fill": "both"})
        self.canvas.tag_bind("Arrow", "<ButtonRelease-1>", self.clicked)

        Button(top,text="Ok",bg="white",command=self.click_ok).pack({"side": "right", "fill": "both"})

    def up_arrow(self, canv, x, y, tagname):
        canv.create_polygon(x, y, [[x - 10, y], [x + 10, y ], [x, y - 5], [x - 10, y]],
                            tags=tagname, outline="black", fill="white", width=1)

    def down_arrow(self, canv, x, y, tagname):
        canv.create_polygon(x, y, [[x - 10, y], [x + 10, y ], [x, y + 5], [x - 10, y]],
                            tags=tagname, outline="black", fill="white", width=1)

    def clicked(self, event):
        owntags = self.canvas.gettags(CURRENT)
        if "nexthour" in owntags:
            inthour = int(self.hour_var.get())
            inthour = (inthour + 1) % 24
            strhour = str(inthour)
            self.hour_var.set(strhour)
        if "lasthour" in owntags:
            inthour = int(self.hour_var.get())
            inthour = (inthour - 1) % 24
            strhour = str(inthour)
            self.hour_var.set(strhour)
        if "nextmin" in owntags:
            intmin = int(self.min_var.get())
            intmin = (intmin + 1) % 60
            strmin = str(intmin)
            self.min_var.set(strmin)
        if "lastmin" in owntags:
            intmin = int(self.min_var.get())
            intmin = (intmin - 1) % 60
            strmin = str(intmin)
            self.min_var.set(strmin)
        if "nextsec" in owntags:
            intsec = int(self.sec_var.get())
            intsec = (intsec + 1) % 60
            strsec = str(intsec)
            self.sec_var.set(strsec)
        if "lastsec" in owntags:
            intsec = int(self.sec_var.get())
            intsec = (intsec - 1) % 60
            strsec = str(intsec)
            self.sec_var.set(strsec)

    def click_ok(self, event = None):
        hour = int(self.hour_var.get())
        min = int(self.min_var.get())
        sec = int(self.sec_var.get())
        strtime = "%02d:%02d:%02d" % (hour, min, sec)
        self.display_var.set(strtime)
        self.top.withdraw()
        self.parent.hour = hour
        self.parent.minute = min
        self.parent.second = sec


class TimePicker(Frame):
    def __init__(self, master, hr_arg=None, min_arg=None, sec_arg=None):
        self.parent = master
        Frame.__init__(self, master)
        self.time_var = StringVar()
        self.hour = hr_arg
        self.minute = min_arg
        self.second = sec_arg
        if self.second is None:
            self.hour = time.localtime()[3]
            self.minute = time.localtime()[4]
            self.second = time.localtime()[5]
        self.time_var.set("%02d:%02d:%02d" % (self.hour, self.minute, self.second))
        label = Label(self, textvariable=self.time_var, bg="white")
        label.bind("<Button-1>", self.select_time)
        label.pack()

    def select_time(self, event):
        TimeSelectWindow(self, self.time_var)

    def get_time(self):
        return datetime.time(self.hour, self.minute, self.second)

class DateSelectWindow:
    days_names = "Su  Mo  Tu  We  Th  Fr  Sa"
    months_names = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun',
                '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    def __init__(self, parent, result_string):
        self.parent = parent
        self.display_var = result_string
        top = self.top = Toplevel()
        try:
            self.month = int(self.parent.month)
        except TypeError or ValueError:
            self.month = 1
        self.canvas = Canvas(top, width=200, height=190, relief=RIDGE, background="white", borderwidth=1)

        self.year_var = StringVar()
        self.year_var.set(str(self.parent.year))
        self.lYear = Label(top, textvariable=self.year_var, font=(DEFAULTFONT, FONTSIZE), background="white")
        self.lYear.place(x=85, y=0)

        self.month_var = StringVar()
        strmonth = DateSelectWindow.months_names[str(self.month)]
        self.month_var.set(strmonth)

        self.lYear = Label(top, textvariable=self.month_var,font=(DEFAULTFONT, FONTSIZE), background="white")
        self.lYear.place(x=85, y=22)

        base_tag = "Arrow"
        self.tagBaseNumber = "DayButton"

        button_tag = "lastyear"
        final_tag = tuple((base_tag, button_tag))
        self.left_arrow(self.canvas, 40, 13, final_tag)
        button_tag = "nextyear"
        final_tag = tuple((base_tag, button_tag))
        self.right_arrow(self.canvas, 150, 13, final_tag)

        button_tag = "lastmonth"
        final_tag = tuple((base_tag, button_tag))
        self.left_arrow(self.canvas, 40, 35, final_tag)
        button_tag = "nextmonth"
        final_tag = tuple((base_tag, button_tag))
        self.right_arrow(self.canvas, 150, 35, final_tag)

        self.canvas.create_text(100, 60, text=DateSelectWindow.days_names, font=(DEFAULTFONT, FONTSIZE))
        self.canvas.pack(expand=1, fill=BOTH)
        self.canvas.tag_bind("Arrow", "<ButtonRelease-1>", self.clicked)
        self.write_days()

    def right_arrow(self, canv, x, y, tagname):
        canv.create_polygon(x, y, [[x + 0, y - 5], [x + 5, y - 5], [x + 5, y - 10],
                                   [x + 20, y + 0], [x + 5, y + 10], [x + 5, y + 5], [x + 0, y + 5]],
                            tags=tagname, outline="black", fill="white", width=1)

    def left_arrow(self, canv, x, y, tagname):
        canv.create_polygon(x, y, [[x + 15, y - 10], [x + 15, y - 5], [x + 20, y - 5],
                                   [x + 20, y + 5], [x + 15, y + 5], [x + 15, y + 10]],
                            tags=tagname, outline="black", fill="white", width=1)

    def clicked(self, event):
        owntags = self.canvas.gettags(CURRENT)
        if "nextyear" in owntags:
            intyear = int(self.year_var.get())
            intyear += 1
            stryear = str(intyear)
            self.year_var.set(stryear)
        if "lastyear" in owntags:
            intyear = int(self.year_var.get())
            intyear -= 1
            stryear = str(intyear)
            self.year_var.set(stryear)
        if "nextmonth" in owntags:
            if self.month < 12:
                self.month += 1
                strnummonth = str(self.month)
                strmonth = DateSelectWindow.months_names[strnummonth]
                self.month_var.set(strmonth)
            else:
                self.month = 1
                strnummonth = str(self.month)
                strmonth = DateSelectWindow.months_names[strnummonth]
                self.month_var.set(strmonth)
                intyear = int(self.year_var.get())
                intyear += 1
                stryear = str(intyear)
                self.year_var.set(stryear)
        if "lastmonth" in owntags:
            if self.month > 1:
                self.month -= 1
                strnummonth = str(self.month)
                strmonth = DateSelectWindow.months_names[strnummonth]
                self.month_var.set(strmonth)
            else:
                self.month = 12
                strnummonth = str(self.month)
                strmonth = DateSelectWindow.months_names[strnummonth]
                self.month_var.set(strmonth)
                intyear = int(self.year_var.get())
                intyear -= 1
                stryear = str(intyear)
                self.year_var.set(stryear)
        self.write_days()

    def write_days(self):
        init_x_pos = 20
        arr_y_pos = [80, 100, 120, 140, 160, 180]
        intposarr = 0
        self.canvas.delete("DayButton")
        self.canvas.update()
        intyear = int(self.year_var.get())
        monthcal = calendar.monthcalendar(intyear, self.month)
        for row in monthcal:
            xpos = init_x_pos
            ypos = arr_y_pos[intposarr]
            for item in row:
                stritem = str(item)
                if stritem == "0":
                    xpos += 27
                else:
                    tag_number = tuple((self.tagBaseNumber, stritem))
                    self.canvas.create_text(xpos, ypos, text=stritem,
                                            font=(DEFAULTFONT, FONTSIZE), tags=tag_number)
                    xpos += 27
            intposarr += 1
            self.canvas.tag_bind("DayButton", "<ButtonRelease-1>", self.click_on_day)

    def click_on_day(self, event):
        owntags = self.canvas.gettags(CURRENT)
        for x in owntags:
            if (x == "current") or (x == "DayButton"):
                pass
            else:
                year = int(self.year_var.get())
                day = int(x)
                strdate = "%4d-%02d-%02d" % (year, self.month, day)
                self.display_var.set(strdate)
                self.top.withdraw()
                self.parent.year = year
                self.parent.month = self.month
                self.parent.day = day


class DatePicker(Frame):
    def __init__(self, master, year_arg=None, month_arg=None, day_arg=None):
        Frame.__init__(self, master)
        self.date_var = StringVar()
        self.year = year_arg
        self.month = month_arg
        self.day = day_arg
        if self.day is None:
            self.year = time.localtime()[0]
            self.month = time.localtime()[1]
            self.day = time.localtime()[2]
        self.date_var.set("%4d-%02d-%02d" % (self.year, self.month, self.day))
        label = Label(self, textvariable=self.date_var, bg="white")
        label.bind("<Button-1>", self.select_date)
        label.pack()

    def select_date(self, event):
        DateSelectWindow(self, self.date_var)

    def get_date(self):
        return datetime.date(self.year, self.month, self.day)


def print_date(datepicker, timepicker):
    print datepicker.get_date()
    print timepicker.get_time()


if __name__ == '__main__':
    date = "notread"
    root = Tk()
    root.title("DatePicker")
    dp = DatePicker(root)
    dp.pack({"side": "left"})
    tp = TimePicker(root)
    tp.pack({"side": "left"})
    b = Button(root, text="Print Date", command=lambda d=dp, t=tp: print_date(d,t))
    b.pack({"side": "left"})
    root.mainloop()

