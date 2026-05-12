from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# This will not open the Wikipedia Page, but a search where you can then find it.
# Münster is add in front of every name, since some district names like Dom, Martini, Bahnhof are not specific enough
# We implemented a match name statement so it only gets added to unspecific district names, but it wasn't saved 💀
url = QUrl("https://de.wikipedia.org/w/index.php?search=Münster+[%Name%]")
webview = QWebView()

webview.load(url)
webview.show()