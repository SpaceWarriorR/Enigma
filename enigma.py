# this file contains the main enigma algorithm
from string import ascii_lowercase, ascii_uppercase


# replaces letters in string with corresponding ones in plugboard
def do_plugboard(unconverted, plugs):
    converted = []
    for character in unconverted:
        change = False
        for pair in plugs:
            if character in pair:
                converted.append(pair[(pair.index(character) + 1) % 2])
                change = True
                break
        if not change:
            converted.append(character)
    return ''.join(converted)


# calculates number of clicks before kick
def get_reset(raw_setting, pos):
    clicks = list(ascii_lowercase).index(raw_setting) - list(ascii_uppercase).index(pos)
    if clicks < 1:
        clicks += 26
    return clicks


# function for stepping rotors
def step(rotor, n):
    end_byte = rotor[-1]
    rotor = rotor[:-1]
    rotor = rotor[(n % len(rotor)) * -1:] + rotor[:(n % len(rotor)) * -1]
    for i in range(len(rotor)):
        num = ascii_uppercase.index(rotor[i]) + n
        while num < 0:
            num += 26
        while num > 25:
            num = (num + 1) % 26 - 1
        rotor[i] = ascii_uppercase[num]
    rotor.append(end_byte)
    return rotor


# adjusts the rotor settings to match inputs
def get_rotor_position(raw_rotor, setting, initial_pos):
    offset = list(ascii_uppercase).index(setting) - list(ascii_uppercase).index(initial_pos)
    return step(raw_rotor, offset)


# main encrypting/decrypting function
def enigma(msg, rotors, poss, rings, reflector, plugboard):
    # plugboard encoding
    msg = do_plugboard(msg, plugboard)

    # machine set up
    resets = []
    for i in range(len(rotors)):
        resets.append(get_reset(rotors[i][-1], poss[i]))
        rotors[i] = get_rotor_position(rotors[i], rings[i], poss[i])

    # main encrypting loop
    encrypted = []
    for char in msg:
        # stepping sequence
        double = False
        if resets[1] == 1:
            rotors[1] = step(rotors[1], -1)
            resets[1] = 26
            rotors[0] = step(rotors[0], -1)
            resets[0] -= 1
            double = True
        rotors[2] = step(rotors[2], -1)
        resets[2] -= 1
        if resets[2] == 0:
            resets[2] = 26
            if not double:
                rotors[1] = step(rotors[1], -1)
                resets[1] -= 1

        # encrypting (equivalent to passing signal through rotors)
        char = rotors[2][ascii_uppercase.index(char)]
        char = rotors[1][ascii_uppercase.index(char)]
        char = rotors[0][ascii_uppercase.index(char)]
        char = reflector[ascii_uppercase.index(char)]
        char = ascii_uppercase[rotors[0].index(char)]
        char = ascii_uppercase[rotors[1].index(char)]
        char = ascii_uppercase[rotors[2].index(char)]
        char = do_plugboard(char, plugboard)
        encrypted.append(char)

    # formatting encrypted result and returning it
    encrypted = ''.join(encrypted)
    encrypted = ' '.join([encrypted[i:i + 5] for i in range(0, len(encrypted), 5)])
    encrypted = '\n'.join([encrypted[i:i + 29] for i in range(0, len(encrypted), 30)])
    return encrypted
