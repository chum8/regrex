# [----IMPORT LIBRARIES----]
import requests

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
def filename_maker(my_url):
    my_url = my_url.replace('://','_')
    my_url = my_url.replace('//','_')
    my_url = my_url.replace('/','_')
    my_url = my_url.replace('.','_')
    return 'urllog/log_' + my_url

# [----PROGRAM BODY----]
#defaults
my_url = 'http://www.example.com'
my_exit_message = '\nExiting RegRex URL Helper.'

# load opening image
print(open('regrexu_img.txt', 'r').read())

# get url contents
my_url = input('URL contents will be scraped. Enter a URL to try: ')
my_txt = retrieve(my_url)
print("Successfully loaded", my_url)

# write url contents to a file
my_file = filename_maker(my_url)
file_write(my_txt, my_file, my_exit_message)
print("Successfully wrote contents of", my_url, "to", my_file)

# see if user wants to view contents
if input("Would you like to echo the text of " + my_url + " to your terminal window before passing the contents to RegRex? (Yn) ").lower() == 'y':
    print("\nBody of", my_url)
    print("[BEGIN RECORD]")
    print(my_txt)
    print("[RECORD END]")

# pass contents into regrex.py for further processing

# exit
print(my_exit_message)
exit()
# [----END OF PROGRAM----]

