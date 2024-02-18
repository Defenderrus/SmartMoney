import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mycolorpy import colorlist as mcp
import matplotlib.pyplot as plt


class Charts:
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

    def plot(self, incomes_category, expenses_category):
        self.incomes, self.expenses = incomes_category, expenses_category
        self.fig.clear()
        plt.subplots_adjust(wspace=0.8, hspace=0.8)
        self.fig.suptitle("Диаграммы", color="w", fontweight="bold", size=14)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.color_g, self.color_r = mcp.gen_color(cmap="YlGn_r", n=9), mcp.gen_color(cmap="YlOrRd_r", n=17)
        self.annotation1 = self.ax1.annotate("", xy=(0, 0), xytext=(-80, 40), textcoords="offset points",
                                             color='white', fontsize=9, bbox=dict(boxstyle="round", fc="black", ec="g", lw=2),
                                             arrowprops=dict(arrowstyle="->"))
        self.annotation2 = self.ax2.annotate("", xy=(0, 0), xytext=(-20, 40), textcoords="offset points",
                                             color='white', fontsize=9, bbox=dict(boxstyle="round", fc="black", ec="r", lw=2),
                                             arrowprops=dict(arrowstyle="->"))
        self.wedges1, _, self.perc1 = self.ax1.pie(self.incomes.values(), labels=self.incomes.keys(), autopct='%1.2f%%',
                                                   textprops={'visible': False}, colors=self.color_g, startangle=270)
        self.wedges2, _, self.perc2 = self.ax2.pie(self.expenses.values(), labels=self.expenses.keys(), autopct='%1.2f%%',
                                                   textprops={'visible': False}, colors=self.color_r, startangle=270)
        self.annotation1.set_visible(False)
        self.annotation2.set_visible(False)
        self.ax1.set_title("Доходы", color="w", size=11)
        self.ax2.set_title("Расходы", color="w", size=11)
        self.ax1.axis('equal')
        self.ax2.axis('equal')
        self.canvas.draw()

    def hover(self, event):
        if self.selected_wedge is not None:
            self.selected_wedge.set_center((0, 0))
            self.selected_wedge = None
        if event.inaxes == self.ax1:
            for i, w in enumerate(self.wedges1):
                if w.contains_point([event.x, event.y]):
                    w.set_facecolor("#00ff0099")
                    self.annotation1.set_text(f'Категория: {w.get_label()}\n'
                                              f'Сумма: {'{:,.2f}'.format(self.incomes[w.get_label()])} руб.\n'
                                              f'В процентах: {self.perc1[i]._text}')
                    self.annotation1.xy = (event.xdata, event.ydata)
                    self.annotation1.set_visible(True)
                    theta = np.radians((w.theta1 + w.theta2) / 2)
                    w.set_center((.2 * np.cos(theta), .2 * np.sin(theta)))
                    self.selected_wedge = w
                else:
                    w.set_facecolor(self.color_g[i])
                self.fig.canvas.draw_idle()
        if event.inaxes == self.ax2:
            for i, w in enumerate(self.wedges2):
                if w.contains_point([event.x, event.y]):
                    w.set_facecolor("#ff000099")
                    self.annotation2.set_text(f'Категория: {w.get_label()}\n'
                                              f'Сумма: {'{:,.2f}'.format(self.expenses[w.get_label()])} руб.\n'
                                              f'В процентах: {self.perc2[i]._text}')
                    self.annotation2.xy = (event.xdata, event.ydata)
                    self.annotation2.set_visible(True)
                    theta = np.radians((w.theta1 + w.theta2) / 2)
                    w.set_center((.2 * np.cos(theta), .2 * np.sin(theta)))
                    self.selected_wedge = w
                else:
                    w.set_facecolor(self.color_r[i])
                self.fig.canvas.draw_idle()
        if self.selected_wedge is None and (self.annotation1.get_visible() or self.annotation2.get_visible()):
            self.annotation1.set_visible(False)
            self.annotation2.set_visible(False)
            self.fig.canvas.draw_idle()
