rm -r dist
rm -r build
\Python26\python.exe setup.py py2exe
copy \Python26\Lib\site-packages\gtk-2.0\runtime\bin\*.dll dist