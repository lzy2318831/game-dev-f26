"""Minimal tkinter table. Only the engine commits rules and score."""
import argparse
import math
import tkinter as tk
from tkinter import ttk

from .engine import Episode
from .baseline import choose


class TableApp:
    def __init__(self, root, mode='hvb'):
        self.root, self.mode = root, mode
        self.episode = Episode()
        self.busy = False
        self.closed = False
        self.angle = tk.IntVar(value=0)
        self.power = tk.IntVar(value=2)
        self.message = tk.StringVar(value='Click the table to aim, then Shoot.')
        root.title('Six-ball Pool — competitive billiards')
        root.resizable(False, False)
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.status = ttk.Label(root, font=('Segoe UI', 13))
        self.status.pack(pady=8)
        self.canvas = tk.Canvas(root, width=1040, height=540, bg='#553722', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind('<Motion>', self.aim)
        self.canvas.bind('<Button-1>', self.aim)
        controls = ttk.Frame(root)
        controls.pack(fill='x', padx=15, pady=8)
        ttk.Label(controls, text='Direction (degrees)').pack(side='left')
        self.angle_control = tk.Spinbox(controls, from_=0, to=359, textvariable=self.angle, width=5, command=self.draw)
        self.angle_control.pack(side='left', padx=8)
        ttk.Label(controls, text='Power').pack(side='left')
        for p in (1, 2, 3):
            ttk.Radiobutton(controls, text=str(p), variable=self.power, value=p, command=self.draw).pack(side='left')
        self.shoot_button = ttk.Button(controls, text='Shoot (Space)', command=self.shoot)
        self.shoot_button.pack(side='left', padx=15)
        self.restart_button = ttk.Button(controls, text='Restart (R)', command=self.restart)
        self.restart_button.pack(side='right')
        ttk.Label(root, textvariable=self.message).pack(pady=5)
        ttk.Label(root, text='Each object = 1 point • Scratch = 0 points for shot • Turns always alternate • 24 attempts', foreground='#444444').pack(pady=4)
        root.bind('<space>', lambda event: self.shoot())
        root.bind('r', lambda event: self.restart())
        root.bind('<Escape>', lambda event: self.close())
        root.bind('<Left>', lambda event: self.adjust(-1))
        root.bind('<Right>', lambda event: self.adjust(1))
        self.draw()

    def close(self):
        self.closed = True
        self.root.destroy()

    def human_turn(self):
        return self.mode == 'hvh' or self.episode.active_player == 'p1'

    def adjust(self, delta):
        if not self.busy:
            self.angle.set((self.angle.get() + delta) % 360)
            self.draw()

    def aim(self, event):
        if self.busy or self.episode.reason or not self.human_turn():
            return
        cue = self.episode.observe(self.episode.active_player)['balls'][0]
        self.angle.set(round(math.degrees(math.atan2(event.y - 20 - cue['y'], event.x - 20 - cue['x']))) % 360)
        self.draw()

    def restart(self):
        if self.busy:
            return
        self.episode.reset()
        self.message.set('New match. Click to aim; choose power, then Shoot.')
        self.draw()

    def draw(self, observation=None):
        if self.closed:
            return
        o = observation or self.episode.observe(self.episode.active_player)
        c = self.canvas
        c.delete('all')
        c.create_rectangle(20, 20, 1020, 520, fill='#176447', outline='#dfb877', width=3)
        for x, y in o['table']['pockets']:
            c.create_oval(x - 4, y - 4, x + 44, y + 44, fill='#101919', outline='#b29867', width=2)
        colors = ['white', '#ffce42', '#68b5ff', '#f87575', '#c98cff', '#f49945', '#66d3c0']
        for b in o['balls']:
            x, y = b['x'] + 20, b['y'] + 20
            c.create_oval(x - 10, y - 10, x + 10, y + 10, fill=colors[b['id']], outline='#162c24', width=1)
            if b['id']:
                c.create_text(x, y, text=str(b['id']), fill='#111111', font=('Segoe UI', 9, 'bold'))
        if not self.busy and not self.episode.reason:
            cue = next(b for b in o['balls'] if b['id'] == 0)
            try:
                angle = self.angle.get() % 360
            except tk.TclError:
                angle = 0
            r = math.radians(angle)
            length = 80 + 35 * self.power.get()
            c.create_line(cue['x'] + 20, cue['y'] + 20, cue['x'] + 20 + length * math.cos(r), cue['y'] + 20 + length * math.sin(r), fill='#f8f1cb', dash=(6, 4), arrow='last', width=2)
        out = self.episode.outcome()
        label = 'Human vs Human' if self.mode == 'hvh' else 'Human (P1) vs Geometric Baseline (P2)'
        self.status.config(text=f"{label}   |   P1 {o['scores']['p1']} : {o['scores']['p2']} P2   |   Turn {o['active_player'].upper()}   |   Attempts left {o['attempts_remaining']}")
        if out['status'] == 'terminal':
            result = ('Execution failure' if out['failure'] else ('Draw' if out['draw'] else out['winner'].upper() + ' wins'))
            c.create_rectangle(280, 220, 760, 320, fill='#10291f', outline='#dfb877')
            c.create_text(520, 255, text=result, fill='white', font=('Segoe UI', 25, 'bold'))
            c.create_text(520, 290, text=out['reason'] + ' — press R to restart', fill='white')

    def shoot(self):
        if self.busy or self.episode.reason or not self.human_turn():
            return
        try:
            action = dict(angle=self.angle.get(), power=self.power.get())
        except tk.TclError:
            self.message.set('Enter an integer direction from 0 to 359.')
            return
        if not self.episode.valid(action):
            self.message.set('Direction must be 0–359; power must be 1–3.')
            return
        self.resolve(action)

    def resolve(self, action):
        self.busy = True
        self.shoot_button.config(state='disabled')
        self.restart_button.config(state='disabled')
        def frame(observation):
            if self.closed:
                return
            self.draw(observation)
            self.root.update()
            # Schedule-based frame pacing is unnecessary for rule execution;
            # this is a fast shot preview, not real-time gameplay.
        try:
            result = self.episode.step(self.episode.active_player, action, frame_callback=frame)
        finally:
            self.busy = False
        if self.closed:
            return
        self.message.set('Shot: ' + str(action) + '  ' + (str(result['events']) if result['events'] else 'No pocket.'))
        self.shoot_button.config(state='normal')
        self.restart_button.config(state='normal')
        self.draw()
        if not self.episode.reason and not self.human_turn():
            self.root.after(400, self.baseline_turn)

    def baseline_turn(self):
        if self.closed or self.busy or self.episode.reason or self.human_turn():
            return
        action = choose(self.episode.observe('p2'), self.episode.legal_actions('p2'))
        self.angle.set(action['angle'])
        self.power.set(action['power'])
        self.resolve(action)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('hvh', 'hvb'), default='hvb')
    args = parser.parse_args()
    root = tk.Tk()
    TableApp(root, args.mode)
    root.mainloop()


if __name__ == '__main__':
    main()
