# TikTok Comment Gatherer
Written and maintained by [@Olliemyers4](https://github.com/Olliemyers4)

Tested Python Version - Python 3.11.6

Scripts are designed for usage in Windows


## Requirements


### Chromedriver:

Chrome and the associated version of the chrome webdriver.

Assuming you have the latest version of chrome, the corresponding webdriver can be acquired at the link below:


**Please Note:** The `chromedriver` link that corresponds to your operating system should be copied and pasted into the browser to download the zip folder that contains the file `chromedriver.exe`


[Chrome Web Driver](https://googlechromelabs.github.io/chrome-for-testing/#stable)

This chromedriver file needs to be placed inside of the folder containing the code.

### Python:

This code has been tested on python version 3.11.6 put should work with versions 3.8.0 +

To install the required libraries for this code please run this from the folder:

```sh
pip install -r requirements.txt
```

Or run the file `installPythonReq.bat` if on Windows

### Config:

This project contains a file: `config.json`

This file contains the path to where chrome data is stored. Typically this is:

```
C:\\Users\\<YOUR-USERNAME>\\AppData\\Local\\Google\\Chrome\\User Data\\
```

This file needs to be opened and the `<YOUR-USERNAME>` needs replacing with the username of your computer.

The final step that needs to be undertaken is to open chrome and log into [TikTok](https://www.tiktok.com) 


## Running

On Windows, just double clicking and running `runTikTok.bat` will run the program.

Debug information will be provided on screen, and the program will eventually prompt for a hashtag.

From here, Chrome will visit different webpages. Please don't touch it during this time. When the program is done, Chrome and the window that opened initially will close and a `comments.txt` will have been created. This file contains all the found comments.