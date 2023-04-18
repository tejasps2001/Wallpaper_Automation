# Testing progress_bar.

import time

print('\033[?25l', end="")
for i in range(1, 11):
    print('\r\033[K', end='')
    print('Progress', end='')
    for i in range(3):
        print('.', end='', flush=True)
        time.sleep(1)
print()

print("Done!")
