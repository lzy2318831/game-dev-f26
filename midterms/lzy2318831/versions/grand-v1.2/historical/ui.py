"""Original monochrome arcade presentation; no historical graphics included."""
import argparse
import math
import time
import tkinter as tk

from .engine import Episode
from .baseline import choose,nibble


class ArcadeApp:
    def __init__(self,root,mode='hvb',heats=2,extended=True,scale=3):
        self.root=root
        self.scale=scale
        self.mode=tk.StringVar(value=mode)
        self.heats=tk.IntVar(value=heats)
        self.extended=tk.BooleanVar(value=extended)
        self.episode=Episode(frames_per_step=1)
        self.screen='start'
        self.closed=False
        self.keys=set()
        self.mouse_down=False
        self.mouse=(128,152)
        self.action=dict(x=8,y=8)
        self.transition_until=0
        self.last_time=time.perf_counter()
        self.accumulator=0
        self.notice=''
        root.title('Pool Shark - Historical Reconstruction')
        root.resizable(False,False)
        root.configure(bg='black')
        root.protocol('WM_DELETE_WINDOW',self.close)
        self.canvas=tk.Canvas(root,width=256*scale,height=278*scale,bg='black',highlightthickness=0)
        self.canvas.pack()
        self.options=tk.Frame(root,bg='black')
        self.options.pack(fill='x',padx=8)
        for value,label in (('hvh','2 HUMANS'),('hvb','HUMAN / BASELINE'),('bvb','DEMO')):
            tk.Radiobutton(self.options,text=label,variable=self.mode,value=value,bg='black',fg='white',selectcolor='#333333',activebackground='black',activeforeground='white').pack(side='left')
        tk.Label(self.options,text='HEATS',bg='black',fg='white').pack(side='left',padx=5)
        tk.Spinbox(self.options,from_=2,to=5,width=2,textvariable=self.heats,bg='#222222',fg='white').pack(side='left')
        tk.Checkbutton(self.options,text='EXTENDED',variable=self.extended,bg='black',fg='white',selectcolor='#333333',activebackground='black').pack(side='left',padx=6)
        buttons=tk.Frame(root,bg='black')
        buttons.pack(fill='x',pady=5)
        for label,command in (('START / RESTART  [R]',self.start),('PAUSE / RESUME  [SPACE]',self.pause),('QUIT  [ESC]',self.close)):
            tk.Button(buttons,text=label,command=command,bg='#222222',fg='white',activebackground='#555555',activeforeground='white',relief='flat').pack(side='left',expand=True)
        root.bind('<KeyPress>',self.key_down)
        root.bind('<KeyRelease>',self.key_up)
        root.bind('<FocusOut>',self.focus_out)
        self.canvas.bind('<Motion>',self.mouse_move)
        self.canvas.bind('<ButtonPress-1>',self.mouse_press)
        self.canvas.bind('<ButtonRelease-1>',self.mouse_release)
        self.canvas.bind('<Leave>',self.mouse_release)
        self.draw()
        root.after(16,self.pump)

    def start(self):
        try:
            self.episode=Episode(heats=self.heats.get(),extended=bool(self.extended.get()),frames_per_step=1)
        except (ValueError,tk.TclError):
            self.notice='CHOOSE 2 TO 5 HEATS'
            self.draw()
            return
        self.screen='playing'
        self.keys.clear()
        self.mouse_down=False
        self.action=dict(x=8,y=8)
        self.transition_until=0
        self.accumulator=0
        self.last_time=time.perf_counter()
        self.notice='PLAYER 1 - STEER THE WHITE BALL'
        self.canvas.focus_set()
        self.draw()

    def close(self):
        self.closed=True
        self.root.destroy()

    def pause(self):
        if self.screen in ('start','over'):
            self.start()
            return
        self.screen='playing' if self.screen=='paused' else 'paused'
        self.keys.clear()
        self.mouse_down=False
        self.accumulator=0
        self.last_time=time.perf_counter()
        self.draw()

    def key_down(self,event):
        key=event.keysym.lower()
        if key in ('space','return'):
            # Ignore OS key-repeat for the pause key until its release.
            if key not in self.keys:
                self.pause()
                self.keys.add(key)
        elif key=='r':
            self.start()
        elif key=='escape':
            self.close()
        else:
            self.keys.add(key)

    def key_up(self,event):
        self.keys.discard(event.keysym.lower())

    def focus_out(self,event=None):
        self.keys.clear()
        self.mouse_down=False

    def mouse_move(self,event):
        self.mouse=(event.x/self.scale,event.y/self.scale)

    def mouse_press(self,event):
        self.mouse_move(event)
        self.mouse_down=True
        self.canvas.focus_set()

    def mouse_release(self,event=None):
        self.mouse_down=False

    def human_action(self):
        if self.mouse_down:
            cue=self.episode.observe(self.episode.active_player)['balls'][0]
            dx,dy=self.mouse[0]-cue['x'],self.mouse[1]-cue['y']
            return dict(x=nibble(max(-1.75,min(1.75,dx/18))),y=nibble(max(-1.75,min(1.75,dy/18))))
        slow='shift_l' in self.keys or 'shift_r' in self.keys
        speed=.75 if slow else 1.75
        dx=int(bool(self.keys & {'right','d'}))-int(bool(self.keys & {'left','a'}))
        dy=int(bool(self.keys & {'down','s'}))-int(bool(self.keys & {'up','w'}))
        return dict(x=nibble(dx*speed),y=nibble(dy*speed))

    def advance(self):
        if self.screen!='playing':
            return
        player=self.episode.active_player
        baseline=self.mode.get()=='bvb' or (self.mode.get()=='hvb' and player=='p2')
        if baseline:
            if self.episode.frames%8==0 or self.action is None:
                # Same public vocabulary; GUI baseline chooses every 8 frames.
                obs=self.episode.observe(player)
                obs['frames_per_step']=8
                self.action=choose(obs,self.episode.legal_actions(player))
        else:
            self.action=self.human_action()
        result=self.episode.step(player,self.action)
        for event in result['events']:
            if event['type']=='segment_end':
                self.keys.clear()
                self.mouse_down=False
                self.action=None
                self.notice=event['reason'].replace('_',' ').upper()+' - NEXT PLAYER'
                self.transition_until=time.perf_counter()+1
            elif event['type']=='bonus':
                self.notice='BONUS +15 - KEEP PLAYING'
            elif event['type']=='pocket' and event['ball']:
                self.notice=f"PLAYER {player[-1]} SCORES"
        if self.episode.reason:
            self.screen='over'
        return result

    def pump(self):
        if self.closed:
            return
        now=time.perf_counter()
        elapsed=min(.1,now-self.last_time)
        self.last_time=now
        if self.screen=='playing' and now>=self.transition_until:
            self.accumulator+=elapsed
            ticks=0
            while self.accumulator>=1/60 and ticks<6 and self.screen=='playing':
                self.advance()
                self.accumulator-=1/60
                ticks+=1
                if time.perf_counter()<self.transition_until:
                    self.accumulator=0
                    break
        else:
            self.accumulator=0
        self.draw()
        self.root.after(8,self.pump)

    def text(self,x,y,label,size=8,fill='white',**kwargs):
        self.canvas.create_text(x,y,text=label,fill=fill,font=('Consolas',max(6,int(size*self.scale)),'bold'),**kwargs)

    def draw(self):
        if self.closed:
            return
        c=self.canvas
        c.delete('all')
        o=self.episode.observe(self.episode.active_player)
        c.create_rectangle(0,0,256,256,fill='#858585',outline='')
        c.create_rectangle(0,0,256,53,fill='black',outline='')
        self.text(64,10,'PLAYER 1',8)
        self.text(192,10,'PLAYER 2',8)
        self.text(64,25,f"{o['scores']['p1']:02}",13)
        self.text(192,25,f"{o['scores']['p2']:02}",13)
        if self.screen!='start':
            self.text(27 if o['active_player']=='p1' else 155,25,'>',11)
        self.text(60,44,f"RACK {o['heat']}/{o['heats']}",8)
        self.text(184,44,f"TIME {o['timer']:02}",8)
        c.create_rectangle(18,57,238,241,fill='black',outline='white',width=1)
        c.create_rectangle(25,65,230,234,fill='#858585',outline='white',width=1)
        for x,y in o['table']['pockets']:
            c.create_oval(x-9,y-9,x+9,y+9,fill='black',outline='white',width=.6)
        # Original diamond marks, not Atari character tiles.
        for y in (99,137,175,211):
            for x in (20,236):
                c.create_polygon(x,y-2,x+2,y,x,y+2,x-2,y,fill='white')
        for ball in sorted(o['balls'],key=lambda b:b['id'],reverse=True):
            x,y=ball['x'],ball['y']
            cue=ball['id']==0
            c.create_oval(x-7,y-7,x+7,y+7,fill='white' if cue else 'black',outline='black' if cue else 'white',width=.6)
            if not cue:
                self.text(x,y,str(ball['id']),5.5)
        if o['bonus_awarded']:
            self.text(128,247,'BONUS',6,fill='black')
        self.text(128,262,'ARROWS / WASD: STEER   SHIFT: SLOW',6)
        self.text(128,273,'OR HOLD MOUSE ON TABLE   RELEASE: STOP',5.5)
        if self.screen in ('start','paused','over'):
            c.create_rectangle(29,90,227,214,fill='black',outline='white',width=1)
            if self.screen=='start':
                self.text(128,110,'POOL SHARK',17)
                self.text(128,130,'BEHAVIORAL RECONSTRUCTION',5.5)
                self.text(128,148,'STEER THE WHITE BALL',8)
                self.text(128,163,'SCORE BEFORE TIME EXPIRES',6)
                self.text(128,176,'SCRATCH ENDS YOUR SEGMENT',6)
                self.text(128,196,'PRESS ENTER TO START',8)
            elif self.screen=='paused':
                self.text(128,135,'PAUSED',17)
                self.text(128,165,'SPACE TO RESUME',8)
            else:
                outcome=self.episode.outcome()
                title='DRAW' if outcome['draw'] else (outcome['winner'].upper()+' WINS' if outcome['winner'] else 'LIMIT REACHED')
                self.text(128,111,'GAME OVER',16)
                self.text(128,137,title,12)
                self.text(128,158,outcome['reason'].replace('_',' ').upper(),6)
                self.text(128,184,'R TO PLAY AGAIN',9)
        elif time.perf_counter()<self.transition_until:
            c.create_rectangle(30,112,226,165,fill='black',outline='white')
            self.text(128,129,f"PLAYER {o['active_player'][-1]} READY",12)
            self.text(128,150,self.notice,5.5)
        if self.notice and self.screen=='start':
            self.text(128,223,self.notice,5,fill='black')
        c.scale('all',0,0,self.scale,self.scale)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('hvh','hvb','bvb'),default='hvb')
    parser.add_argument('--heats',type=int,choices=range(2,6),default=2)
    parser.add_argument('--no-extended',action='store_true')
    parser.add_argument('--scale',type=int,choices=(2,3,4),default=3)
    args=parser.parse_args()
    root=tk.Tk()
    ArcadeApp(root,args.mode,args.heats,not args.no_extended,args.scale)
    root.mainloop()


if __name__=='__main__':
    main()
