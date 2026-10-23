# Makefile push changes out to github 

default:
	git add --all
	git commit -m "Remote update"
	git push -u origin main

local:
	git add --all
	git commit -m "Local update"	
