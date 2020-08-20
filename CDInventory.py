#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# ormerodl, 2020-Aug-18, Update file title
# ormerodl, 2020-Aug-18, Add/Move processing code into DataProcesser class
# ormerodl, 2020-Aug-18, Add write_file capability
# ormerodl, 2020-Aug-18, Add/Move I/O functions from presentation into IO class
# ormerodl, 2020-Aug-19, Troubleshoot for delete loop running but not deleting
# ormerodl, 2020-Aug-19, Troubleshoot for save loop running but not saving to file
# ormerodl, 2020-Aug-19, Update Docstring and comments
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt' # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def get_dicRow(value1, value2, value3):
        """Function to add row to a list of dictionaries

        Appends data input by a user to the 2D list lstTbl

        Args:
            value1: user input ID
            value2: user input Title
            value3: user input Artist

        Returns:
            None.
        """
        dicRow = {'ID': int(value1), 'Title': value2, 'Artist': value3}
        lstTbl.append(dicRow)


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()
        pass

    @staticmethod
    def write_file(file_name, table):
        """Function to save data from a list of dictionaries to text file

        Writes the data from a 2D table (list of dicts) to a text file identified by file_name
         one dictionary row in table represents one line in the file.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        objFile = open(file_name, 'w')
        for row in lstTbl:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()
        print('CD Inventory has been saved to "CDInventory.txt"\n')

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ''
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================\n')

    @staticmethod
    def user_input():
        """Gets user input for CD Inventory

        Args:
            None.

        Returns:
            strID (string): A numeric string from user input
            strTitle (string): alphanumeric string for CD Title
            StrArtist (string): alphnumeric string for CD Artist

        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist

    @staticmethod
    def del_Row(value4):
        """Function to add row to a list of dictionaries

        Appends data input by a user to the 2D list lstTbl
        
        Args:
            value4 (int): user input ID for deletion
        
        Returns:
            None.
        """
        delInput = int(input('Enter the ID you would like to delete: '))
        for i in range(len(lstTbl)):
            if lstTbl[i]['ID'] == delInput:
                del lstTbl[i]
                break
            print('\nThe CD was removed\n')
        else:
            print('\nCould not find this CD!\n')

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory loaded from file.')
        strYesNo = input('Would you like to continue and load from file? [y/n] ')
        if strYesNo.lower() == 'y':
            print('loading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT loaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        tplID, tplTitle, tplArtist = IO.user_input()
        DataProcessor.get_dicRow(tplID, tplTitle, tplArtist)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        IO.del_Row(lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




