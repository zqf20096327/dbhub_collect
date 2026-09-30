# 快速测试脚本示例

在根目录下，创建 `test.sql`，在里面写想要执行的指令，然后执行 `test.sh` 即可。

# 手动快速测试

```shell build
cd src/observer/sql/parser && ./gen_parser.sh  # 如果改了 parser
bash build.sh debug --make -j32
```

```shell server
cd miniob
cd build
./bin/observer -f ../etc/observer.ini -s miniob.sock
```


```shell client
cd miniob
cd build
./bin/obclient -s miniob.sock
```

insert into text_table values (4,'VHZN828IPVI72728RW1ILEPWOTJI8JA1Z77Q1Q6LNA2GIV3QZCKKW8C2361TTRFRLVF1EQ4IV6UGBKVQC2LNA75SZEF0T4U8F6DRTJPRSN2DV4E59AA2N6UD7MPM0QNPIPFCWQJ0T7IC71JAIY67I3DGNGK7LY3VOTDH1PR49FT278TRLD3X88UCT2CU4666B6R7X6LP4DRSXMKICNTQKK9EADKCNT...
select * from text_table;
insert into text_table values (5, 'FD2NGON9DMW1KUG8SOADHNWSCYZU1ZXZH8QA03GUI3JOS3GZ9X1KPZTDVF63GP2ZE1TEFBV426E907NY8400MVOG7KRI1WUCO4467S1OMO28Y9UY3PWC2XN02HVOJFIGG349CLJTPXYKN8H762DEH6CPZ1ZT2QDJ69YMNSC7WWEYPSOB8TN5GMBAR4DTTFPCMFS31N69OPX6VHBV2Z0XQP1B7TCBI...
update text_table set info='6G8SSUZN7JFK6143NBY1XXOH1Y96D96SGB0LGRO8GRILCBYFYAT9V7G3YJJ1SSFJVFZKREL6MAMXV45BDBY0D70ZL4AIVYEVLQ1OA6XQ56YOVKKWLX39IQ5L05SUJZZ5ZJH9FMU773XXAD92VTTKIVXCRVRQ3QCZQK10PPUAET6BVRGHAU8TKRHAPARHB01274ICUJSLK76VTDDML8SPBH82TTSUB6U1XHZS...
+ failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007f5349afc017 in std::once_flag::_Prepare_ex...
failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007f5349afc017 in std::once_flag::_Prepare_execution::_Prepare_execution<std::call_once<void (&)()>(std::once_flag&, void (&)())::{lambda()#1}>(void (&)()) () from /usr/lib/libmemtracer.so
#2  0x00007f5349afbeab in void std::call_once<void (&)()>(std::once_flag&, void (&)()) () from /usr/lib/libmemtracer.so
#3  0x00007f5349afbe1a in memtracer::MemTracer::init_hook_funcs() () from /usr/lib/libmemtracer.so
#4  0x00007f5349afb6b6 in malloc () from /usr/lib/libmemtracer.so
#5  0x00007f5349afbc3b in operator new(unsigned long) () from /usr/lib/libmemtracer.so
#6  0x00007f5349989dac in std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::reserve(unsigned long) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#7  0x00007f534997e61f in std::__cxx11::basic_stringbuf<char, std::char_traits<char>, std::allocator<char> >::overflow(int) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#8  0x00007f5349987ea1 in std::basic_streambuf<char, std::char_traits<char> >::xsputn(char const*, long) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#9  0x00007f5349977dc4 in std::basic_ostream<char, std::char_traits<char> >& std::__ostream_insert<char, std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*, long) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#10 0x0000563c6f221783 in std::operator<< <std::char_traits<char> > (__s=0x7f53400ade88 "6G8SSUZN7JFK6143NBY1XXOH1Y96D96SGB0LGRO8GRILCBYFYAT9V7G3YJJ1SSFJVFZKREL6MAMXV45BDBY0D70ZL4AIVYEVLQ1OA6XQ56YOVKKWLX39IQ5L05SUJZZ5ZJH9FMU773XXAD92VTTKIVXCRVRQ3QCZQK10PPUAET6BVRGHAU8TKRHAPARHB01274ICUJSL"..., __out=...) at /usr/include/c++/13/ostream:667
#11 CharType::to_string (this=<optimized out>, val=..., result="") at /home/miniob/miniob_test/players/miniob/src/observer/common/type/char_type.cpp:233
#12 0x0000563c6f19a5bc in Value::to_string[abi:cxx11]() const (this=this@entry=0x7f53400035c8) at /home/miniob/miniob_test/players/miniob/src/observer/common/value.cpp:370
#13 0x0000563c6f1d9f19 in UpdatePhysicalOperator::open (this=0x7f5340001c58, trx=<optimized out>) at /home/miniob/miniob_test/players/miniob/src/observer/sql/operator/update_physical_operator.cpp:136
#14 0x535a564645413837 in ?? ()
exit code:-11
-- below are some requests executed before(partial) --
-- init data
create table text_table(id int, info text);
insert into text_table values (1,'this is a very very long string');
insert into text_table values (2,'this is a very very long string2');
insert into text_table values (3,'this is a very very long string3');
-- delete
delete from text_table where id=1;
select * from text_table;
-- update
UPDATE text_table set info='a tmp data' where id = 2;
select * from text_table;

insert into text_table values (4,'1AUQ8LX8JDOYR4DM68FL2AQ5CX5T561LIBDG9KU7AQXM9EGTDKVDQZ4V4FATIVQBUKSZ0H46R9XU43OMVNBP40P6VOSQF6ULU1ABF17SV0E5R5G9M1XIPWH5LIL2QRAXJB5HNUPCAZQ60YQG1GPYBRC931PFRFHWBJX6FXM1AVOWAYNPTET4VJ33BPD70ZKAD1KSX7K7E44JX5IY6NZ84F5Q5TJ0G8...
select * from text_table;
insert into text_table values (5, 'H5SELDW5AM72ZZZGZGTKKSINELZ32JK2EC8S0GFZJ1F6MW61EEKKJIJ2EZ1S481AKGR16EIPSFSA7K6MNK9450GBJHHCBD21AO02HK1WB1L0P9FFEH4OW4M48SIDO7MSR5FU2ZVBRHWR9IURJOLPFGXP2ZWXDE7HILKOWNLHDTM6UDHGZLT65XVBIIF2D0Y4PAGIKYHM9UC0VV84O4TGEL0AGDCKQ...
update text_table set info='UA4CN9LBG6KKNBWRCEF5GMY3Z5P88Y6IXVUTQ0KNF6JGQBKOTKLJ7AE6BK4KM9RN7IWKMTSJAVBZW8IZJLQ9W6PSW39H612BH72YN0D6G1UBIH7JPAF6K4BIWLZ1IER2K9DGRX3TECT9BPLVSWW9QQ0FG00NV56VUHFFMJ04LVRS6UCZIFR6CKU4DDUQZRURBQSFY8RP1BY0VUMT8XJ0S5E7BWJ4KZNNTRV4...
+ failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007f6102100017 in std::once_flag::_Prepare_ex...
failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007f6102100017 in std::once_flag::_Prepare_execution::_Prepare_execution<std::call_once<void (&)()>(std::once_flag&, void (&)())::{lambda()#1}>(void (&)()) () from /usr/lib/libmemtracer.so
#2  0x00007f61020ffeab in void std::call_once<void (&)()>(std::once_flag&, void (&)()) () from /usr/lib/libmemtracer.so
#3  0x00007f61020ffe1a in memtracer::MemTracer::init_hook_funcs() () from /usr/lib/libmemtracer.so
#4  0x00007f61020ff6b6 in malloc () from /usr/lib/libmemtracer.so
#5  0x00007f61020ffc3b in operator new(unsigned long) () from /usr/lib/libmemtracer.so
#6  0x00007f6101f8ddac in std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::reserve(unsigned long) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#7  0x00007f6101f8261f in std::__cxx11::basic_stringbuf<char, std::char_traits<char>, std::allocator<char> >::overflow(int) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#8  0x00007f6101f8bea1 in std::basic_streambuf<char, std::char_traits<char> >::xsputn(char const*, long) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#9  0x00007f6101f7bdc4 in std::basic_ostream<char, std::char_traits<char> >& std::__ostream_insert<char, std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*, long) () from /lib/x86_64-linux-gnu/libstdc++.so.6
#10 0x00005607a0bd0803 in std::operator<< <std::char_traits<char> > (__s=0x7f60f80ade88 "UA4CN9LBG6KKNBWRCEF5GMY3Z5P88Y6IXVUTQ0KNF6JGQBKOTKLJ7AE6BK4KM9RN7IWKMTSJAVBZW8IZJLQ9W6PSW39H612BH72YN0D6G1UBIH7JPAF6K4BIWLZ1IER2K9DGRX3TECT9BPLVSWW9QQ0FG00NV56VUHFFMJ04LVRS6UCZIFR6CKU4DDUQZRURBQSFY8RP"..., __out=...) at /usr/include/c++/13/ostream:667
#11 CharType::to_string (this=<optimized out>, val=..., result="") at /home/miniob/miniob_test/players/miniob/src/observer/common/type/char_type.cpp:233
#12 0x00005607a0b4963c in Value::to_string[abi:cxx11]() const (this=this@entry=0x7f60f80035c8) at /home/miniob/miniob_test/players/miniob/src/observer/common/value.cpp:370
#13 0x00005607a0b88f99 in UpdatePhysicalOperator::open (this=0x7f60f8001c58, trx=<optimized out>) at /home/miniob/miniob_test/players/miniob/src/observer/sql/operator/update_physical_operator.cpp:136
#14 0x314b384d364b4453 in ?? ()
exit code:-11
-- below are some requests executed before(partial) --
-- init data
create table text_table(id int, info text);
insert into text_table values (1,'this is a very very long string');
insert into text_table values (2,'this is a very very long string2');
insert into text_table values (3,'this is a very very long string3');
-- delete
delete from text_table where id=1;
select * from text_table;
-- update
UPDATE text_table set info='a tmp data' where id = 2;
select * from text_table;

insert into text_table values (4,'K8VJZK3WWEGQNQNSLWVA1NWSYZIO35MF1KRBXQJIOKEX94ZL2OC943A6XZ0LORKYGJVVDWKHWEUCXM2XH3GPY81V28FZYCDENGIAQ5FYY4V0VVUSHYBDW3A4SWMZS2TY6GF4A7IWLXYV9LCFRAMPRR4M1O4DPXR211N8YQYDIHXL9HS4XLUKFJKBZ73355LDGGNHWCFQAQO7GLPAJ88ZDQMT0T7H9E...
select * from text_table;
insert into text_table values (5, '1UDYE7U6UNL19PM6P885MWMNLV6MF7PMB44NXFIX6QDD23U5RXH8UD48KY9ENG9TH9MUX1PNCL9USDOZLM2TIHSCRTMK2N8BAXW9QTK5A6EIPNG276NQUF5ZMLGN408XNYZXCJIXHDJYGNL56PQ7UZ2WZBQ9ZOKLU7Y7E3TZYLAI3KOZ501RC06P4UBJCNNYB2V7PP1L6ZNLJ7DGHC9F65XX6NVIV...
update text_table set info='47FK2RNGWQSTLRVM1WX2A5T64F5Z6N1K4Y94NBUXGOKW93IOPDX3PF8DK5FEVP187277TY8X5D957MWUV8RVIQFBZHRFRK46RBQQ0GUU1NPQKZZ1UKXZ3X4UNQ7S17DGL9NGNSFME9FXQCE8KORIQDKLQ9JISWQUDHB2J7I1RLEF7900YS60QCVLC1787ECYSJNBF6R5E6ZL9SJDGFLWE9XPXNUV43T8YLYX...
+ failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007f6ae0e88017 in std::once_flag::_Prepare_ex...
failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007f6ae0e88017 in std::once_flag::_Prepare_execution::_Prepare_execution<std::call_once<void (&)()>(std::once_flag&, void (&)())::{lambda()#1}>(void (&)()) () from /usr/lib/libmemtracer.so
#2  0x00007f6ae0e87eab in void std::call_once<void (&)()>(std::once_flag&, void (&)()) () from /usr/lib/libmemtracer.so
#3  0x00007f6ae0e87e1a in memtracer::MemTracer::init_hook_funcs() () from /usr/lib/libmemtracer.so
#4  0x00007f6ae0e876b6 in malloc () from /usr/lib/libmemtracer.so
#5  0x00007f6ae0e87c3b in operator new(unsigned long) () from /usr/lib/libmemtracer.so
#6  0x000055c67a4e1519 in std::__new_allocator<char>::allocate (this=<optimized out>, __n=65611) at /usr/include/c++/13/bits/new_allocator.h:151
#7  std::allocator<char>::allocate (__n=65611, this=0x7f6adf3f1ae0) at /usr/include/c++/13/bits/allocator.h:198
#8  std::allocator_traits<std::allocator<char> >::allocate (__n=65611, __a=...) at /usr/include/c++/13/bits/alloc_traits.h:482
#9  std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_S_allocate (__n=65611, __a=...) at /usr/include/c++/13/bits/basic_string.h:126
#10 std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_create (this=0x7f6adf3f1ae0, __old_capacity=0, __capacity=<synthetic pointer>: <optimized out>) at /usr/include/c++/13/bits/basic_string.tcc:159
#11 std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_construct<char const*> (__end=0x7f6ad80bede2 "", __beg=0x7f6ad80aed98 "47FK2RNGWQSTLRVM1WX2A5T64F5Z6N1K4Y94NBUXGOKW93IOPDX3PF8DK5FEVP187277TY8X5D957MWUV8RVIQFBZHRFRK46RBQQ0GUU1NPQKZZ1UKXZ3X4UNQ7S17DGL9NGNSFME9FXQCE8KORIQDKLQ9JISWQUDHB2J7I1RLEF7900YS60QCVLC1787ECYSJNBF6R5"..., this=0x7f6adf3f1ae0) at /usr/include/c++/13/bits/basic_string.tcc:229
#12 std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string<std::allocator<char> > (__a=..., __s=0x7f6ad80aed98 "47FK2RNGWQSTLRVM1WX2A5T64F5Z6N1K4Y94NBUXGOKW93IOPDX3PF8DK5FEVP187277TY8X5D957MWUV8RVIQFBZHRFRK46RBQQ0GUU1NPQKZZ1UKXZ3X4UNQ7S17DGL9NGNSFME9FXQCE8KORIQDKLQ9JISWQUDHB2J7I1RLEF7900YS60QCVLC1787ECYSJNBF6R5"..., this=0x7f6adf3f1ae0) at /usr/include/c++/13/bits/basic_string.h:649
#13 CharType::to_string (this=<optimized out>, val=..., result="") at /home/miniob/miniob_test/players/miniob/src/observer/common/type/char_type.cpp:238
#14 0x000055c67a45a57c in Value::to_string[abi:cxx11]() const (this=this@entry=0x7f6ad80035c8) at /home/miniob/miniob_test/players/miniob/src/observer/common/value.cpp:370
exit code:-11
-- below are some requests executed before(partial) --
-- init data
create table text_table(id int, info text);
insert into text_table values (1,'this is a very very long string');
insert into text_table values (2,'this is a very very long string2');
insert into text_table values (3,'this is a very very long string3');
-- delete
delete from text_table where id=1;
select * from text_table;
-- update
UPDATE text_table set info='a tmp data' where id = 2;
select * from text_table;

insert into text_table values (4,'08FJTA2V4T28O0NGPWZYA9P4L8AB1YAYA5U1TGW58TGPH1RAU1GCZ63R3V1N4OI8HOBTW91TVJSOZGS1DDCJ7LD436XGXE135Z4A5TQ5ULE3VQF701PW00EI8SA3JUV88YPCO6CRE1EM38TEQVZA29Y0M3A6FVKXTLQSNRDRFV407B7FYEISU7XXGXWJA49HW49HATP3MJLLK3JDVOOV8R0JN87BN0...
select * from text_table;
insert into text_table values (5, 'IXQZ13LKSP2HE7URWPHGWGLXEH9FDHXHBIXZWR8FWYBLBLPIMX88FP2J77WA5MDZPDQ50WPETW13CVSBHA7FL2O1VDBUME7UD0IGM9MZM9LOVKAQWL5UEFGAJHF3R7SERDHXF2TZ7MZF82TNPT0GPLIUHDILAW4WX14M71N9NZTPPCPLJ6B531TOH3PK04HLNINT84183X1BUPXY337DEF2Q8CNOO...
update text_table set info='4NKPWYHLHMDBOR0Y2X8Z75J84HYIBQC4HL367NXAFP77MT7ESHQ12GEMHX6ZD4865VR6LDWZH8LK6PMNOZYORPOIJ2BXZGHYZSGXFRVZJ5U36HHDQW98ROJVWW2K5MWN2XDM3K2D5ZB00JZR4JHXO4IYPVTGRWDT5M2NR8J4BXM89D7WO7ZISZLJZ3PSQ4F5KLVHO3EU0OOMMU5KI5PE3J7URPVQAU5LOLM9...
+ failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007fee7d46c017 in std::once_flag::_Prepare_ex...
failed to receive response from observer. reason=Failed to receive from server. poll return POLLHUP=16 or POLLERR=str(event & select.POLLERR)
#0  __tls_get_addr () at ../sysdeps/x86_64/tls_get_addr.S:33
#1  0x00007fee7d46c017 in std::once_flag::_Prepare_execution::_Prepare_execution<std::call_once<void (&)()>(std::once_flag&, void (&)())::{lambda()#1}>(void (&)()) () from /usr/lib/libmemtracer.so
#2  0x00007fee7d46beab in void std::call_once<void (&)()>(std::once_flag&, void (&)()) () from /usr/lib/libmemtracer.so
#3  0x00007fee7d46be1a in memtracer::MemTracer::init_hook_funcs() () from /usr/lib/libmemtracer.so
#4  0x00007fee7d46b839 in free () from /usr/lib/libmemtracer.so
#5  0x0000562e4f66cca4 in Record::~Record (this=0x7fee74001658, __in_chrg=<optimized out>) at /home/miniob/miniob_test/players/miniob/src/observer/storage/record/record.h:107
#6  Record::~Record (this=0x7fee74001658, __in_chrg=<optimized out>) at /home/miniob/miniob_test/players/miniob/src/observer/storage/record/record.h:104
#7  std::destroy_at<Record> (__location=0x7fee74001658) at /usr/include/c++/13/bits/stl_construct.h:88
#8  std::_Destroy<Record> (__pointer=0x7fee74001658) at /usr/include/c++/13/bits/stl_construct.h:149
#9  std::_Destroy_aux<false>::__destroy<Record*> (__last=0x7fee74001670, __first=0x7fee74001658) at /usr/include/c++/13/bits/stl_construct.h:163
#10 std::_Destroy<Record*> (__last=0x7fee74001670, __first=<optimized out>) at /usr/include/c++/13/bits/stl_construct.h:196
#11 std::_Destroy<Record*, Record> (__last=0x7fee74001670, __first=<optimized out>) at /usr/include/c++/13/bits/alloc_traits.h:948
#12 std::vector<Record, std::allocator<Record> >::~vector (this=0x7fee7b9d6180, __in_chrg=<optimized out>) at /usr/include/c++/13/bits/stl_vector.h:735
#13 UpdatePhysicalOperator::open (this=<optimized out>, trx=<optimized out>) at /home/miniob/miniob_test/players/miniob/src/observer/sql/operator/update_physical_operator.cpp:194
#14 0x5a50514438513152 in ?? ()
exit code:-11
-- below are some requests executed before(partial) --
-- init data
create table text_table(id int, info text);
insert into text_table values (1,'this is a very very long string');
insert into text_table values (2,'this is a very very long string2');
insert into text_table values (3,'this is a very very long string3');
-- delete
delete from text_table where id=1;
select * from text_table;
-- update
UPDATE text_table set info='a tmp data' where id = 2;
select * from text_table;

CREATE TABLE TAB_VEC(ID INT, A INT, B VECTOR(10));
INSERT INTO TAB_VEC VALUES(1, 1, STRING_TO_VECTOR('[2.04,2.68,0.86,1.72,0.71,1.22,4.8,0.27,3.86,4.5]'));
INSERT INTO TAB_VEC VALUES(2, 2, STRING_TO_VECTOR('[1.63,3.1,3.21,1.62,0.24,4.53,2.91,1.17,4.56,0.4]'));
INSERT INTO TAB_VEC VALUES(3, 3, STRING_TO_VECTOR('[0.72,4.1,0.32,2.17,3.48,2.5,3.69,3.28,1.26,2.42]'));
INSERT INTO TAB_VEC VALUES(4, 4, STRING_TO_VECTOR('[2.55,0.52,1.46,2.43,3.81,3.09,4.33,1.53,0.27,2.55]'));


create table t_order_by_1(id int);
create table t_order_by_2(id int, score float, name char(4));
insert into t_order_by_1 VALUES (5);
insert into t_order_by_1 VALUES (7);
insert into t_order_by_1 VALUES (6);


insert into t_update_mvcc_2 values (2, 'xiaoming', 95.0);
insert into t_update_mvcc_2 values (4, 'zhanghua', 88.5);
insert into t_update_mvcc_2 values (7, 'xiaoyang', 91.0);
insert into t_update_mvcc_2 values (10, 'wangming', 92.0);

create table t_update_mvcc(id int, age int, name char(4));
create unique index t_update_mvcc_id_index on t_update_mvcc(id);
insert into t_update_mvcc values(1, 1, 'a');
insert into t_update_mvcc values(2, 2, 'a');
insert into t_update_mvcc values(3, 3, 'a');
insert into t_update_mvcc values(4, 4, 'a');
insert into t_update_mvcc values(5, 5, 'a');
select * from t_update_mvcc
update t_update_mvcc set name = 'b' where id = 1;

create table t_update_mvcc_2 (id int, name char(8), score float);
create unique index t_update_mvcc_2_id_index on t_update_mvcc_2 (id);
-- concurrency insert data
insert into t_update_mvcc_2 values (1, 'xiaohong', 90.0);
insert into t_update_mvcc_2 values (2, 'xiaoming', 95.0);
insert into t_update_mvcc_2 values (4, 'zhanghua', 88.5);
insert into t_update_mvcc_2 values (7, 'xiaoyang', 91.0);
insert into t_update_mvcc_2 values (10, 'wangming', 92.0);
select * from t_update_mvcc_2;
update t_update_mvcc_2 set score = 99 where name = 'xiaoyang'
