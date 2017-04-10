import threading
import time

clock_is_work = True

def clock(interval):
    while clock_is_work:
        print('The time is ' + str(time.localtime()) + ' s')
        time.sleep(interval)


if __name__ == '__main__':
    print('Threading...')

    thread_1 = threading.Thread(target=clock, args=(1,))
    thread_1.daemon = True
    thread_1.start()


    # time.sleep(20)

    # thread_1.join(3)
    print(threading.active_count())

    time.sleep(20)

    clock_is_work = False

    time.sleep(1)

    print(threading.active_count())


