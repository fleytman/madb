from readchar import readkey, key



while True:
    k = readkey()
    if k == key.CTRL_C:
        raise KeyboardInterrupt()
    elif k == key.ENTER:
        print("Enter")

    print(k.encode())
