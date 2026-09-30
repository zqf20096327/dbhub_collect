Dreambox BSP layer for dm800se only under https://github.com/OpenPLi/openpli-oe-core.

Run in your oe directory:
```
git submodule add https://github.com/ims21/dm800se.git
```
In oe directory add into "Makefile" dm800se BSP layer:
```
	$(CURDIR)/meta-openpli \
	$(CURDIR)/meta-dream \
+	$(CURDIR)/dm800se \
	$(CURDIR)/meta-vuplus \
```
Remove the "/meta-dream/classes/image_types_nfi.bbclass" (it doesn't support "jffs2nfi" images).

Build image - in oe directory run:
```
MACHINE=dm800se make image
```

Build in oe directory feed:
```
cd build
source env.source
MACHINE=dm800se bitbake openpli-enigma2-feed
```
You can rebuild then indexes (not needed usually):
```
MACHINE=dm800se bitbake package-index
```


update dm800 ... in dm800se run:
```
git pull origin master
```


If you want in future remove this dm800se BSP layer, use in oe directory this 3 steps:
```
# Remove the submodule entry from .git/config

git submodule deinit -f dm800se

# Remove the submodule directory from the superproject's .git/modules directory

rm -rf .git/modules/dm800se

# Remove the entry in .gitmodules and remove the submodule directory located at path/to/submodule

git rm -f dm800se
```
