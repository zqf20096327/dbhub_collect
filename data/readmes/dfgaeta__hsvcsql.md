# hsvcsql - SQLite3 via SVC on Hercules 3.13

Redirects SVC 251 from the guest to a dynamic Hercules module (HDL) that executes SQLite3. Includes an assembler API (macros), callable entry point, and examples.

**Minimum guest requirement: MVS 3.8J** (IFOX00, IEWL, ANS COBOL).
Everything also runs on VM/SP CMS and on later systems (MVS/XA, OS/390, z/OS), since it only uses Assembler XF features, S/370 instructions, standard OS linkage, and QSAM.

## Structure

| Directory/file                 | Contents                                                                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hercules/general2.c.patch`    | Hook in `DEF_INST(supervisor_call)`, before ECPS:VM                                                                                                   |
| `hercules/hsvcsql.h`           | Hook <-> module interface (`HSVC_CTX`, R0-R15, storage access)                                                                                        |
| `hercules/hsvcsql.c`           | HDL module: functions 1 through 10 (OPEN ... BINDLIST)                                                                                                |
| `hercules/Makefile.am.snippet` | Module inclusion in the build                                                                                                                         |
| `api/*.MACRO`                  | Macros SQLEQU, SQLPARM, SQLBDESC, SQLOPEN, SQLCLOSE, SQLEXEC, SQLPREP, SQLFETCH, SQLFINAL, SQLBIND, SQLRESET, SQLRUN, SQLBLIST, and internal SQL#xxxx |
| `api/SQLAPI.ASSEMBLE`          | Callable entry point (assembler, ANS COBOL, FORTRAN)                                                                                                  |
| `api/SQLDEMO.ASSEMBLE`         | Macro example, with output to SYSPRINT                                                                                                                |
| `api/SQLTEST.ASSEMBLE`         | Example using the SVC directly, without macros                                                                                                        |
| `api/SQLCOBD.COBOL`            | ANS COBOL example using SQLAPI                                                                                                                        |
| `api/SQLPARMC.COPY`            | COBOL parameter block copybook                                                                                                                        |
| `mvs/SQLINST.JCL`              | IEBUPDTE: creates MACLIB, SOURCE, and LOADLIB (all source code embedded)                                                                              |
| `mvs/SQLBLD.JCL`               | IFOX00 + IEWL for SQLAPI/SQLDEMO/SQLTEST and execution                                                                                                |
| `mvs/SQLCOB.JCL`               | IKFCBL00 + IEWL + execution of SQLCOBD                                                                                                                |
| `cms/SQLBUILD.EXEC`            | Generates the MACLIB and assembles everything under CMS                                                                                               |

## Hercules

1. `patch -p1 < hercules/general2.c.patch`
2. Copy `hsvcsql.c` and `hsvcsql.h` to the source root directory.
3. Adjust `Makefile.am` according to the snippet (including `-lsqlite3`).
4. `./autogen.sh && ./configure && make && make install`
5. From the console or in the `.cnf`: `ldmod hsvcsql`

Options: `-DHSVC_SQLITE_NUM=nnn` (default 251) and `-DHSVC_REQUIRE_AUTH=1`
(requires supervisor state or key < 8).

## MVS 3.8J

1. Replace `HERC01` with your prefix in the three jobs.
2. Submit `SQLINST`, then `SQLBLD`, then `SQLCOB` (optional).
3. `SQLDEMO` lists the table in SYSPRINT; `SQLCOBD` writes to SYSOUT.

For your programs: the IFOX00 SYSLIB is `SYS1.MACLIB` +
`HERC01.SQLITE.MACLIB`; COBOL links to `SQLAPI` by autocall from the LOADLIB.

## CMS (VM/SP Rel 5)

Transfer `api/name.MACRO` as `name MACRO A`, `api/name.ASSEMBLE` as `name ASSEMBLE A`, and `cms/SQLBUILD.EXEC` as `SQLBUILD EXEC A`.

Execute `SQLBUILD` and then `LOAD SQLDEMO (START`.

## Calling Convention

* R0 = function, R1 = 40-byte parameter block (macro `SQLPARM`)
* R15: 0 = OK, 4 = end of data, 8 = truncated, 12 = SQLite error (message in buffer), 16 = invalid parameter, 20 = table full, 24 = unauthorized
* R0: SQLite code
* SQLAPI: `CALL SQLAPI,(FUNCTION,PARM[,RC[,DATA[,BUFFER]]]),VL`; DATA and BUFFER populate the addresses in the parameter block (ANS COBOL cannot obtain field addresses). SQL-BTS in COBOL = type * 256 + scale.

## Notes / Precautions

* Make sure SVC 251 is not already in use on your MVS (IEASVCxx / TK4- SVC table); with the module loaded, Hercules intercepts it before the operating system.
* The database path and host system path are lowercase in the examples: submit the jobs while preserving lowercase characters.
* Any guest program accesses files with the permissions of the Hercules process.
* Calls are serialized by a global lock; long-running queries hold the CPU that issued the SVC.
