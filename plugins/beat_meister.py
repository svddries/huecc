import threading
import time
import phue

class BeatMeister:

    def __init__(self, bridge):
        self.light_name = 'Sfeerlamp Zithoek'
        # light_name = "Hanglamp Eetkamer"

        self.bridge = bridge
        self.cycle_time = 0
        self.thread = None

    def _run(self):
        t_start = time.time()

        self.stopped = False

        # hue range : 0 - 65535
        beat_hues = [ 0, 10000, 20000, 40000 ]

        while not self.stopped:

            if self.cycle_time == 0:
                time.sleep(0.1)
            else:   
                beat = int((time.time() - t_start) / self.cycle_time) % 4    

                self.bridge.set_light(light_id=self.light_name, parameter={
                    "bri" : 254,
                    "sat" : 254,
                    "hue" : beat_hues[beat] 
                }, transitiontime=0)

                # Sleep until next beat
                t_elapsed = time.time() - t_start
                n = int(t_elapsed / self.cycle_time)
                t_new = (n + 1) * self.cycle_time

                sleep_time = t_new - t_elapsed
                time.sleep(sleep_time)

    def start(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.start()        

    def stop(self):
        self.stopped = True
        self.thread.join()

    def set_data(self, data):
        bpm = data["bpm"]
        print "BeatMeister: setting bpm to {0}".format(bpm)
        self.cycle_time = 60.0 / bpm

    def disable(self):
        self.cycle_time = 0