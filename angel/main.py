# Project Angel
import os
import aiy.audio
import aiy.voicehat
import time
import hashlib
import json
from ._speaking import speaking, speaking_from_file
from .transition import transition
from ._recording import recording
from ._player import simple_player
from ._recorder import simple_recorder
from .logging import logger

PJ = os.path.join
this_dir = os.path.dirname(os.path.abspath(__file__))

led = aiy.voicehat.get_led()
button = aiy.voicehat.get_button()

def main():

    logger.info('Main: press the button')
    #speaking_from_file('testing.txt')
    speaking_from_file('intro.txt')
    button.wait_for_press()
    asking = recording()
    if asking == '旅遊':
        logger.info('Main: Asking about sightseeing spot')
        speaking('旅遊還沒接上喔')

    elif asking == '交通':
        logger.info('Main: Asking about transportation')
        speaking('您的目的地是')
        button.wait_for_press()
        destination = recording()

        transition(destination)
        speaking_from_file('transition_cost.txt')

        try:
            while True:
                button.wait_for_press()
                transportation = recording()

                # bus, tram, walking are the keywords for google Maps API
                if transportation=='公車':
                    speaking_from_file('bus_detail.txt')
                    break
                elif transportation=='捷運':
                    speaking_from_file('tram_detail.txt')
                    break
                elif transportation=='腳踏車':
                    #speaking_from_file('ubike_detail.txt')
                    break
                else:
                    speaking('請從公車、捷運、腳踏車中選擇一項')
        except KeyboardInterrupt:
            pass
    else:
        logger.info('Main: Asking about neither sightseeing nor transportation.')
        speaking('抱歉，我沒聽清楚喔')
        #speaking('抱歉')



if __name__ == '__main__':
    with open(PJ(this_dir, 'res/init.mp3'), 'rb') as fd:
        simple_player.play_bytes(fd)
    led.set_state(led.BLINK_3)
    time.sleep(1)
    led.set_state(led.OFF)

    try:
        while True:
            button.wait_for_press()
            main()

    except KeyboardInterrupt:
        pass
    
    finally:
        led.set_state(led.OFF)
        led.stop()
