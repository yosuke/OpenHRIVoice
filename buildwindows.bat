rmdir /S /Q dist
rmdir /S /Q build
\Python26\python.exe setup.py py2exe
copy \Python26\Lib\site-packages\gtk-2.0\runtime\bin\*.dll dist
mkdir dist\language-specs
copy \Python26\Lib\site-packages\gtk-2.0\runtime\share\gtksourceview-2.0\language-specs dist\language-specs
mkdir dist\styles
copy \Python26\Lib\site-packages\gtk-2.0\runtime\share\gtksourceview-2.0\styles dist\styles
