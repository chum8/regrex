# [---IMPORT LIBRARIES---]
import re

# [---CLASS DEFINITION---]
class re_builder():

    # initialize class
    def __init__(self):
        # public variables
        # self.data_file = 'data.txt'
        self.data_file = 'universities.txt'     # default file to read data
        self.word_list_file = 'words_01.txt'    # default file of words to turn into a regex
        self.results = ""                       # store the results
        self.records_loaded = 0                 # track the number of presets available
        self.write_file = 'regrex_results.txt'  # default file to write the results
        self.img_file = 'regrex_img.txt'       

        # private variables
        self.__re = ""
        self.__data = ""
        self.__application_name = 'RegRex'
        self.__default_error = '\nExiting ' + self.__application_name 
        self.__words = []
        self.__presets_file = 'regrex_defaults.txt'
        self.__presets = []

    # load data from file
    def load_data(self):
        try:
            self.__data = open(self.data_file, 'r').read()
            # print(self.__data) # debug line
        except:
            print("There was a problem loading the file",self.__default_error)

    # load word list from file
    def load_word_list(self):
        try:
            self.__words = open(self.word_list_file, 'r').read().split()
            # print(self.words) # debug line
        except:
            print("There was a problem loading the word list file",self.default_error)

    # load regex presets from file
    def load_presets(self):
        try:
            temp = open(self.__presets_file, 'r').read().split()
            # print(temp) # debug line
            for line in temp:
                self.__presets.append(line)
            self.records_loaded = len(self.__presets)
        except:
            print("There was a problem loading the default presets file",self.default_error)

    # load a prebuilt regular expression
    def load_re(self, my_re):
        self.__re = my_re

    # build regular expression
    def build_word_search_re(self, case_sensitive = 'y'):
        left_, right_  = '(', ')'
        temp = left_
        try:
            first = True
            for w in self.__words:
                if not first:
                    temp += '|' + str(w)
                else:
                    temp += str(w)
                    first = False
            temp += right_
            self.__re = temp

        except:
            print("There was a problem building the regular expression",self.default_error)

    # get results of regular expression
    def process_re(self, case_sens = 'n'):
        if case_sens.lower() == 'y':
            r = re.compile(self.__re)
        else:
            r = re.compile(self.__re, re.I)

        # print(type(r)) # debug line
        self.results = r.findall(self.__data)
        # print(self.results) # debug line

    # print active regular expression
    def retrieve_re(self):
        return self.__re

# [----PROGRAM BODY----]
# instantiate class
my_re = re_builder()

# load data from file
my_re.load_data()

# load regex presets
my_re.load_presets()

# default numbers
select_custom = 5     # menu option to do a custom regex
select_exit = 6       # menu option to exit

# set how many times program can loop
loop_maker = 'iloop'    # program will loop as many times as there are characters in this string

# interactive terminal
print(open(my_re.img_file, 'r').read()) # bring up the welcome screen
while loop_maker:
    try:
        s = int(input('Please type an option from the menu above and strike ENTER: '))
        if s >= 1 and s <= my_re.records_loaded:
            print('You selected option',s)
        elif s == select_custom:
            print("Custom selected")
            #my_re.dosometing()
        elif s == select_exit:
            loop_maker = ''
        else:
            print('Not a menu selection!')
    except:
        print('Invalid selection!')
    
    if loop_maker:
        loop_maker = loop_maker[1:]
    else:
        exit()

print('Maximum run-throughs reached, please launch RegRex again to keep regexxing!')

#print('Welcome to The Forgotten Five Regex Lab.')
#print('Regular expression now in memory is \'' + my_re.retrieve_re() + '\'')
#if input('Run this regular expression against \'' + my_re.data_file + '\'? (Yn) ').lower() == 'y':
#    my_re.process_re()
#
#    # to print results in terminal
#    for item in my_re.results:
#        print(item)
#
#    # to write to file
#    with open(my_re.write_file, 'w') as f:
#        for item in my_re.results:
#            # to write stripping paranthese
#            f.write(item.translate({ord(c): None for c in '()'}))
#
#            # to write as is
#            # f.write(item)
#
#            # add new line
## [----END OF PROGRAM----]
#
# [----DEPRECATED OPTIONS----]
# move into program body if desired to re-implement
# for regular expressions based on a preloaded regular expression
# my_re.load_re(domain_re1)

# for regular expressions based on a word list
# my_re.load_word_list()
# my_re.build_word_search_re()


           #f.write('\n')
