# [---IMPORT LIBRARIES---]
import re, csv, sys

# [---CAPTURE OPENING ARGUMENT---]
if len(sys.argv) > 1:
    data_file = sys.argv[1]
else:
    data_file = ''

# [---CLASS DEFINITION---]
class re_builder():

    # initialize class
    def __init__(self, data_file):
        # public variables
        default_data_file = 'data.txt'
        if data_file == '' : data_file = default_data_file
        self.data_file = data_file   
        self.word_list_file = 'words_01.txt' # deprecated
        self.results = ""                       
        self.log_file = 'regrex_log'  
        self.img_file = 'regrex_img.txt'       
        self.select_exit = 1 
        self.select_cat = 2
        self.select_custom_1 = 3
        self.select_custom_2 = 4
        self.default_start = 5
        self.presets_loaded = 0                 

        # private variables
        self.__re = ""
        self.__data = ""
        self.__application_name = 'RegRex'
        self.__default_error = '\nExiting ' + self.__application_name 
        self.__words = []
        self.__presets_file = 'regrex_defaults.csv'
        self.__presets = []

    # load data from file
    def load_data(self):
        try:
            self.__data = open(self.data_file, 'r').read()
            # print(self.__data) # debug line
        except:
            print("There was a problem loading the file",self.__default_error)

    # cat the file in memory
    def show_data(self):
        print(self.__data)

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
            with open(self.__presets_file) as f:
                reader = csv.reader(f, delimiter=',', quotechar='"')
                n = self.default_start
                for row in reader:
                    temp = {'opt':n,'title':row[0],'re':row[1]}
                    self.__presets.append(temp)
                    n += 1
                print(self.__presets) # debug line
            self.presets_loaded = len(self.__presets)
        except:
            print("There was a problem loading the default presets file",self.__default_error)

    # load a preset regular expression
    def load_re_preset(self, n):
        n -= self.default_start
        self.__re = self.__presets[n]['re']
        # print(self.__re) # debug line

    # load a custom regular expression
    def load_re(self, my_re):
        self.__re = my_re
        print(self.__re) # debug line

    # print main menu
    def make_menu(self):
        print('   File in memory =',self.data_file)
        print('  ',self.select_exit,'  Exit')
        print('  ',self.select_cat,'  Cat file in memory')
        print('  ',self.select_custom_1,'  Custom Regular Expression')
        print('  ',self.select_custom_2,'  Custom Regular Expression (case sensitive)')
        for row in self.__presets:
            print('  ',row['opt'],' ',row['title'])

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
    def process_re(self, print_results = 'n', case_sensitive = 'n'):
        print('Preparing regular expression.')
        if case_sensitive.lower() == 'y':
            r = re.compile(self.__re)
        else:
            r = re.compile(self.__re, re.I)

        self.results = r.findall(self.__data)
        # print(self.results) # debug line

        # to print results in terminal
        if print_results.lower() == 'y':
            for item in my_re.results:
                print(item)
        result_total = len(my_re.results) 
        print(result_total,'results returned.')
        if result_total > 0:
            wipe = str(input('Wipe results from file? (Yn) ENTER = no: '))
        log = str(input('Log results? (Yn) ENTER = yes: '))
        if log:
            f = open(self.log_file, 'w')
            f.write('Logged ' + str(result_total) + ' results.')
            
    # print active regular expression
    def retrieve_re(self):
        return self.__re

# [----PROGRAM BODY----]
# instantiate class
my_re = re_builder(data_file)

# load data from file
my_re.load_data()

# load regex presets
my_re.load_presets()

# set how many times program can loop
loop_maker = 'loop twenty times!!!'    # program will loop as many times as there are chars

# launch interactive terminal with image and build display
print(open(my_re.img_file, 'r').read())
my_re.make_menu()

# get user input
while loop_maker:
    #try:
    n = int(input('\nPlease type an option from the menu above and strike ENTER: '))
    if n >= my_re.default_start and n <= my_re.default_start + my_re.presets_loaded:
        my_re.load_re_preset(n)
        my_re.process_re('y', 'y')
        my_re.make_menu()
    elif n == my_re.select_exit:
        loop_maker = ''
    elif n == my_re.select_cat:
        print('\n[BEGINNING OF FILE]')
        my_re.show_data()
        print('[END OF FILE]\n')
        my_re.make_menu()
    elif n == my_re.select_custom_1:
        temp = str(input('Enter regular expression: '))
        my_re.load_re(temp)
        my_re.process_re('y', 'y')
        my_re.make_menu()
    elif n == my_re.select_custom_2:
        temp = str(input('Enter regular expression: '))
        my_re.load_re(temp)
        my_re.process_re('y', 'y')
        my_re.make_menu()
    else:
        print('Your selection is not in the menu.')
#    except:
       # print('Invalid key entered!')


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
