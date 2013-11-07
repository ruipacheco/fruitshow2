fruitshow
=========

This is a web forum written in Python that aims to be a cross between [Fruit Show](http://sourceforge.net/projects/fruitshow/) and [Vanilla](http://vanillaforums.org/).

It supports anonymous posting like Fruit Show, but also registered users like Vanilla with registration being done by invite only. Posts created by registered users are only viewed by 
other registered users.

Installation for Development
------------
1. sudo apt-get install install libncurses5-dev
2. Install [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito)
3. Create a workspace and activate it
4. Checkout the project from github
5. `pip install -r requirements.txt`
6. Install the database from the sql file
7. Edit `config.py` 
8. `python fruitshow.py`
