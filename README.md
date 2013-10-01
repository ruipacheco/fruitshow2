fruitshow
=========

This is a web forum written in Python that aims to be a cross between [Fruit Show](http://sourceforge.net/projects/fruitshow/) and [Vanilla](http://vanillaforums.org/).

It supports anonymous posting like Fruit Show, but also registered users like Vanilla with registration being done by invite only. Posts created by registered users are only viewed by 
other registered users.

Installation for Development
------------
1. Install [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito)
2. Create a workspace and activate it
3. Checkout the project from github
4. `pip install -r requirements.txt`
5. Install the database from the sql file
6. Edit `config.py` 
7. `python fruitshow.py`
