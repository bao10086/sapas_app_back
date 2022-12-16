import time, threading


def sing():
    for i in range(3):
        print("is singing... %d" % i)
        time.sleep(1)


def dance():
    for i in range(3):
        print("is dancing... %d" % i)
        time.sleep(1)


if __name__ == '__main__':
    print("The main thread starts to execute")

    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)

    t1.start()

    t2.start()


    print("Main thread execution completed")
    a = 3
    b = 4
    print(a+b)
    # exit()