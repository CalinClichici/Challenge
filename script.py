import pandas as pd
import os

# Load CSV file into a DataFrame
with open(os.path.join("dataset" , "joined_dataset_final.csv")) as file:
    data = pd.read_csv(file, delimiter=",")

# Set filter columns
filterCols = ['NAME1', 'WRBTR', 'BUKRS', 'BLDAT', 'XBLNR']

# Set DataFrame to only use the filter columns
# and initialize empty DataFrame. The empty DataFrame
# used for storing the duplicates
data = pd.DataFrame(data, columns = filterCols)
df = pd.DataFrame(columns = filterCols)

"""
Initialize empty dictionary
Dictionary will be formated as follows:
    {key : [#dup, [list1], [list2], list[3]]}
            
            key -> first word from the name of each row
            
            #dup -> number of possible copies found
            
            [list1] -> list of tuples containing
                            - row index of the possible duplicate found
                            - row index of the original string
                            
            [list2] -> list of row indices of first occurence of a name
            
            [list3] -> list containng the first occurence of a name
"""
dictionary = {}

# Iterate through the csv file once to compile a dicitonary
# containing all unique names found in 'NAME1' column of DataFrame
# Fill dictionary
for index, row in data.iterrows():
    
    # Take the entire name from current row
    name = row["NAME1"]
    
    # take the first word of the name
    name_begin = name.split(' ', 1)[0]
    
    # If 'name_begin' not in name_dict, then add key 'name_begin' to  
    # 'name_dict' and 'name_full' to this key
    if name_begin not in dictionary:   
        # Add new key to ledger
        
        dictionary.update({name_begin : [0,[],[index], [name]]})
        
    elif name in dictionary[name_begin][3]:
        # If 'name' is already in 'dictionary', then treat it as
        # a possible duplicate and add it to [list1]
        rowOriginal = dictionary[name_begin][2][dictionary[name_begin][3].index(name)]
        dictionary[name_begin][1].append((index, rowOriginal))
        
        # Count the possible duplicates so far
        dictionary[name_begin][0] = len(dictionary[name_begin][1])
        
    else:
        # If the first word of the name is a key in the dictionary
        # but the entire name is not in found at that key, then
        # add the name to [list3] and its row index to [list2]
        dictionary[name_begin][3].append(name)
        dictionary[name_begin][2].append(index)

# Filter entries in dictionary to categorize duplicates
for i in dictionary:
    
    # Get number of possible duplicates counted for key i
    dup_count = dictionary[i][0]
    
    # Get the row indices of the  names which are non-duplicate
    rows = dictionary[i][2]
    
    # If the possible duplicate count for the current row is greater than 0,
    # then check for exact duplicate
    if dup_count > 0:
        
        # Get the list of duplicates
        listDup = dictionary[i][1]
        
        # Iterate through the tuple list
        for i in range(dup_count):
            
            # Get current tuple
            a = listDup[i]
            
            # Check potentian duplicate with original row
            if ((data['BUKRS'][a[0]] == data['BUKRS'][a[1]])
                &(data['BLDAT'][a[0]] == data['BLDAT'][a[1]])
                &(data['WRBTR'][a[0]] == data['WRBTR'][a[1]])
                &(data['XBLNR'][a[0]] == data['XBLNR'][a[1]])):
                
                # Add both rows to 'df'. First add original row,
                # then add the duplicate
                df = df.append(['Master vendor data error'])
                df = df.append(data.iloc[a[1]])                
                df = df.append(data.iloc[a[0]])
                df = df.append([''])
    
    # If a key contains multiple names which are not duplicates,
    # then check for possible subsidiary duplicate.
    if len(rows) > 1:
        
        # Group the rows by the 'BUKRS' column
        grouped = data.iloc[rows].groupby('BUKRS')
        
        # For each group check if the other columns match as well
        for name, group in grouped:
            
            # Checking for duplicates in ['WRBTR', 'BLDAT', 'XBLNR'] columns
            # and setting the group to the duplicates found
            group = group[group.duplicated(['WRBTR', 'BLDAT', 'XBLNR'], keep = False)]
            
            # If duplicates are found, then the number of elements will be > 1
            if len(group) > 1: 
                
                # Add duplicates found in groups to 'df'
                df = df.append(['Multiple subsidiaries'])
                df = df.append(group)
                df = df.append([''])

# Save the DataFrame 'df' as a csvs
df.to_csv('results.csv')