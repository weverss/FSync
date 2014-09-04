FSync
=====

Sublime Text 3 plugin for file synchronization between workspaces

How to install
==============
Copy the code below and paste into Sublime console to install the plugin:
<pre>
import urllib.request,os; pf = 'FSync.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://wevers.com.br/FSync.zip' ).read(); open(os.path.join( ipp, pf), 'wb' ).write(by)
</pre>
