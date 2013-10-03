
(setq org_py_exe "/Users/susuxixi/Documents/workspace/OrgTime/pyorg.py")
(setq org_filename "/Users/susuxixi/Documents/workspace/OrgTime/test.org")
(setq png_path "/Users/susuxixi/Documents/workspace/OrgTime/")

(defun org-time-chart ()
  "Take a screenshot into a unique-named file in the current buffer file
  directory and insert a link to this file."
  (interactive)
  ;; (setq filename
  ;;   (concat (make-temp-name
  ;;        (concat  (getenv "HOME") "/.emacs.img/" ) ) ".png"))
  ;; (suspend-frame)
  (setq msg (shell-command-to-string (concat org_py_exe " " org_filename " " png_path)))
  ;; (call-process-shell-command "scrot" nil nil nil nil " -s " (concat
  ;;                               "\"" filename "\"" ))
  (setq summary_content_begin "#+BEGIN: clocktable")
  (setq summary_content_end "#+END:")
  (beginning-of-buffer)
  (search-forward summary_content_begin)
  (beginning-of-line)
  (setq begin_pos (point))
  (search-forward summary_content_end)
  (end-of-line)
  (setq end_pos (point))
  (delete-region begin_pos end_pos)
  (insert (concat summary_content_begin " " (format-time-string "%Y-%m-%d %H-%M-%S\n")))
;  (insert buffer-file-name msg "]]"))
  (insert msg)
  (insert (concat "\n" summary_content_end))
  )
 
;(global-set-key (kbd "C-p") 'my-screenshot)

  
