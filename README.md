OrgTime
=======
# Install & setup
Copy or link file orgtime.py to your $PATH and put following code in your .emacs file
> (add-to-list 'load-path  "/path/to/OrgTime")
> (require 'orgtime)
> (setq png_path "/path/to/store/the/generated/piechart/") ; optional, will use ~/.emacs.d by default