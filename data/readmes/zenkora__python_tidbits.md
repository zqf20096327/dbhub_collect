## Python Tidbits
This repository contains any Python scripts I write to make my life easier.

### Requirements
- Python 3 (completely untested on 2)

If you are running Windows and want to call these tools from a shell, you will
not only need to place them in your `%PATH%`, but also ensure that the `.py`
file extension is in `%PATHEXT%` and associated with a working Python 3
interpreter. Python's installer should do this for you.

Unix users can make these tools callable from a shell through aliases, or by
marking them as executable with `chmod +x $script` and adding them to `$PATH`.
Preferably, just rename your cloned copy of the repo to a hidden folder and add
it to your `$PATH` through your shell's rc file. Please don't drop them in
`/usr/bin`. You know who does that? People who enjoy kicking puppies.

### Usage
Every script has a help message with detailed instructions, just call it with
`[python] $script.py help`. In addition, most have a non-positional `verbose`
argument.

Note that scripts prefixed with `_mod_` are local modules (which you are free
to steal) and if a `__main__` section exists, it's purely for testing.

### License
As a lot of this code could be considered to be trivial, I can't justify
copyrighting and applying a restrictive license (like the GNU GPL) to them. So
they're in the public domain. If your jurisdiction doesn't recognize the public
domain, you can consider this entire repo to be licensed under the WTFPL
(included below).

```
        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
