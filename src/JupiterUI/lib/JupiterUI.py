__author__ = 'Nathan'
import tkinter
import requests
import sys
import configparser
import os
import os.path
import logging


class PortfolioData:
    def __init__(self, url):
        self.url = url

    def get(self, portfolio):
        try:
            r = requests.get("{0}/portfolio/{1}/".format(self.url, portfolio))
            if r.status_code == 200:
                logging.info(r.text)
                return r.json
            else:
                return {}
        except Exception as e:
            logging.info("Unable to connect to Jupiter Server at {0} to get portfolio {1}".format(self.url, portfolio))
            return {}


class PortfolioList:
    def __init__(self, url):
        self.portfolios = []
        self.url = url

    def get(self):
        try:
            r = requests.get("{0}/portfolio/".format(self.url))
            if r.status_code == 200:
                prtf_data = r.json()
                for p in prtf_data:
                    self.portfolios.append(p['name'])
        except Exception as e:
            logging.info("Unable to connect to Jupiter Server at {0}".format(self.url))
            self.portfolios.append("empty")
        return self.portfolios

class JupiterUIApp(tkinter.Tk):
    def __init__(self, config, portfoliolist=PortfolioList):
        try:
            self.server_host = config.get("DEFAULT", "jupiter_server_host")
        except:
            self.server_host = "127.0.0.1"
        try:
            self.server_port = config.get("DEFAULT", "jupiter_server_port")
        except:
            self.server_port = "8090"

        self.portfoliodata_class = PortfolioData
        tkinter.Tk.__init__(self)
        try:
            self.title(config.get("DEFAULT", "jupiter_title"))
        except:
            self.title("Jupiter UI")
        self.geometry("900x400")

        dir = os.path.dirname(os.path.abspath(__file__))
        self.wm_iconbitmap(os.path.join(dir, "favicon.ico"))
        self.configure(background="#000000")

        self.portfolios = portfoliolist(self._get_url()).get()
        logging.debug("Got portfolios: {0}".format(self.portfolios))

        self.t = PortfolioTable(self)
        self.e = ChoosePortfolio(self, self.portfolios)
        self.b = PortfolioBanner(self)

        self.e.pack(side="top", fill="x", expand=True)
        self.b.pack(fill="x", expand=True, anchor="center")
        self.t.pack(side="top", fill="x", expand=True)

    def _set_portfoliodata(self, prftdata):
        self.portfoliodata_class = prftdata

    def go_pressed(self):
        logging.debug("Get portfolio {0}".format(self.e.option_chosen.get()))
        try:
            prtf_data = self.portfoliodata_class(self._get_url()).get(self.e.option_chosen.get())
        except Exception as g:
            logging.info("Unable to contact Jupiter Server : {0}".format(g))
            return

        logging.info(prtf_data)
        row = 1
        self.b.set(prtf_data['name'], prtf_data['description'])
        try:
            for p in prtf_data['stocks']:
                try:
                    self.t.set(row, 0, p['symbol'])
                    self.t.set(row, 1, p['latestactivity']['lasttradeprice'])
                    self.t.set(row, 2, p['latestactivity']['index'])
                    self.t.set(row, 3, p['latestactivity']['lasttradedatetime'])
                    self.t.set(row, 4, p['latestactivity']['stockid'])
                    self.t.set(row, 5, p['description'])
                    row += 1
                except Exception as e:
                    logging.info("Problem with stock data. {0}\n{1}".format(e, prtf_data['stocks']))
        except Exception as f:
            logging.info("No stock data available. {0}".format(f))

    def _get_url(self):
        return "http://{0}:{1}".format(self.server_host, self.server_port)


class PortfolioBanner(tkinter.Frame):
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

        self.btn = tkinter.Button(self, name="go", text="Go", bg="#000000", fg="#FFFFFF", command=parent.go_pressed)
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

    properties_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              os.path.pardir, os.path.pardir, 'properties'))
    configfile = os.path.join(properties_dir, 'JupiterUI.properties')
    config = configparser.ConfigParser()
    config.read(configfile)

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.DEBUG,
                        filename=os.path.join(logfiledir,
                                              "JupiterUI.{0}.log".format(config.get("DEFAULT", "jupiter_server_port"))),
                        datefmt='%Y%m%d %H:%M:%S')

    logging.info("Starting JupiterUI...")

    app = JupiterUIApp(config)
    app.mainloop()

