# created 2022.Jan.11 12.55PM  Los Angeles by Teodor Ciobanu

# Imports
from datetime import datetime
import os
import csv
from tkinter import filedialog
import tkinter

# open file dialog
root = tkinter.Tk()
root.withdraw()
# root.iconbitmap(default='transparent.ico')
filePath=filedialog.askopenfilename(defaultextension='.csv',filetypes=[("CSV",".csv")]) 

# read CSV file to list
file_dir, file_name = os.path.split(filePath)
with open(filePath, newline='') as csv_file:
	reader = csv.reader(csv_file)
	contentList = list(reader)

# Making changes
newContentList = contentList

###  * rename column header 'nps' to 'nps_score'
header = newContentList[0]
for i in range(len(header)): # range(len(newContentList[0])):
	if header[i] == 'nps':
		newContentList[0][i] = 'nps_score'

### * add a column 'arrival_city-state' 
# which contains the arrival city and arrival state separated by a dash, e.g. “Chicago-Illinois”
newContentList[0].append('arrival_city-state') 
for row in newContentList[1:]:
	arrivalCity_state = row[24].strip() + '-' + row[26].strip()
	row.append(arrivalCity_state)
	
###  * add a column 'score_numeric' 
# which contains a number (1-5) based off the score column from 'Very Bad' -> 1 to 'Very Good' -> 5
newContentList[0].append('score_numeric') 
scoreIndex = {'Very Bad':'1', 'Bad':'2', 'Alright':'3', 'Good':'4', 'Very Good':'5'}
for row in newContentList[1:]:
	scoreNumeric = scoreIndex[row[2].strip()]
	row.append(scoreNumeric)

###  * Remove all rows which have a departure state of 'United Kingdom'
for row in newContentList[1:]:
	if row[25].strip() == 'United Kingdom':
		newContentList.remove(row)
	
### * Ensure columns are ordered as follow:
        # ['unique_id', 'airline_name', 'date', 'score', 'title', 'location', 'review',
        # 'flight_type', 'flight_class', 'flight', 'seat_comfort',
        # 'customer_service', 'cleanliness', 'food_beverages', 'legroom',
        # 'check_in', 'entertainment', 'nps_score', 'csat', 'nps_duplicate',
        # 'ticket_price', 'question', 'sensitive', 'departure_city', 'departure_state',
        # 'arrival_city', 'arrival_state', 'arrival_city-state', 'score_numeric']
ColumnOrder = ['unique_id', 'airline_name', 'date', 'score', 'title', 'location', 'review',
        'flight_type', 'flight_class', 'flight', 'seat_comfort',
        'customer_service', 'cleanliness', 'food_beverages', 'legroom',
        'check_in', 'entertainment', 'nps_score', 'csat', 'nps_duplicate',
        'ticket_price', 'question', 'sensitive', 'departure_city', 'departure_state',
        'arrival_city', 'arrival_state', 'arrival_city-state', 'score_numeric']
newOrder = []
for i in ColumnOrder:
	newOrder.append(header.index(i))
reorderedContent = []
for row in newContentList:
	newRow = []
	for i in newOrder:
		newRow.append(row[i])
	reorderedContent.append(newRow)

""" 
# for numbering new files
dirContent = os.listdir(file_dir)
dirCsvFiles = [i[-5:-4] for i in dirContent if file_name.lower() in i.lower() and file_name.lower() != i.lower()]
n = 1
while n in dirCsvFiles or n == 1000:
	n += 1
newFileName = file_name[:-4] + str(n) + '.csv'
"""

# for date time in new name file
now = datetime.now().strftime("%Y%m%d%H%M%S")
newFileName = file_name[:-4] +'_' + str(now) + '.csv'

# New File Path for save as
newFilePath = file_dir + '/' + newFileName

# Save as new file
with open(newFilePath, 'w', newline = '') as newFile:
	write = csv.writer(newFile)
	write.writerows(reorderedContent)

# Message Dialog
tkinter.messagebox.showinfo(title = "Success", message = "Corrections completed\nNew file:\n{0}\nSaved in:\n{1}".format(newFileName, file_dir))



