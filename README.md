# TexasHoldEm_Python
Demo client for Texas Hold 'Em for python

## Getting Started with the Python Demo Client
If you're a seasoned python vet you can probably skip right over this introductory material. All you need to do is download the repository and start hacking! If you're a little less confident, maybe give it a quick a skim, make sure you've got any additional packages downloaded, and then you should be good to go! Finally, if you're a complete novice, fear not! This short guide should provide you with enough information to get up and running with the client!

### Setting up Python
First, you need to install python on your machine. Head over to https://www.python.org/downloads/ and download the latest version of Python 3 for your OS (as of writing, it's Python 3.6.1).

Next we need the python package manager, pip. Check out https://packaging.python.org/tutorials/installing-packages/  for instructions on how install pip. If you downloaded the latest version of python 3 using the link from the previous paragraph, you should already be good to go.

Now we have pip installed  we can install all of the additional packages we require: requests, pillow, json, and tkinter. Staying on the same page the pip link took you to, you can scroll to the section 'Use pip for Installing' (or if you feel exceptionally lazy, follow this link https://packaging.python.org/tutorials/installing-packages/#use-pip-for-installing). This explains how to download packages from PyPI. The requests and pillow packages can be downloaded from here. Note, we need to install the packages for Python 3, so make sure you use the command pip3 if you're on macOS or Linux. We also require the json package. This should be installed by default on all platforms. The last package we require is the tkinter package. This should come with the python install on Windows and macOS. For Linux, you should search for how to install this package for your particular distribution.

### Running the Client
This bit is really easy! Just pass the TexasHoldEmDemoClient.py to the python interpreter! 

### Adding Logic
Coming up with the logic might not be easy, but adding it to your bot sure is! Open up the TexasHoldEm.py file. In there you should see the calculate_move method. This is called by the client every time the server wants you to make a move. Start adding your own code here!

### (Optional) Setting up Your Development Environment
Now we have everything in place, all that is left is to set up our development environment. This really comes down to personal preference, some like to do all their coding in a lightweight text editor, and others like to use a fully featured IDE. We recommend the latter for most users. A great IDE (that is also completely free) is PyCharm from JetBrains. Head over to https://www.jetbrains.com/pycharm/?fromMenu and hit the download button in the top right corner of the page.  On the page this takes you to, select your OS and then download the community version. The IDE is fairly easy to use, but be sure to check out https://www.jetbrains.com/help/pycharm/quick-start-guide.html for some introductory material to get you started.

### Final Remarks
Hopefully now you're in place to get picking through the demo code. This should help you figure out how the API works, and ultimately starting work on your army of intelligent bots! We look forward to seeing what you build! 
