JsonDir =./json/

default: test

test:
	green3 . -vvv

run:
	python3 scraper/post_scraper.py

install:
	pip3 install -r requirements.txt

style:
	pycodestyle scraper/ tests/

cov:
	coverage run -m py.test tests/test.py
	coverage report -m scraper/post_scraper.py
	coverage html scraper/post_scraper.py

full:
	make test
	make cov
	make style

# Call for creating a Json dir and moves all json files there
.PHONY: json
json:
	mkdir -p $(JsonDir)
	mv *.json $(JsonDir); true

# Call for *.json clean up
.PHONY: clean
clean:
	rm -f ./*.json
	rm -f $(JsonDir)*.json


# Call for help with this makefile's commands
.PHONY: help
help:
	@echo "\n\t Makefile of Facebook scrapper from UnB\n"
	@echo " make............= Runs the tests using green3 "
	@echo " make test.......= Also run the tests using green3"
	@echo " make run........= Run post_scrapper.py"
	@echo " make install....= Install the requirements necessary for this project"
	@echo " make style......= Cheks if your code is our pattern of coding for this project"
	@echo " make json.......= Creates a json dir and moves all .json files there"
	@echo " make cov........= Checks how much our program is coverage"
	@echo " make full.......= runs make test, cov and style" 
	@echo " make json.......= Creates a json dir and moves all .json files there"
	@echo " make clean......= Removes all .json files"
	@echo "\n\t End of Makefile Help\n"


