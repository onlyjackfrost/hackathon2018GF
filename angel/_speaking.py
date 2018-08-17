# Reading from input.txt, and speaking out in Mandarin
import asyncio
import tempfile
import websockets
import time
import os
import hashlib
import aiy.audio  # noqa # pylint: disable=import-error
import aiy.voicehat  # noqa # pylint: disable=import-error
from gtts import gTTS
from ._player import simple_player
from ._recorder import simple_recorder
from .logging import logger


PJ = os.path.join
this_dir = os.path.dirname(os.path.abspath(__file__))

led = aiy.voicehat.get_led()

async def ws_to_tts(speaker_queue, lang='zh-tw'):
    try:
        sentence = await speaker_queue.get()
    except Exception:
        return 1
    logger.info('Speaking: Calling gTTS')
    tts = gTTS(sentence, lang=lang, lang_check=False)
    led.set_state(led.ON)
    with tempfile.TemporaryFile() as tempf:
        tts.write_to_fp(tempf)
        tempf.seek(0)
        logger.info('Speaking: Speaking...')
        simple_player.play_bytes(tempf) # simple_player.play_bytes() plays the audio
    led.set_state(led.OFF)
    return 0

# Function read_from_file() added by monmon
async def read_from_file(speaker_queue, fileName):
    logger.info('Speaking: Reading from %s.' % fileName)
    for L in open(fileName,'r',encoding='UTF-8'):
        await asyncio.sleep(0.5)
        await speaker_queue.put(L)
        if len(L) == 0:
            break
        logger.info(L)

    logger.info('Speaking: Finish reading from file.')

    return 0;

def speaking(fileName):

    led.set_state(led.PULSE_QUICK)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    speaker_queue = asyncio.Queue()

    try:
        loop.run_until_complete(
            asyncio.gather(read_from_file(speaker_queue, fileName),
                           ws_to_tts(speaker_queue))
        )

    except Exception as err:
        logger.error(err)
        loop.stop()
        loop.run_forever()

    finally:
        loop.close()
        led.set_state(led.OFF)
    logger.info('Speaking: Done')


if __name__ == '__main__':
    with open(PJ(this_dir, 'res/init.mp3'), 'rb') as fd:
        simple_player.play_bytes(fd)
    led.set_state(led.BLINK_3)
    time.sleep(2)
    led.set_state(led.OFF)

    #button = aiy.voicehat.get_button()
    #button.on_press(speaking('input.txt')) #這樣寫之後按鈕會失效
    speaking('input.txt')

    #try:
    #    while True:
    #        time.sleep(1)
    #except KeyboardInterrupt:
    #    pass

    #finally:
    led.set_state(led.OFF)
    led.stop()
