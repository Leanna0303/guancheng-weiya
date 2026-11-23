# Original festive pentatonic loop, synthesized from scratch (no samples) -> royalty-free.
import numpy as np, wave
SR=44100; BPM=100; BEAT=60/BPM; BARS=16; L=int(SR*BEAT*4*BARS)
rng=np.random.default_rng(7)
out=np.zeros((L,2))
def hz(n): return 440*2**((n-69)/12)
def put(sig,t,pan=0.0,gain=1.0):
    i=int(t*SR)%L; n=len(sig)
    l=np.sqrt(0.5*(1-pan))*gain; r=np.sqrt(0.5*(1+pan))*gain
    for k in range(0,n):
        pass
    end=i+n
    if end<=L: out[i:end,0]+=sig*l; out[i:end,1]+=sig*r
    else:
        a=L-i; out[i:,0]+=sig[:a]*l; out[i:,1]+=sig[:a]*r; out[:n-a,0]+=sig[a:]*l; out[:n-a,1]+=sig[a:]*r
def pluck(f,dur,bright=0.5,decay=0.996):
    N=int(SR/f); buf=rng.uniform(-1,1,N)
    # soften the excitation
    for _ in range(int(3*(1-bright))+1): buf=0.5*(buf+np.roll(buf,1))
    n=int(dur*SR); y=np.zeros(n); b=buf.copy(); j=0
    for k in range(n):
        y[k]=b[j]; nj=(j+1)%N; b[j]=decay*0.5*(b[j]+b[nj]); j=nj
    env=np.minimum(1,np.arange(n)/(0.002*SR)); return y*env
def pad(fs,dur):
    n=int(dur*SR); t=np.arange(n)/SR; y=np.zeros(n)
    for f in fs:
        for d in (-0.6,0.6): y+=np.sin(2*np.pi*f*(1+d/1200)*t)+0.25*np.sin(4*np.pi*f*t)
    att=np.minimum(1,t/0.6); rel=np.minimum(1,(dur-t)/0.8); return y*att*np.clip(rel,0,1)/len(fs)
def bell(f,dur=2.5):
    n=int(dur*SR); t=np.arange(n)/SR
    y=np.sin(2*np.pi*f*t)*np.exp(-t*2.2)+0.5*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*4)+0.25*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*7)
    return y*np.minimum(1,t/0.003)
def block(f=900):
    n=int(0.12*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*1.6*t))*np.exp(-t*45)
def drum():
    n=int(0.5*SR); t=np.arange(n)/SR; f=95*np.exp(-t*6)+48
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)+0.15*rng.uniform(-1,1,n)*np.exp(-t*40)
B=BEAT
# chord per bar (root midi, triad notes) : C  Am  F  G | C  Em  F  G | Am Em F C | F  G  C  C
prog=[(48,[60,64,67]),(45,[57,60,64]),(41,[57,60,65]),(43,[55,59,62]),
      (48,[60,64,67]),(40,[55,59,64]),(41,[57,60,65]),(43,[55,59,62]),
      (45,[57,60,64]),(40,[55,59,64]),(41,[57,60,65]),(48,[55,60,64]),
      (41,[57,60,65]),(43,[55,59,62]),(48,[55,60,64]),(48,[55,60,64])]
# melody: (beat offset within piece, midi, length beats) - gong pentatonic C D E G A
mel=[]
phr=[ [(0,72,1),(1,74,.5),(1.5,76,.5),(2,79,1),(3,76,1)],
      [(0,81,1.5),(1.5,79,.5),(2,76,1),(3,74,1)],
      [(0,72,.5),(.5,74,.5),(1,76,1),(2,74,.5),(2.5,72,.5),(3,69,1)],
      [(0,74,2),(2,76,.5),(2.5,79,.5),(3,74,1)],
      [(0,72,1),(1,74,.5),(1.5,76,.5),(2,79,1),(3,81,1)],
      [(0,84,1.5),(1.5,81,.5),(2,79,1),(3,76,1)],
      [(0,77,.5),(.5,76,.5),(1,74,1),(2,72,.5),(2.5,74,.5),(3,76,1)],
      [(0,74,3),(3,79,1)],
      [(0,81,1),(1,79,.5),(1.5,81,.5),(2,84,1),(3,81,1)],
      [(0,79,1.5),(1.5,76,.5),(2,79,1),(3,83,1)],
      [(0,81,.5),(.5,79,.5),(1,77,1),(2,76,.5),(2.5,74,.5),(3,72,1)],
      [(0,76,2),(2,79,1),(3,76,1)],
      [(0,72,.5),(.5,74,.5),(1,76,.5),(1.5,79,.5),(2,81,1),(3,79,1)],
      [(0,76,.5),(.5,79,.5),(1,74,1),(2,76,1),(3,74,1)],
      [(0,72,3),(3,67,1)],
      [(0,69,1),(1,72,1),(2,74,1),(3,79,1)]]
for bar,notes in enumerate(phr):
    for (o,m,l) in notes: mel.append((bar*4+o,m,l))
for (bt,m,l) in mel:
    put(pluck(hz(m),max(1.2,l*B+0.8),bright=0.7,decay=0.9975),bt*B,pan=0.15,gain=0.42)
    if l>=1.5: put(pluck(hz(m+12),1.0,bright=0.5,decay=0.993),bt*B+0.012,pan=0.4,gain=0.10)
for bar,(root,tri) in enumerate(prog):
    t0=bar*4*B
    put(pad([hz(n) for n in tri],4*B+0.6),t0,gain=0.11)
    # bass pluck on 1 and 3, arpeggio on off-beats
    put(pluck(hz(root),2.0,bright=0.3,decay=0.998),t0,pan=-0.1,gain=0.38)
    put(pluck(hz(root+7),1.6,bright=0.3,decay=0.998),t0+2*B,pan=-0.1,gain=0.28)
    arp=[tri[0],tri[1],tri[2],tri[1]]
    for k in range(4): put(pluck(hz(arp[k]),0.9,bright=0.4,decay=0.994),t0+(k+0.5)*B,pan=-0.45,gain=0.13)
    put(drum(),t0,gain=0.30)
    if bar%2==1: put(drum(),t0+2.5*B,gain=0.18)
    for k in (1,3): put(block(1000),t0+k*B,pan=0.5,gain=0.10)
    put(block(1350),t0+3.5*B,pan=0.5,gain=0.06)
    if bar%4==0: put(bell(hz(84 if bar!=8 else 88)),t0,pan=0.6,gain=0.10)
# simple stereo reverb (feedback combs), wrapped around for a seamless loop
def reverb(x,delays,fb):
    y=np.zeros_like(x)
    for d in delays:
        d=int(d*SR); c=x.copy()
        for _ in range(6): c=np.roll(c,d)*fb; y+=c
    return y/len(delays)
wet=np.stack([reverb(out[:,0],[0.0297,0.0371,0.0411,0.0437],0.55),reverb(out[:,1],[0.0313,0.0353,0.0429,0.0451],0.55)],1)
mix=out+0.35*wet
# gentle low-pass + normalize
for ch in (0,1):
    y=mix[:,ch]; z=np.zeros_like(y); a=0.35; acc=0
    z=np.convolve(y,np.ones(3)/3,mode='same'); mix[:,ch]=z
mix/=np.max(np.abs(mix))*1.12
pcm=(mix*32767).astype(np.int16)
with wave.open('/home/claude/music/loop.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('seconds',L/SR)
