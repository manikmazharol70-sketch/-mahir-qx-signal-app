from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class CandleChart(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prices = [288.42]
        random.seed(7)
        for _ in range(42):
            self.prices.append(self.prices[-1] + random.choice([-1, -0.5, -0.2, 0.15, 0.3, 0.55]) / 100)
        self.signal = "WAIT"
        self.bind(pos=self.redraw, size=self.redraw)

    def add_candle(self):
        step = random.choice([-0.55, -0.3, -0.15, 0.12, 0.25, 0.5]) / 100
        self.prices.append(self.prices[-1] + step)
        self.prices = self.prices[-42:]
        if len(self.prices) >= 12:
            fast = sum(self.prices[-5:]) / 5
            slow = sum(self.prices[-12:]) / 12
            self.signal = "UP" if fast >= slow else "DOWN"
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        if len(self.prices) < 2 or self.width <= 0 or self.height <= 0:
            return
        lo, hi = min(self.prices), max(self.prices)
        pad = (hi - lo) * 0.15 + 0.001
        lo -= pad; hi += pad

        with self.canvas:
            Color(0.055, 0.07, 0.12, 1)
            Rectangle(pos=self.pos, size=self.size)

            # grid
            Color(0.14, 0.18, 0.25, 1)
            for i in range(1, 6):
                y = self.y + self.height * i / 6
                Line(points=[self.x, y, self.right, y], width=0.7)
            for i in range(1, 7):
                x = self.x + self.width * i / 7
                Line(points=[x, self.y, x, self.top], width=0.7)

            n = len(self.prices)
            cw = self.width / n
            for i in range(1, n):
                o = self.prices[i-1]
                c = self.prices[i]
                x = self.x + i*cw + cw*0.18
                body_w = cw*0.64
                y1 = self.y + (o-lo)/(hi-lo)*self.height
                y2 = self.y + (c-lo)/(hi-lo)*self.height
                top = max(y1, y2)
                bottom = min(y1, y2)
                h = max(dp(4), top-bottom)

                # candle color
                if c >= o:
                    Color(0.0, 0.75, 0.42, 1)
                else:
                    Color(1.0, 0.30, 0.16, 1)
                Rectangle(pos=(x, bottom), size=(body_w, h))
                Line(points=[x+body_w/2, bottom-dp(7), x+body_w/2, top+dp(7)], width=1)

            # current price line
            cp = self.prices[-1]
            y = self.y + (cp-lo)/(hi-lo)*self.height
            Color(0.35, 0.75, 1, 1)
            Line(points=[self.x, y, self.right, y], width=1.2)

class SignalApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(6))

        top = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        title = Label(text="[b]MARKET SIGNAL[/b]", markup=True, font_size=dp(19), halign="left")
        balance = Label(text="LIVE   $3.78", font_size=dp(15), halign="right")
        top.add_widget(title); top.add_widget(balance)
        root.add_widget(top)

        pair = BoxLayout(size_hint_y=None, height=dp(38))
        pair.add_widget(Label(text="🌐  USD/PKR  OTC    94%", font_size=dp(15)))
        self.status = Label(text="WAITING", font_size=dp(15))
        pair.add_widget(self.status)
        root.add_widget(pair)

        self.chart = CandleChart()
        root.add_widget(self.chart)

        info = GridLayout(cols=2, size_hint_y=None, height=dp(76), spacing=dp(6))
        self.timer = Label(text="Timer\n00:00:05", font_size=dp(18))
        self.invest = Label(text="Investment\n$1", font_size=dp(18))
        info.add_widget(self.timer); info.add_widget(self.invest)
        root.add_widget(info)

        self.signal_label = Label(text="SIGNAL: WAITING", font_size=dp(25), bold=True,
                                  size_hint_y=None, height=dp(48))
        root.add_widget(self.signal_label)

        buttons = BoxLayout(size_hint_y=None, height=dp(58), spacing=dp(8))
        up = Button(text="UP  ↑", font_size=dp(20))
        down = Button(text="DOWN  ↓", font_size=dp(20))
        up.bind(on_release=lambda *_: self.manual("UP"))
        down.bind(on_release=lambda *_: self.manual("DOWN"))
        buttons.add_widget(up); buttons.add_widget(down)
        root.add_widget(buttons)

        self.history = Label(text="History:  —", font_size=dp(14), size_hint_y=None, height=dp(42))
        root.add_widget(self.history)

        self.seconds = 5
        self.results = []
        Clock.schedule_interval(self.tick, 1)
        return root

    def tick(self, dt):
        self.seconds -= 1
        self.chart.add_candle()
        if self.seconds <= 0:
            self.seconds = 5
            sig = self.chart.signal
            self.signal_label.text = f"SIGNAL: {sig}"
            self.status.text = f"{sig}  •  NEW"
            self.results.insert(0, sig)
            self.results = self.results[:6]
            self.history.text = "History: " + "  |  ".join(self.results)
        self.timer.text = f"Timer\n00:00:{self.seconds:02d}"

    def manual(self, sig):
        self.signal_label.text = f"DEMO: {sig}"
        self.status.text = f"{sig}  •  DEMO"

if __name__ == "__main__":
    SignalApp().run()
