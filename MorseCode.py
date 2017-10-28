RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 24
BUZZER_PIN = 25

import pigpio
import time
import sys
import asyncore
import thread

# the length of a dot is 1 unit
# a dash is 3 units
# spacing between parts of the same letter is 1 unit
# spacing between letters is 3 units
# spacing between words is 7 units

timeUnit = 0.1
morseCode = {
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----'
}

def blinkLetter(letter, pi):
    morse = morseCode[letter]
    sys.stdout.write(letter)
    sys.stdout.flush()
    for char in morse:
        if char == '.':
            pi.set_PWM_dutycycle(RED_PIN, 255)
            pi.set_PWM_dutycycle(GREEN_PIN, 255)
            pi.set_PWM_dutycycle(BLUE_PIN, 255)
            pi.write(BUZZER_PIN, 1)
            time.sleep(timeUnit)
        elif char == '-':
            pi.set_PWM_dutycycle(RED_PIN, 255)
            pi.set_PWM_dutycycle(GREEN_PIN, 255)
            pi.set_PWM_dutycycle(BLUE_PIN, 255)
            pi.write(BUZZER_PIN, 1)
            time.sleep(timeUnit * 3)
        pi.set_PWM_dutycycle(RED_PIN, 0)
        pi.set_PWM_dutycycle(GREEN_PIN, 0)
        pi.set_PWM_dutycycle(BLUE_PIN, 0)
        pi.write(BUZZER_PIN, 0)
        time.sleep(timeUnit)

def blinkWord(word, pi, firstWord):
    if firstWord:
        firstWord = False
    else:
        sys.stdout.write(' ')
        sys.stdout.flush()
    for letter in word:
        blinkLetter(letter, pi)
        time.sleep(timeUnit * 2)

def blinkSentence(sentence, pi):
    firstWord = True
    words = sentence.lower().split()
    for word in words:
        blinkWord(word, pi, firstWord)
        firstWord = False
        time.sleep(timeUnit * 4)
    sys.stdout.write('\n')
    sys.stdout.flush()

pi = pigpio.pi()

message = str(raw_input("Enter a message: "))
blinkSentence(message, pi)