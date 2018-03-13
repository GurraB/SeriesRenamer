Guide


1. put .py file in folder with tv series

2. Start it and enter the tv series name (which needs to be the same as the folder name)

3. Add any seasons you want to exclude

4. Watch it rename all the files

5. Check the error log if anything went wrong.




File structure required



.

|--Series 1

|   |--Season 1

|       |--S01E01.mp4

|       |--S01E02.mp4

|       |--S01EXX.mp4

|   |--Season 2

|       |--S02E01.mp4

|       |--S02E02.mp4

|       |--S02EXX.mp4

|   |--Season x

|       |--S0XE01.mp4

|       |--S0XE02.mp4

|       |--S0XEXX.mp4

|--Series 2

|   |--Season 1

|       |--S01E01.mp4

|       |--S01E02.mp4

|       |--S01EXX.mp4

|--renamer.py



File names can be anything initially but require SXXEXX somewhere in the name.
For example 'Some_random_series_S01E02_and_some_random_name.mp4' is fine.
The Series name needs to be the actual series name (since it webscrapes IMDB).