from random import randint

words = [
    "cat",
    "dog",
    "house",
    "tree",
    "book",
    "chair",
    "apple",
    "banana",
    "orange",
    "table",
    "window",
    "flower",
    "school",
    "pencil",
    "river",
    "mountain",
    "garden",
    "summer",
    "winter",
    "bottle",
    "ladder",
    "pocket",
    "thunder",
    "diamond",
    "blanket",
    "turtle",
    "rocket",
    "shadow",
    "lantern",
    "mailbox",
    "chicken",
    "mirror",
    "curtain",
    "dolphin",
    "bicycle",
    "popcorn",
    "sandwich",
    "pancake",
    "balloon",
    "rainbow",
    "treasure",
    "suitcase",
    "octopus",
    "tractor",
    "castle",
    "monster",
    "whisper",
    "coconut",
    "elephant",
    "penguin",
    "lighthouse"
]

times = 0
full_word = []
guessed_word = []


def char_input():
    print("Please enter a letter")
    char = input("\t > ")
    global times
    times += 1
    return char

def get_hangman(tup):
    if len(tup) <= 0:
        rand = randint(0, 50)
        return words[rand]
    rand = randint(0, (len(tup)-1))
    return tup[rand]

def hangman(*args):
    word = get_hangman(args)
    print("MADE BY JACK GRANT : YO THIS YunNig GRIEZZY, HI")
    print("Type 'exit' to quit")
    looped_times = 0
    full_word = list(word.lower())
    guessed_word = list("_" * len(full_word))
    user_char = ""
    while guessed_word != full_word:
        global times
        repeated = False
        prev_word = ''
        looped_times = 0
        repeat_times = times
        # If a cheeky yn types "<><>" it will tell u the full word
        if user_char == 'answer':
            times -= 1
            print(" ".join(full_word))
        if user_char == 'guesses':
            times -= 1
            print(times)
        # If u type this yn : ">" it will exit the code
        if user_char.lower() == 'exit':
            exit()
        if user_char not in full_word:
            if len(user_char) > 1:
                repeat_times = 0
                if user_char != 'answer' and user_char != 'guesses':
                    print("Must be a single letter!!")
                if user_char.isdigit():
                    print("Word will only be a letter!!")
            if repeat_times >= 1:
                print("Wrong, Try again!")
            user_char = char_input()
            if user_char == '>':
                exit()
            #if user_char == '<><>':
                #print(" ".join(full_word))
        else:
            for i in full_word:
                looped_times += 1
                repeat_times += 1
                if i == user_char:
                    prev_word = guessed_word[looped_times-1]
                    guessed_word[looped_times-1] = user_char
                    if prev_word == user_char:
                        repeated = True
            if repeated == True:
                print("Already guessed this")
                times -= 1
            else:  
                print("".join(guessed_word))
        if guessed_word == full_word:
            break
        if looped_times > 1:
            user_char = char_input()
        
    print(f'''

     ------------------------------------
    | 🎉 Correct, it took you {times} tries{'!' if times < 10 else ''}🎉 |
     ------------------------------------

    ''')