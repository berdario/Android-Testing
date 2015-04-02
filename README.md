Android-Testing:
===============

# M0blizer:
===============

Moblizer helps you do static analysis of any android application or .apk file. As it is a very premature tool we have included very limited functionality such as information disclosure automation from the source code of the .apk file. And there are certain limitations but still we are useing it in our daily pentesting projects and it helped us saving lots of time and decreases our effort. Hope it will help you also.


Pre-Requisites:
----------------
1. java installed in your system.
2. apktool.jar in your working directory.
3. python 3.4 or greater installed.


How to use Moblizer:
--------------------
1. Go to the directory containing your apktool.jar
2. Run `python3 /path/to/moblizer.py /path/to/your.apk`
3. It will search for files which contains any sensitive keyword such as email, ip, username etc, redirect the output using your shell functionality if you need to store it. It also provides you Manifest permission details at the end of the ouput.
