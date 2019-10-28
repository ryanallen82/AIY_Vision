import time
from aiy.leds import Leds, Color, Pattern


with Leds() as leds:
    for _ in range(4):
        leds.update(Leds.privacy_on())
        leds.update(Leds.rgb_on(Color.GREEN))
        time.sleep(1)
        leds.update(Leds.rgb_off())
        time.sleep(1)
        leds.update(Leds.rgb_on(Color.GREEN))
        time.sleep(1)
        leds.update(Leds.rgb_off())
        time.sleep(1)
        leds.update(Leds.privacy_off())

with Leds() as leds:
    leds.pattern = Pattern.blink(500)
    leds.update(Leds.rgb_pattern(Color.GREEN))
    time.sleep(5)
