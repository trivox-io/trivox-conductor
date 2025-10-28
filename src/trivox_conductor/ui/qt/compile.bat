pyside6-rcc.exe resource.qrc -o ../resource_rc.py

pyside6-uic.exe source/main_window.ui -o compiled/main_window.py --from-imports
