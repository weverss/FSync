FSync
=====

Sublime Text 3 plugin for file synchronization between workspaces

How to install
==============


With github repository and Package Control
-------------

With **Package Control**, add repository below (Preferences > Package Control > Add Repository) and install **FSync** package normally.

<pre>
https://github.com/weverss/FSync
</pre>

*If you don't have Package Controll installed, see [this link](https://sublime.wbond.net/installation) to install it.*


With a hosted ZIP
--------------

Copy the code below and paste into Sublime console to install the plugin:
<pre>
import urllib.request,os; pf = 'FSync.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://wevers.com.br/FSync.zip' ).read(); open(os.path.join( ipp, pf), 'wb' ).write(by)
</pre>
