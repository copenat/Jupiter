__author__ = 'Nathan'
import tkinter
import requests
import sys
import configparser
import os
import os.path
import logging


class JupiterUIApp(tkinter.Tk):
    def __init__(self, config):
        try:
            self.server_host = config.get("DEFAULT", "jupiter_server_host")
        except:
            self.server_host = "127.0.0.1"
        try:
            self.server_port = config.get("DEFAULT", "jupiter_server_port")
        except:
            self.server_port = "8090"

        tkinter.Tk.__init__(self)
        try:
            self.title(config.get("DEFAULT", "jupiter_title"))
        except:
            self.title("Jupiter UI")
        self.geometry("900x400")

        dir = os.path.dirname(os.path.abspath(__file__))
        self.wm_iconbitmap(os.path.join(dir, "favicon.ico"))
        self.configure(background="#000000")

        self.get_all_portfolios()

        self.t = PortfolioTable(self)
        self.e = ChoosePortfolio(self, self.portfolios)
        self.p = Portfolio(self)

        self.e.pack(side="top", fill="x", expand=True)
        self.p.pack(fill="x", expand=True, anchor="center")
        self.t.pack(side="top", fill="x", expand=True)

    def go_pressed(self):
        logging.debug("Get portfolio {0}".format(self.e.option_chosen.get()))
        try:
            r = requests.get("{0}/portfolio/{1}/".format(self._get_url(), self.e.option_chosen.get()))
            if r.status_code == 200:
                logging.debug(r.text)
                prtf_data = r.json()
                row = 1
                self.p.set(prtf_data['name'], prtf_data['description'])
                try:
                    for p in prtf_data['stocks']:
                        self.t.set(row, 0, p['symbol'])
                        self.t.set(row, 1, p['latestactivity']['lasttradeprice'])
                        self.t.set(row, 2, p['latestactivity']['index'])
                        self.t.set(row, 3, p['latestactivity']['lasttradedatetime'])
                        self.t.set(row, 4, p['latestactivity']['stockid'])
                        self.t.set(row, 5, p['description'])
                        row += 1
                except:
                    pass
        except Exception as e:
            logging.info("Unable to contact Jupiter Server : {0}".format(e))
            sys.exit(1)

    def get_all_portfolios(self):
        self.portfolios = []
        try:
            r = requests.get("{0}/portfolio/".format(self._get_url()))
            if r.status_code == 200:
                prtf_data = r.json()
                for p in prtf_data:
                    self.portfolios.append(p['name'])
        except Exception as e:
            logging.info("Unable to connect to Jupiter Server at {0}".format(self._get_url()))
            sys.exit(1)

    def _get_url(self):
        return "http://{0}:{1}".format(self.server_host, self.server_port)


class Portfolio(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, background="black")
        self.prtf = tkinter.Label(self, text="My portfolio", bg="#000000", fg="#FFFFFF", font=("Helvetica", 16))
        self.prtf.pack(side='left')
        self.desc = tkinter.Label(self, text="Here", bg="#000000", fg="#FFFFFF", font=("Helvetica", 16))
        self.desc.pack(side='left')

    def set(self, prtf=None, desc=None):
        if prtf:
            self.prtf['text'] = prtf
        if desc:
            self.desc['text'] = desc

class ChoosePortfolio(tkinter.Frame):
    def __init__(self, parent, portfolios):
        self.portfolios = portfolios

        tkinter.Frame.__init__(self, parent, background="black")
        self.lbl = tkinter.Label(self, text="Enter Portfolio : ", bg="#000000", fg="#FFFFFF")
        self.lbl.pack(side="left")

        self.option_chosen = tkinter.StringVar()
        self.option_chosen.set(self.portfolios[0])

        self.option = tkinter.OptionMenu(self, self.option_chosen, *self.portfolios)
        self.option.pack(side="left")

        self.btn = tkinter.Button(self, text="Go", bg="#000000", fg="#FFFFFF", command=parent.go_pressed)
        self.btn.pack(side='left')


class PortfolioTable(tkinter.Frame):
    def __init__(self, parent, rows=15, columns=6):
        tkinter.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tkinter.Label(self, text="-", borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
        self._setup_column_headings()

    def _setup_column_headings(self):
        self.set(0,0, "Symbol")
        self.set(0,1, "Price")
        self.set(0,2, "Index")
        self.set(0,3, "Last Trade")
        self.set(0,4, "ID")
        self.set(0,5, "Description")

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == "__main__":
    try:
        logfiledir = os.path.join(os.environ["LOCALAPPDATA"], "Jupiter")
    except Exception as e:
        logfiledir = os.path.join(os.path.expanduser("~"), "logs")
    if not os.path.isdir(logfiledir):
        os.makedirs(logfiledir)

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.DEBUG,
                        filename=os.path.join(logfiledir, "JupiterUI.log"),
                        datefmt='%Y%m%d %H:%M:%S')

    properties_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              os.path.pardir, os.path.pardir, 'properties'))
    configfile = os.path.join(properties_dir, 'JupiterUI.properties')
    config = configparser.ConfigParser()
    config.read(configfile)

    logging.info("Starting JupiterUI...")

    app = JupiterUIApp(config)
    app.mainloop()

import json.tool