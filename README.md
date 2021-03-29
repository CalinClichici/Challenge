# Challenge

The code should be run from any enivronment which runs Python3 code and has the required libraries. The code provided was made using Spyder4 from Anaconda.

Find duplicates in .csv file

To find the duplicates in the .csv file a dictionary was used.

After the file is read into the script an empty dictionary is being initialized. Then a FOR loop is used to iterrate through the file using iterrows().
While the script does iterate through the entire .csv file, it does so only once in orde to compile the dictionary.

The format os the dictionary is as follows:
  { key : [ #_of_possible_duplicates, [ list1 ], [ list2 ], [ list 3] ]}
  
    key ->  The first word of each name which is not already in the dictionary is used as a key. Any further occurences of the key in other names flags the name
            as a possible duplicate. This technically also takes care of duplciates due to a type. Although in some cases it will not recognize them.
    
    #_of_possible_duplicates -> This value is an integer denoting how many possible duplicates have been found for each key.
    
    [ list1 ] ->  This list contains tuples which show which rows are possible duplicates. In the format of (dup, org), dup reperesents the row index of the possible
                  duplicate and org denotes the row index of the original row, which was found as afirst occurence.
                  
    [ list2 ] ->  This list contains the row indices of the original rows found while compiling the dictionary. An original row is the first occurence of that name while
                  iterating through the DataFrame.
                  
    [ list3 ] ->  This list contains the names of the original rows as strings.
    

After compiling the dictionary, we loop through all the keys and look for duplciates. If the key has a count of possible duplicates greater than 0, this means that there are
possible duplicates to be found at that key, otherwise the key containes only one entry, therefore, no duplcates to be found. Then  take the list of tuples and check the rows
to see if they have matching column values. If yes, then add the row to the empty DataFrame, otherwise move on. That entry is tagged as 'Master Vendor data error' and is an
exact duplicate. Both the original row and the duplicate row are inserted into the DataFrame, the original being the first and the duplicate the second. Afterwards a check is
being made to see if the number of original rows found for the current key is greater than 1. This would mean that there are possible subsidiaries to be found in the list. The
rows corresponding to the key are grouped by the company code 'BUKRS'. If the values in the  following columns, ['WRBTR', 'BLDAT', 'XBLNR'], of any row are equal with the values
of any othre row from the group, this would mean that a subsidiary duplicate has been found. The corresponding rows are then added to the 'df' DataFrame. After all the key go thorugh this process, all the possible duplicates should have been found. The file is then saved as 'results.csv. in the same folder where the script is.
