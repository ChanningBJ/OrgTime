(provide 'orgtime)
(setq org_py_exe "orgtime.py")
(setq orgtime_path (file-name-directory load-file-name))
(add-to-list 'exec-path  orgtime_path)
(defun org-time-summary ()
  "Take a screenshot into a unique-named file in the current buffer file
  directory and insert a link to this file."
  (interactive)

  (setq msg (shell-command-to-string (concat org_py_exe " " buffer-file-name " " orgtime_path)))

  (setq summary_content_begin "#+BEGIN: clocktable")
  (setq summary_content_end "#+END:")
  (beginning-of-buffer)
  (search-forward summary_content_begin nil t 1)
  (beginning-of-line)
  (setq begin_pos (point))
  (search-forward summary_content_end nil t 1)
  (end-of-line)
  (setq end_pos (point))
  (delete-region begin_pos end_pos)
  (insert (concat summary_content_begin " " (format-time-string "%Y-%m-%d %H-%M-%S\n")))
  (insert msg)
  (insert (concat "\n" summary_content_end))
  (org-display-inline-images)
  )

  
