import pathlib
import sys
import re
import pickle


# Person object with input fields: Last name, first name, middle initial, id, phone number
# Has a basic display function to print out the contents of Person
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee id: " + self.id + "\n\t" + self.first + " " + self.mi + " " + self.last + "\n\t" + self.phone)


# Regex method for ID
# Checks if id is two letters followed by 4 digits
# Will continue checking the user's new id until it fits the format
def formatID(inputID):
    match = re.search("[a-zA-Z][a-zA-Z][0-9][0-9][0-9][0-9]", inputID)
    while match is None:
        inputID = input(inputID + " is invalid ID"
                                  "\nID must be two letters followed by four digits"
                                  "\nPlease enter a valid ID: ")
        match = re.search("[a-zA-Z][a-zA-Z][0-9][0-9][0-9][0-9]", inputID)
    return inputID


# Regex method for phone number
# Checks if id is of the format "XXX-XXX-XXXX"
# Will continue checking the user's new phone number until it fits the format
def formatPhoneNumber(inputPhoneNumber):
    match = re.search("[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", inputPhoneNumber)
    while match is None:
        inputPhoneNumber = input(inputPhoneNumber + " is invalid phone number"
                                                    "\nEnter phone number in form 123-456-7890"
                                                    "\nPlease enter a valid phone number: ")
        match = re.search("[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", inputPhoneNumber)
    return inputPhoneNumber


# Method that processes data.csv
def processFile(filePath):
    # Dictionary of Persons which will be returned at the end of the method
    personDictionary = {}

    # reads through the various lines of the file
    file = open(pathlib.Path.cwd().joinpath(filePath), 'r')

    for line in file.readlines()[1:]:
        # Saving the fields from each line
        fields = line.split(",")

        # Making sure that each ID is unique and that there are no duplicates
        id = formatID(fields[3])
        while id in personDictionary:
            print("ERROR: " + id + " IS A DUPLICATE ID")
            id = formatID(input("PLEASE ENTER A DIFFERENT ID: "))

        lastName = fields[0].strip().capitalize()
        firstName = fields[1].strip().capitalize()
        middleInitial = fields[2].strip().capitalize() if len(fields[2]) > 0 else "X"
        phoneNumber = formatPhoneNumber(fields[4].strip())

        # Create Person object corresponding to each line and save it into a dictionary with key being ID
        personDictionary[id] = Person(lastName, firstName, middleInitial, id, phoneNumber)
    file.close()
    return personDictionary


# Main method
if __name__ == '__main__':
    # Making sure the user enters a file name as a sysarg
    if len(sys.argv) < 2:
        fp = input('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        # Creating, writing, and then reading from a pickle file that saves the dictionary of Person objects
        pickle.dump(processFile(fp), open('personDictionary.p', 'wb'))
        personDictionary = pickle.load(open('personDictionary.p', 'rb'))
        [person.display() for person in personDictionary.values()]
