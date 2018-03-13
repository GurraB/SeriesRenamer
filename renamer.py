import glob, os, re, requests, shutil
from bs4 import BeautifulSoup

error_report = []
exclusion = []

#get the names of the episodes from imdb by webscraping
def get_episode_name(imdb_id, season):
    names = []
    page = requests.get("http://www.imdb.com/title/" + imdb_id + "/episodes?season=" + season) #get the page for an entire season of the tv series
    soup = BeautifulSoup(page.content, 'html.parser')
    for episode in soup.find_all('div', class_='info'): #get all divs of class info
        obj = re.search(r'title=".*">', str(episode.find('strong'))) #find the strong attribute of the div
        if obj: #if it exists
            name = obj.group()
            name = name[7:len(name) - 2] #should look at the contents of <a> tag instead. Currently it finds the "title="aaaaa" attribute of the <a> tag but not all series has that attribute
            if r':' in name or r'/' in name or r'*' in name or r'?' in name: #not allowed in a file name in windows
                error_report.append("Invalid name, S" + season + "E" + str(len(names) + 1) + ":" + name + "\t Fixed automatically") #add to the error report that the problem was fixed
                name = name.replace(r':', r',')
                name = name.replace(r'/', r' ')
                name = name.replace(r'*', r'---')
                name = name.replace(r'?', r'')
            names.append(name) #add the found name to the list of names
    return names

#rename a series
def rename(series, imdb_id):
    for directory in os.listdir(series): # directory contains all the items in the series folder
        if os.path.isdir(os.path.join(os.getcwd() + '\\' + series , directory)): #check if it is a directory
            try:
                seasonNumber = str(int(directory[len(directory) - 2:len(directory)]))
                print(seasonNumber)
                if str(int(seasonNumber)) in exclusion: #if this was in the excluded seasons, skip it
                    continue
            except: #if we could not extract a season number from the directory name, skip it. Useful for example if there are a "Movies" folder such as in the Futurama series.
                continue
            names = get_episode_name(imdb_id, seasonNumber)
            epCounter = 0 
            for ep in os.listdir(os.path.join(os.getcwd() + '\\' + series , directory)): #for every file in the season folder
                name = os.path.join(os.getcwd() + '\\' + series + '\\' + directory, ep) #get the name of the current file
                
                obj = re.search(r'S\d\dE\d\dE\d\d', name, re.I) #find the double episode number such as S01E18E19
                if obj:
                    try:
                        print(obj.group())
                        print("old path: " + name)
                        print("new path: " + os.path.join(os.getcwd() + '\\' + series + '\\' + directory, series + r' ' + obj.group() + r' ' + names[epCounter] + os.path.splitext(name)[1]))
                        print()
                        os.rename(name, os.path.join(os.getcwd() + '\\' + series + '\\' + directory, series + r' ' + obj.group() + r' ' + names[epCounter] + os.path.splitext(name)[1])) #rename the file 'Series S01E18E19 episode name.file_extension'
                    except:
                        error_report.append("S" + seasonNumber + "E" + str(epCounter + 1) + ": Error renaming") #add to the error report if anything went wrong.
                    epCounter += 2 #append the episode counter by two since it was a double episode
                    continue

                obj = re.search(r'S\d\dE\d\d', name, re.I) #find the episode number such as S01E01
                if obj:
                    try:
                        print(obj.group())
                        print("old path: " + name)
                        print("new path: " + os.path.join(os.getcwd() + '\\' + series + '\\' + directory, series + r' ' + obj.group() + r' ' + names[epCounter] + os.path.splitext(name)[1]))
                        print()
                        os.rename(name, os.path.join(os.getcwd() + '\\' + series + '\\' + directory, series + r' ' + obj.group() + r' ' + names[epCounter] + os.path.splitext(name)[1]))#rename the file 'Series S01E01 episode name.file_extension'
                    except:
                        error_report.append("S" + seasonNumber + "E" + str(epCounter + 1) + ": Error renaming")
                    epCounter += 1
            if not epCounter == len(names): #if the number of named files is not the same number of episodes found on imdb something might have gone wrong. Report it.
                error_report.append("Error in season " + seasonNumber)

#Get the imdb id for the tv series by doing a search on imdb.com
def get_imdb_id(name):
    name = name.replace(r' ', '+') #replace spaces with '+'
    page = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + name +"&s=all") #get the page
    soup = BeautifulSoup(page.content, 'html.parser') #format the page using beautifulsoup
    series = soup.find('td', class_='result_text') #find the first <td> of class result_text
    obj = re.search(r'title/.*/', str(series)) #narrow down the text in the element
    return obj.group()[6:15] #take the imdb id out

series_name = input("Series name:\n")
excluded_seasons = input("Add season exclusions (ex. 1,2,3,4,5...)\n")
exclusion.extend(excluded_seasons)
imdb_id = get_imdb_id(series_name)
rename(series_name, imdb_id)

error_log = open('renamer_error_log.txt', 'w') #create an error log
for error in error_report:
    error_log.write(error + "\n") #report all the errors into the .txt file
error_log.close()
