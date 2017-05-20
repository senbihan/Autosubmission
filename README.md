# Autosubmission
This repository is for submitting source file while solving problem in competitive programming websites like codeforces, codechef in both practice and contest mode. I will develop the same for hackerrank, hackerearth etc also.

## Setup
run ```$python setup.py``` for installing the prerequisites 

## Submit to codeforces
1. Open ```codeforces.py``` and add your handle, password, key and secret key generated from your codeforces setting page
2. Run ```$python codeforces.py [p|c|pc] [source_file_complete_path]``` from terminal.
   ```p``` for practice mode
   ```c``` for contest mode
   ```pc``` for past contest mode
  
## Submit to codechef
1. Open ```codechef.py``` and add your handle, password
2. Run ```$python codechef.py [p|c] [source_file_complete_path]``` from terminal.
   ```p``` for practice mode
   ```c``` for contest mode

### Additional Information
1. This project uses ```RoboBrowser``` and ```BeautifulSoup``` for web crawling.
2. Showing verdict from server is sometime delayed. Adjust ```delay``` variable in the source file as required.
3. Codechef does not have any API. The verdict is fetched from the last submission. 
