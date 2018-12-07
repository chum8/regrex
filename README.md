# RegRex
Regular expression tool for command line

## What RegRex does
RegRex loads a file into memory.  From the interactive menu, run various regular expressions against the data in the file.

## RegRex includes two files for you to use:
```bash
  data.txt
  universities.txt
```
You may use any text file with RegRex.

## Using the RegRexU URL helper
  RegRexU scrapes a website and passes the contents into RegRex.
  To run RegRexU with a prompt for the website
  ```bash
    py regrexu.py
  ```
  To run RegRexU in Fast Track mode, pass the name of the website
  ```bash
    py regrexu.py <http://somewebsite.com>
  ```
    
## Installing
```bash
git clone https://github.com/chum8/regrex.git
```
## Running
Note: you can change the file in memory from the interactive terminal.
To run RegRex with the default file (currently set to data.txt)
```bash
  py regrex.py
```
To run RegRex with a different file
```bash
  py.regrex.py <file>
```
## Available commands
   1    Exit
   2    Cat file in memory
   3    Change file in memory
   4    Toggle case sensitivity
   5    Custom regular expression
   6    Domain name finder
   7    URL finder
   8    Email address finder
   9    Phone number finder
   10   SSN finder

## Logging and masking
  After hunting for regular expressions, the program gives you the option of
    Logging the results to a file
    Saving the results with a mask character to replace the original data
      i.e. a social security number 999-99-5555 could be masked as XXX-XX-XXXX
