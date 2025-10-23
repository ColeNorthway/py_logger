import threading
import time

test = 0

class FileOperations:
    lock = threading.Lock()

    @staticmethod
    def append_file():
        print("thread1 entered append")
        with FileOperations.lock:
            with open("test.txt", "a") as f:
                for x in range(0, 4):
                    print("in the loop with thread 1")
                    time.sleep(1)
                    f.write("gangshit")
            test = 1

    @staticmethod
    def overwrite_file():
        print("thread 2 waiting on thread 1")
        with FileOperations.lock:
            print("thread 2 got in")
            with open("test.txt", "w") as f:
                for x in range(0, 4):
                    f.write("gangy")


class Thread1Class:
    @classmethod
    def appending(cls):
        FileOperations.append_file()

class Thread2Class:
    @classmethod
    def re_writing(cls):
        print("before accessing the overwrite file")
        FileOperations.overwrite_file()


def main():
    f = open("test.txt", "x")
    f.close()


    t1 = threading.Thread(target=Thread1Class.appending, args=())
    t2 = threading.Thread(target=Thread2Class.re_writing, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()

'''
what do we want to see from this program to know we hit success

1) The program will be saying in a loop
    > Then the program will say that thread 2 is waiting on thread 1 in the middle of the loop
'''
