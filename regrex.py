# [----IMPORT LIBRARIES----]
import re, csv, sys, datetime, getpass, socket

# [----CAPTURE OPENING ARGUMENT----]
if len(sys.argv) > 1:
    data_file = sys.argv[1]
else:
    data_file = ''

# [----CLASS DEFINITION----]
class re_builder():

    # initialize class
    def __init__(self, data_file):
        # public variables
        self.log_file, self.img_file = 'regrex_log', 'regrex_img.txt'       
        self.word_list_file = 'words_01.txt' # deprecated
        default_data_file = 'data.txt'
        if data_file == '' : data_file = default_data_file
        self.data_file = data_file   
        self.results = ""                       
        self.result_total = 0
        self.hidden_option_1 = 0
        self.select_exit = 1 
        self.select_cat = 2
        self.select_change = 3
        self.select_custom_1 = 4
        self.select_custom_2 = 5
        self.default_start = 6
        self.presets_loaded = 0                 
        self.case_sensitive = 'n'

        # private variables
        self.__re, self.__data, self.__log_time  = "", "", ""
        self.__words, self.__presets = [], []
        self.__application_name = 'RegRex'
        self.__default_error = '\nExiting ' + self.__application_name 
        self.__presets_file = 'regrex_presets.csv'
        self.__an = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'

    # change data file
    def change_file(self, data_file):
        if data_file == self.data_file:
            print('The file you specified is already in memory!\n')
        else:
            self.data_file = data_file
            self.load_data()
            print('Successfully changed file in memory to',data_file,'\n')

    # load data from file
    def load_data(self):
        try:
            self.__data = open(self.data_file, 'r').read()
            # print(self.__data) # debug line
        except:
            print('Fatal error! There was a problem loading the file into memory.',self.__default_error)
            exit()

    # cat the file in memory
    def show_data(self):
        try:
            print(self.__data)
        except:
            print('Unable to show data. Do you have a file loaded?')

    # load word list from file (deprecated)
    def load_word_list(self):
        try:
            self.__words = open(self.word_list_file, 'r').read().split()
            # print(self.words) # debug line
        except:
            print('There was a problem loading the word list file',self.default_error)

    # load regex presets from file
    def load_presets(self):
        self.__presets = []
        try:
            with open(self.__presets_file) as f:
                reader = csv.reader(f, delimiter=',', quotechar='"')
                n = self.default_start
                for row in reader:
                    temp = {'opt':n,'title':row[0],'re':row[1]}
                    self.__presets.append(temp)
                    n += 1
                # print(self.__presets) # debug line
            self.presets_loaded = len(self.__presets)
        except:
            print('There was a problem loading the default presets file. A common problem is an improperly formatted presets csv file.  Check',self.__presets_file,'for bad formatting, including extra whitespace at EOF.',self.__default_error)
            exit()

    # load a preset regular expression
    def load_re_preset(self, n):
        try:
            n -= self.default_start
            self.__re = self.__presets[n]['re']
            # print(self.__re) # debug line
        except:
            print('Unable to load regular expression! Bad expression or expression missing.')

    # load a custom regular expression
    def load_re(self, my_re):
        try:
            self.__re = my_re
            # print(self.__re) # debug line
        except:
            print('Unable to load regular expression! Bad expression or expression missing.')

    # print main menu
    def make_menu(self):
        print('   File in memory =',self.data_file)
        print('  ',self.select_exit,'   Exit')
        print('  ',self.select_cat,'   Cat file in memory')
        print('  ',self.select_change,'   Change file in memory')
        print('  ',self.select_custom_1,'   Toggle case sensitivity')
        print('  ',self.select_custom_2,'   Custom regular expression')
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
    def process_re(self, print_results = 'n'):
        print('Preparing regular expression.')
        try:
            if self.case_sensitive.lower() == 'y':
                r = re.compile(self.__re)
            else:
                r = re.compile(self.__re, re.I)
        except:
            print('Bad regular expression.  Unable to process.\n')
            return 0

        self.__log_time = str(datetime.datetime.now()) # note time
        self.results = r.findall(self.__data)
        # print(self.results) # debug line

        if print_results.lower() == 'y': self.print_results()
        if str(input('Log results? (Yn) ENTER = no: ')).lower() == 'y': self.log_results()
        if self.result_total > 0:
            if str(input('Mask alphanumeric characters and write to file? (Yn) ENTER = no: ')).lower() == 'y': self.mask_results()

    # write results to log file
    def log_results(self):
        f = open(self.log_file, 'a')
        f.write('[BEGIN RECORD]\n')
        f.write(self.__log_time+'\n')
        f.write('system user: '+str(getpass.getuser()+'\n'))
        f.write('system host: '+str(socket.gethostname()+'\n'))
        f.write('results: ' + str(self.result_total) + '\nfile: ' + str(self.data_file) + '\nregular expression: ' + self.__re + '\n[BEGIN RESULTS]\n')
        for item in self.results:
            f.write(item+'\n')
        f.write('[RESULTS END]\n[RECORD END]\n')
        print('Results successfully logged to',self.log_file)
        input('Hit ENTER to continue.')
        print('\n')
 
    # replace alphanumeric data in original file with mask character
    def mask_results(self):
        print('Alphanumeric characters will be masked and the original file overwritten.  Type \'quit\' to cancel.')
        mchar = str(input('Please enter a mask character: '))
        if mchar.lower() == 'quit':
            print('Original file unchanged due to user cancel.')
        else:
            # mask characters in results 
            temp_results = []
            mask = mchar[0] * len(self.__an) # prepare mask
            for item in self.results:
                temp = item.maketrans(self.__an, mask)
                temp = item.translate(temp)
                temp_results.append(temp)
                self.__data = self.__data.replace(item, temp)
            self.results = temp_results[:]
            # print(self.results) # debug line
            # print(self.__data) # debug line
            try:
                f = open(self.data_file, 'w')
                f.write(self.__data)
                print('File',self.data_file,'successfully overwritten with new masked data.')
                input('Hit ENTER to continue.')
            except:
                print('Unable to write masked results to file. Original file unchanged.')

    # to print results in terminal
    def print_results(self):
        for item in self.results:
            print(item)
        self.result_total = len(self.results) 
        print(self.result_total,'results returned.')
           
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
    try:
        n = int(input('\nPlease type an option from the menu above and strike ENTER: '))
        if n >= my_re.default_start and n <= my_re.default_start + my_re.presets_loaded:
            my_re.load_re_preset(n)
            my_re.process_re('y')
            my_re.make_menu()
        elif n == my_re.hidden_option_1:
            # hidden option to reload regex_presets.csv
            my_re.load_presets()
            print('Hidden option chosen. Reloaded presets.',my_re.presets_loaded,'presets found.\n')
            my_re.make_menu()
        elif n == my_re.select_exit:
            loop_maker = ''
        elif n == my_re.select_cat:
            print('\n[BEGINNING OF FILE]')
            my_re.show_data()
            print('[END OF FILE]\n')
            my_re.make_menu()
        elif n == my_re.select_change:
            data_file = str(input('Enter name of file to load: '))
            my_re.change_file(data_file)
            my_re.make_menu()
        elif n == my_re.select_custom_1:
            if my_re.case_sensitive == 'y':
                my_re.case_sensitive = 'n'
                print('Case sensitive now OFF')
            else:
                my_re.case_sensitive = 'y'
                print('Case sensitive now ON')
            loop_maker += '.' # no need to waste a turn toggling case sensitivity
        elif n == my_re.select_custom_2:
            temp = str(input('Enter regular expression: '))
            my_re.load_re(temp)
            my_re.process_re('y')
            my_re.make_menu()
        else:
            print('Your selection is not in the menu.')
    except:
        print('Please make a valid selection.')

    if loop_maker:
        loop_maker = loop_maker[1:]
    else:
        exit()

print('This program has a maximum loop value set. That value has been reached and the program is exiting. Please launch RegRex again to keep regexxing!')
# [----END OF PROGRAM----]
# [----DEPRECATED OPTIONS----]
# move into program body if desired to re-implement
# for regular expressions based on a preloaded regular expression
# my_re.load_re(domain_re1)

# for regular expressions based on a word list
# my_re.load_word_list()
# my_re.build_word_search_re()
