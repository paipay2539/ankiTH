from gtts import gTTS
from playsound import playsound
import time
time_start = time.time()
tts=gTTS(text='สวัสดีโลก',lang='th')
tts.save('hello_world.mp3')
print(time.time()-time_start)
#tts=gTTS(text='価格',lang='ja')
#tts.save('hello_world.mp3')
playsound('hello_world.mp3')
