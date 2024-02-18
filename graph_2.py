from datetime import date
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as md


class Curves:
    def __init__(self):
        plt.style.use('seaborn-v0_8-dark')
        self.selected_wedge = None
        self.fig = plt.figure()
        self.fig.set_size_inches(7.5, 4)
        self.fig.set_facecolor("#ffffff00")
        self.fig.tight_layout()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)

    def plot(self, incomes, expenses):
        self.xdata1 = [date(*list(map(int, key.split("-")))) for key in incomes.keys()]
        self.xdata2 = [date(*list(map(int, key.split("-")))) for key in expenses.keys()]
        self.ydata1, self.ydata2 = list(incomes.values()), list(expenses.values())
        self.fig.clear()
        plt.subplots_adjust(wspace=0.4, hspace=0.4)
        self.fig.suptitle("Графики", color="w", fontweight="bold", size=13)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.annotation1 = self.ax1.annotate("", xy=(0, 0), xytext=(-20, -40), textcoords="offset points",
                                             color='white', fontsize=9, bbox=dict(boxstyle="round", fc="black", ec="g", lw=2),
                                             arrowprops=dict(arrowstyle="->"))
        self.annotation2 = self.ax2.annotate("", xy=(0, 0), xytext=(-80, -40), textcoords="offset points",
                                             color='white', fontsize=9, bbox=dict(boxstyle="round", fc="black", ec="r", lw=2),
                                             arrowprops=dict(arrowstyle="->"))
        self.annotation1.set_visible(False)
        self.annotation2.set_visible(False)
        self.ax1.tick_params(axis='x', colors="w", labelsize=9)
        self.ax1.tick_params(axis='y', colors="w", labelsize=9)
        self.ax1.xaxis.set_major_formatter(md.DateFormatter("%d %b %Y"))
        self.ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, pos: '{0:,}'.format(int(y)).replace(',', '.')))
        self.ax1.plot(self.xdata1, self.ydata1, ".-", color="g")
        self.ax1.set_title("Доходы", color="w", size=11)
        self.ax1.set_ylim(0)
        self.ax1.grid()
        self.ax2.tick_params(axis='x', colors="w", labelsize=9)
        self.ax2.tick_params(axis='y', colors="w", labelsize=9)
        self.ax2.xaxis.set_major_formatter(md.DateFormatter("%d %b %Y"))
        self.ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, pos: '{0:,}'.format(int(y)).replace(',', '.')))
        self.ax2.plot(self.xdata2, self.ydata2, ".-", color="r")
        self.ax2.set_title("Расходы", color="w", size=11)
        self.ax2.set_ylim(0)
        self.ax2.grid()
        self.fig.autofmt_xdate()
        self.canvas.draw()

    def hover(self, event):
        if self.selected_wedge is not None:
            self.selected_wedge = None
        if event.inaxes == self.ax1:
            for i, date in enumerate(self.xdata1):
                if (abs(md.date2num(date) - event.xdata) < ((max(self.xdata1) - min(self.xdata1)).days+1) / 72 and
                        abs(self.ydata1[i] - event.ydata) < max(self.ydata1) / 50):
                    self.annotation1.set_text(f'Дата: {self.xdata1[i].strftime("%d %b %Y")}\n'
                                              f'Сумма: {'{:,.2f}'.format(self.ydata1[i])} руб.')
                    self.annotation1.xy = (event.xdata, event.ydata)
                    self.annotation1.set_visible(True)
                    self.selected_wedge = date
                    self.fig.canvas.draw_idle()
        if event.inaxes == self.ax2:
            for i, date in enumerate(self.xdata2):
                if (abs(md.date2num(date) - event.xdata) < ((max(self.xdata2) - min(self.xdata2)).days+1) / 72 and
                        abs(self.ydata2[i] - event.ydata) < max(self.ydata2) / 50):
                    self.annotation2.set_text(f'Дата: {self.xdata2[i].strftime("%d %b %Y")}\n'
                                              f'Сумма: {'{:,.2f}'.format(self.ydata2[i])} руб.')
                    self.annotation2.xy = (event.xdata, event.ydata)
                    self.annotation2.set_visible(True)
                    self.selected_wedge = date
                    self.fig.canvas.draw_idle()
        if self.selected_wedge is None and (self.annotation1.get_visible() or self.annotation2.get_visible()):
            self.annotation1.set_visible(False)
            self.annotation2.set_visible(False)
            self.fig.canvas.draw_idle()
