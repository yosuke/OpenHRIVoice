rmdir /S /Q dist
rmdir /S /Q build
\Python26\python.exe setup.py py2exe
copy openhrivoice\*.xsd dist
copy "\Program Files (x86)\Graphviz 2.28\bin\*.dll" dist
del dist\Qt*.dll
copy "\Program Files (x86)\Graphviz 2.28\bin\dot.exe" dist
copy \Python26\Lib\site-packages\gtk-2.0\runtime\bin\*.dll dist
robocopy /S \Python26\Lib\site-packages\gtk-2.0\runtime\share dist\share
robocopy /S \Python26\Lib\site-packages\gtk-2.0\runtime\etc dist\etc
cd dist
dot -c
cd ..
rmdir /S /Q dist\share\doc
rmdir /S /Q dist\share\gtk-doc
rmdir /S /Q dist\share\man

