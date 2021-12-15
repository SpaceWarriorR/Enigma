# this file contains the main file processing functions


# general file processing
def get_dat(file):
    with open(file) as f:
        return f.read().split('\n')


# function returning plugboard settings from file
def get_plugs(file):
    with open(file)as f:
        return f.read()


# function writing plugboard settings to file
def set_plugs(txt, file):
    with open('plugboard.enigma', 'w') as f:
        f.write(txt)


# getting plugboard settings
def get_plug_data(file):
    with open(file) as f:
        return f.read().split(' ')


# getting the rotors
def get_rotors(file):
    # getting all rotors from files
    data = get_dat(file)
    func_rotors = []
    func_rotor_names = []
    for line in data:
        func_rotor_names.append(line[:line.index(':')].strip('rotor'))
        temp_rotor = line[:-4][line.index(':') + 1:].split(',')
        temp_rotor.append(line[-2].lower())
        func_rotors.append(temp_rotor)
    # rotors returned [names, rotor values]
    return [func_rotor_names, func_rotors]


# getting reflectors
def get_reflectors(file):
    # getting all reflectors from file
    data = get_dat(file)
    func_reflector_names = []
    func_reflectors = []
    for line in data:
        func_reflector_names.append(line[:line.index(':')].strip('reflector'))
        func_reflectors.append(line[line.index(':') + 1:].split(','))
    # reflectors are returned [names, reflector values]
    return [func_reflector_names, func_reflectors]
