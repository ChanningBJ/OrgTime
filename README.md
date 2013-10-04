OrgTime
=======
## Overview
This emacs extension is designed to work with emacs org-mode. It can generate a time usage summary from your org-mode file. Giving a table summary of the working time of current month, current week and today (I will not feel guilty when seeing I already have worked more than 40 hours this week ). Also will give a pie chart of the time spend on each tag.
Here is an example:
![alt tag](https://raw.github.com/Chengming/OrgTime/master/example.png)
## Install & setup
1. Download and extract the source code to your emacs site
1. Copy or link file orgtime.py to your $PATH
1. Put following code in your .emacs file
`` `lisp
(add-to-list 'load-path  "/path/to/OrgTime")
(require 'orgtime)
(setq png_path "/path/to/store/the/generated/piechart/") ; optional, will use ~/.emacs.d by default
` ``
## How to use
When you open a org file, use this command to gnereate the working time summary
```lisp
org-time-summary
```
The summary will be put at the begnning of the org file.