
from pynput.keyboard import Key, Controller
from pynput import keyboard



def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# in a non-blocking fashion:
# A keyboard listener is a threading.Thread, and all callbacks will be invoked from the thread.
# Call pynput.keyboard.Listener.stop from anywhere, raise StopException or return False from a callback to stop the listener.
# The key parameter passed to callbacks is a pynput.keyboard.Key, for special keys, a pynput.keyboard.KeyCode for normal alphanumeric keys, or just None for unknown keys.
# When using the non-blocking version above, the current thread will continue executing. This might be necessary when integrating with other GUI frameworks that incorporate a main-loop, but when run from a script, this will cause the program to terminate immediately.
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

# or a blocking fashion. 
# Collect events until released. it will continuously listen and the main process will also be stopped here.
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()



''' control keyboard input by program.
keyboard = Controller()
# Press and release space
keyboard.press(Key.space)
keyboard.release(Key.space)

# Type a lower case A; this will work even if no key on the
# physical keyboard is labelled 'A'
keyboard.press('a')
keyboard.release('a')

# Type two upper case As
keyboard.press('A')
keyboard.release('A')
with keyboard.pressed(Key.shift):
    keyboard.press('a')
    keyboard.release('a')

# Type 'Hello World' using the shortcut type method
keyboard.type('Hello World') 
'''
