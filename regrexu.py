# [----IMPORT LIBRARIES----]
import requests, sys, os
from subprocess import call

# [----CHECK FOR OPENING ARGS----]
if len(sys.argv) == 2:
    # put the system on fast track if we passed in a URl in the CLI
    ftrack = True
    my_url = sys.argv[1]
else:
    ftrack = False
    my_url = 'http://www.example.com'

# [----FUNCTIONS----]
# get contents of a url
def retrieve(my_url):
    r = requests.get(my_url)
    r.raise_for_status()
    return r.text

# write contents to a file
def file_write(my_txt, my_file, my_exit_message):
    try:
        f = open(my_file, "w")
        f.write(my_txt)
    except:
        print("Error thrown while attempting to write to file", my_file, "\nMake sure directory urllog exists!'", my_exit_message)
        exit()

# generate a filename for the write to file
def filename_maker(my_url, my_dir):
    my_url = my_url.replace('://','_')
    my_url = my_url.replace('//','_')
    my_url = my_url.replace('/','_')
    my_url = my_url.replace('.','_')
    return my_dir + '/log_' + my_url

# [----PROGRAM BODY----]
#defaults
my_exit_message = '\nExiting RegRex URL Helper.'
my_dir = 'urllog'

if ftrack:
    print('RegRex URL Helper is running in fast track mode...\nplease wait while',my_url,'is scraped.')

    try:
        # get url contents
        my_txt = retrieve(my_url)
        print("URL retrieved...")

        # write url contents to a file
        my_file = filename_maker(my_url, my_dir)
        file_write(my_txt, my_file, my_exit_message)
        print("File written...")

    except:
        print("There was a problem.  Try using RegRex URL Helper in normal mode or check your URL!")
        exit()

else:
    # load opening image
    print(open('regrexu_img.txt', 'r').read())

    # get url contents
    my_url = input('URL contents will be scraped. Enter a URL to try: ')
    my_txt = retrieve(my_url)
    print("Successfully loaded", my_url)

    # write url contents to a file
    my_file = filename_maker(my_url, my_dir)
    file_write(my_txt, my_file, my_exit_message)
    print("Successfully wrote contents of", my_url, "to", my_file)

    # see if user wants to view contents
    if input("Would you like to echo the text of " + my_url + " to your terminal window before passing the contents to RegRex? (Yn) ").lower() == 'y':
        print("\nBody of", my_url)
        print("[BEGIN RECORD]")
        print(my_txt)
        print("[RECORD END]")

# pass contents into regrex.py for further processing
try:
    call(os.getcwd() + '/py regrex.py ' + os.getcwd() + '/' + my_file)
except:
    print("\nRegRexU successfully scraped", my_url + ".")
    print("The system threw an error while attempting to pass the file into regrex.py.")
    print("Please issue the following command to work with the results of the URL scrape:")
    print("\n\tpy regrex.py "+my_file)
# [----END OF PROGRAM----]

