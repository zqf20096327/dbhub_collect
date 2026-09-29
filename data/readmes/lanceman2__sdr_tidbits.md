# sdr_tidbits

Odds and ends, tid bits of code that may be used for Software Defined
Radio (SDR).

Just some demo programs we can run.  We don't explain so much.

Some parts of this package may get tagged (git) and pulled into other
projects/packages using the github web API.  It's a very modular and
distributed way of developing and sharing code without the nasty
side-effects that come about from code replication.  And as everybody
knows, code replication is not a problem if code is stable.  Maybe I need
to look into one of those web distributed software build systems, or
better yet use Nix builds.

This code is being developed on GNU/Linux systems like Ubuntu 20.04.


## Dependencies (auto depend)

We try to make dependencies be self evident for programming experts; like
for example if there is a make warning that says can't find library "foo"
so not making "bar", than if you need bar, than you need foo; otherwise
move on without using bar without error, and just ignore that 'make'
warning.


Dependencies:

  # for compiling tests/iio-monitor
  apt install libcdk5-dev




Stuff in this directory depend on GNUradio and grrun being installed,
and lots of other packages/software.


FILES:


  rxDisplay_demo.bash:

    A simple test to display random I/Q data via GNUradio where the data
    comes from a file pipe standard input. See comments in
    8bitsToEachFloat.c.

  8bitsToEachFloat.c:

    Source to program 8bitsToEachFloat that can be used to turn random
    bits to 8 bit resolution random floats.


To build, run in shell:

  make


Example run in bash shell (will run make for you):

  ./rxDisplay_demo.bash



Source code references (URLs) to "our" files that are (or may be) shared
with other projects:

  Note: There may be lots of other files that these files grab.  How deep
  does the rabbit hole go?  One hopes we resolved to hash to a unique file
  (somehow) as it gets deeper into levels of referring files.  Most
  students are too stupid to even think about such things, which leads
  to bit rot of software.

  Files from https://github.com/lanceman2/small_utils

  We need to nail down the git hash of the version of these scripts that
  we will define what we used to make stuff in this project at release
  time:

    How we installed GNUradio:
    - https://raw.githubusercontent.com/lanceman2/small_utils/master/070_installScripts/gnuradio

    We also installed files from the directory 020_root_installs/ and 050_bin/ in
    - https://raw.githubusercontent.com/lanceman2/small_utils
      TODO: pick a git hash to nail down the source files.

    - https://raw.githubusercontent.com/lanceman2/small_utils/master/070_installScripts/airspyhf
      Replace master with hash d0dc466f9709d929f25bd4013330b938d1891958
      (at the time of this writing: currently master is the same)

    - https://raw.githubusercontent.com/lanceman2/small_utils/master/070_installScripts/libiio

    - https://github.com/lanceman2/quickstream/





Informational references used to work on this project:


  Tx Rx SDR hardware plutoSDR:

    Some C code that reads plutoSDR?
    https://ez.analog.com/dsp/f/q-a/538805/pluto-sdr---rx-tx-c-example

    At the time of writing these notes getting this dam hardware device to
    work was a hell shit storm; hence so many references.  The Analog
    Devices company seem to be using a "newer" Linux Kerneql driver system
    that includes a new kernel driver IIO (not too new but seems to
    require modprode to load on Ubuntu), and a new middle-ware library API
    called libiio.  This IIO stuff seems to be a good idea in principle,
    we'll see how practice goes. 

    libiio and Linux kernel iio driver are two different things, but it
    appears that libiio depends on the Linux kernel iio driver.

    Looks like libiio is bringing on the pain.  Trying to do too much and
    failing.  Looks like libiio makes all IIO like devices look the same,
    even virtual devices that are served from the Internet.

    https://wiki.analog.com/university/tools/pluto

    file:///media/lance/PlutoSDR/info.html -- auto mounted when you plug in
    the plotoSDR USB hardware device

    https://wiki.analog.com/university/tools/pluto/drivers/linux

    https://plutosdr.org/linux-drivers/

    https://www.thegeekdiary.com/understanding-the-sysfs-file-system-in-linux/

    http://analogdevicesinc.github.io/libiio/

    https://wiki.analog.com/resources/tools-software/linux-software/libiio_internals

    https://www.kernel.org/doc/html/v4.14/driver-api/iio/index.html

    https://programmer.group/iio-subsystem-of-linux-device-driver-iio-framework-and-iio-data-structure.html

    https://www.cyberciti.biz/faq/add-remove-list-linux-kernel-modules/


  Rx SDR hardware AirSpy:

    Worked like a charm.  The kernel driver where common, already loaded.
    Just depended on libudev and libusb.  We installed airspyhf
    library/toolkit from latest github tagged source.  See Source code
    references above for URLs and details.  The AirSpy hardware device
    just used the old common middle-ware libusb with libudev, with a
    airspyhf middle-ware toolkit/library API wrapper.



