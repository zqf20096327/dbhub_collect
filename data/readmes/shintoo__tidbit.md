# tidbit

Desktop notifications that display some summary text from a random Wikipedia page that belongs to any of the categories you are interested in.

## dependencies
* notify2 (install via pip)
* [wikipedia (with category members query, provided by yours truly)](https://github.com/shintoo/Wikipedia) (also install via pip)

Example tidbit:
```
Tidbit: Plants
Plantlet

Plantlets are young or small plants. Many plants such as
spider plants naturally create stolons with plantlets on the
ends as a form of asexual reproduction.
```


```
tidbit - shintoo 2018

tidbit creates a desktop notification displaying the first two sentences from
the summary section of a Wikipedia page belonging to one of the categories
listed in ~/.tidbit_categories

  tidbit			display one tidbit notification
  tidbit add <category>		add <category> to list of categories
  tidbit remove <category>	remove <category> from list of categories
  tidbit list			list all categories
  tidbit background <interval>	display one tidbit notification every
				<interval> seconds
  tidbit fact			do not send any notification, instead print to tty
  tidbit help			print this help
```

The Wikipedia portal on Categories can be found [here](https://en.wikipedia.org/wiki/Portal:Contents/Categories).
