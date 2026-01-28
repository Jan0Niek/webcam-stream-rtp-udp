import threading as th

i = 0


def foo():
    global i
    i = 1
    print(i)


def bar():
    i = 2
    print(i)


t1 = th.Thread(target=foo)
t2 = th.Thread(target=bar)
t1.start()
t1.join()
t2.start()
t2.join()
print(i)
