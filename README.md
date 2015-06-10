# neulandeuphonie
An censoring proxy that replaces bad words with good words and all images with images of cats (everybody loves cats).

## Installing
To install it is recommended to create a python2 virtualenv (env/ is already in .gitignore) and activate it. You have to install the virtualenv tool. Most distributions have it in packages named ```python-virtualenv``` or similar. 

    virtualenv --python python2 env # create virtualenv
    source env/bin/activate

After that you can install the dependencies from the requirements.txt via

    pip install -r requirements.txt

If you use python3 you have to do

    pip install --pre -r requirements.txt
    
because configparser only has a python3 compatible beta.

## Running it
To run neulandeuphonie you simply start the proxy.py executing
    
    python proxy.py

It will start a proxy on *:8080 which you can set in your browser.