#!/bin/sh
echo "installing mongodb"
brew install mongodb
echo "done installing mongodb"
echo "installing virtualenv"
pip install virtualenv
echo "done installing virtualenv"
echo "installing the scraper"
virtualenv google-taxonomy-scraper
echo "done installing the scraper"
echo "switch dir"
cd google-taxonomy-scraper
echo "done switch dir"
echo "cloning repo in current folder"
git clone git@github.com:duasamericas/google-taxonomy-scraper 
echo "done cloning repo in current folder"
echo "activating virtual environment"
source ./bin/activate 
echo "done activating virtual environment"
echo "installing scrapy"
pip install scrapy 
echo "done installing scrapy"
