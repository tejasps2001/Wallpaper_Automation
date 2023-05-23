# Testing progress_bar.

import time

# Hide cursor bar.
print('\033[?25l', end="")
for i in range(1, 11):
    # \r to go back to beginning of the line.
    # \033[K to clear the text from the current position to the EOL.
    print('\r\033[K', end='')
    print('Progress', end='')
    for i in range(3):
        print('.', end='', flush=True)
        time.sleep(1)
print()
# Show the cursor again.
print('\033[?025h', end='')

print("Done!")
