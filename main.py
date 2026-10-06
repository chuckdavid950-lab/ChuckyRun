from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label

class RunnerGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.running = False
        self.score = 0
        self.coins = 0
        self.speed = 360
        self.gravity = -1500
        self.jump_power = 650
        self.player_y = 90
        self.velocity_y = 0

        self.obstacles = []
        self.coin_items = []
        self.spawn_timer = 0
        self.coin_timer = 0
        self.score_timer = 0

        self.score_label = Label(
            text="SCORE: 0",
            size_hint=(None,None),
            size=(180,50),
            font_size="20sp",
            bold=True
        )
        self.coin_label = Label(
            text="COINS: 0",
            size_hint=(None,None),
            size=(180,50),
            font_size="20sp",
            bold=True
        )

        self.add_widget(self.score_label)
        self.add_widget(self.coin_label)

        self.start_button = Button(
            text="START RUN",
            size_hint=(None,None),
            size=(220,70),
            pos_hint={"center_x":.5,"center_y":.52},
            font_size="24sp"
        )
        self.start_button.bind(on_release=self.start_game)
        self.add_widget(self.start_button)

        self.jump_button = Button(
            text="JUMP",
            size_hint=(None,None),
            size=(150,75),
            pos_hint={"right":.96,"y":.04},
            font_size="22sp"
        )
        self.jump_button.bind(on_release=self.jump)
        self.add_widget(self.jump_button)

        self.restart_button = Button(
            text="RESTART",
            size_hint=(None,None),
            size=(200,65),
            pos_hint={"center_x":.5,"center_y":.45},
            font_size="22sp"
        )
        self.restart_button.bind(on_release=self.start_game)
        self.restart_button.opacity = 0
        self.restart_button.disabled = True
        self.add_widget(self.restart_button)

        self.message = Label(
            text="",
            size_hint=(1,None),
            height=100,
            pos_hint={"center_x":.5,"center_y":.62},
            font_size="30sp",
            bold=True
        )
        self.add_widget(self.message)

        self.bind(size=self.resize)
        Clock.schedule_interval(self.update, 1/60)

    def resize(self,*args):
        self.score_label.pos = (15,self.height-55)
        self.coin_label.pos = (200,self.height-55)

    def start_game(self,*args):
        self.running = True
        self.score = 0
        self.coins = 0
        self.speed = 360
        self.player_y = 90
        self.velocity_y = 0
        self.obstacles = []
        self.coin_items = []

        self.start_button.opacity = 0
        self.start_button.disabled = True
        self.restart_button.opacity = 0
        self.restart_button.disabled = True
        self.message.text = ""

        self.update_labels()

    def jump(self,*args):
        if self.running and self.player_y <= 92:
            self.velocity_y = self.jump_power

    def on_touch_down(self,touch):
        if self.running:
            self.jump()
            return True
        return super().on_touch_down(touch)

    def spawn_obstacle(self):
        self.obstacles.append({
            "x": self.width + 20,
            "y": 80,
            "w": randint(35,65),
            "h": randint(45,95)
        })

    def spawn_coin(self):
        self.coin_items.append({
            "x": self.width + 20,
            "y": randint(150,max(170,int(self.height-180))),
            "r": 14
        })

    def collision(self,a,b):
        return (
            a["x"] < b["x"]+b["w"] and
            a["x"]+a["w"] > b["x"] and
            a["y"] < b["y"]+b["h"] and
            a["y"]+a["h"] > b["y"]
        )

    def update(self,dt):
        if not self.running:
            self.draw()
            return

        self.velocity_y += self.gravity*dt
        self.player_y += self.velocity_y*dt

        if self.player_y <= 90:
            self.player_y = 90
            self.velocity_y = 0

        self.speed += 3*dt
        self.spawn_timer += dt
        self.coin_timer += dt
        self.score_timer += dt

        if self.spawn_timer >= 1.35:
            self.spawn_timer = 0
            self.spawn_obstacle()

        if self.coin_timer >= 1:
            self.coin_timer = 0
            self.spawn_coin()

        for o in self.obstacles:
            o["x"] -= self.speed*dt

        for c in self.coin_items:
            c["x"] -= self.speed*dt

        self.obstacles = [o for o in self.obstacles if o["x"] > -100]
        self.coin_items = [c for c in self.coin_items if c["x"] > -50]

        player = {
            "x":75,
            "y":self.player_y,
            "w":48,
            "h":58
        }

        for o in self.obstacles:
            if self.collision(player,o):
                self.game_over()
                return

        remaining = []

        for c in self.coin_items:
            box = {
                "x":c["x"]-c["r"],
                "y":c["y"]-c["r"],
                "w":c["r"]*2,
                "h":c["r"]*2
            }

            if self.collision(player,box):
                self.coins += 1
            else:
                remaining.append(c)

        self.coin_items = remaining

        if self.score_timer >= .1:
            self.score_timer = 0
            self.score += 1
            self.update_labels()

        self.draw()

    def update_labels(self):
        self.score_label.text = f"SCORE: {self.score}"
        self.coin_label.text = f"COINS: {self.coins}"

    def game_over(self):
        self.running = False

        self.message.text = (
            f"GAME OVER\n"
            f"Score: {self.score}   Coins: {self.coins}"
        )

        self.restart_button.opacity = 1
        self.restart_button.disabled = False

    def draw(self):
        self.canvas.clear()

        with self.canvas:

            # Sky
            Color(.45,.75,1,1)
            Rectangle(pos=(0,0),size=self.size)

            # Sun
            Color(1,.85,.2,1)
            Ellipse(
                pos=(self.width-110,self.height-130),
                size=(75,75)
            )

            # Ground
            Color(.25,.65,.25,1)
            Rectangle(
                pos=(0,0),
                size=(self.width,80)
            )

            # Player body
            Color(.9,.12,.12,1)
            RoundedRectangle(
                pos=(75,self.player_y),
                size=(48,58),
                radius=[10]
            )

            # Head
            Color(1,.78,.55,1)
            Ellipse(
                pos=(80,self.player_y+35),
                size=(38,38)
            )

            # Eye
            Color(0,0,0,1)
            Ellipse(
                pos=(105,self.player_y+53),
                size=(5,5)
            )

            # Obstacles
            for o in self.obstacles:
                Color(.3,.2,.12,1)
                RoundedRectangle(
                    pos=(o["x"],o["y"]),
                    size=(o["w"],o["h"]),
                    radius=[8]
                )

            # Coins
            for c in self.coin_items:
                Color(1,.82,.05,1)
                Ellipse(
                    pos=(c["x"]-c["r"],c["y"]-c["r"]),
                    size=(c["r"]*2,c["r"]*2)
                )


class ChuckyRunApp(App):

    title = "Chucky Run"

    def build(self):
        Window.clearcolor = (.45,.75,1,1)
        return RunnerGame()


if __name__ == "__main__":
    ChuckyRunApp().run()
