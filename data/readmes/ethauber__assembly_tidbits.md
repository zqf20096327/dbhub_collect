# Assembly Register Conventions
64 bit register conventions
- rax - function return, arithmetic, or logical operations
- rbx - Memory addressing or "args to function"
- rcx - loop counter or string operations or "args to function"
- rdx - I/O ops or "args to function"
- rdi - destination index for string operations or "args to function"
- rsi - source index for string operations or "args to function"
- rbp - base pointer for stack frames
- rsp - stack pointer
- r8-r15 - additional "args to function" or temporary registers

32 bit register conventions
- eax - function return, arithmetic, or logical operations
- ebx - Memory addressing or "args to function"
- ecx - loop counter or string operations or "args to function"
- edx - I/O ops or "args to function"

# Relevant Docs
nasm basics: https://www.nasm.us/xdoc/2.13.03/html/nasmdoc3.html  

Apple syscall defs: https://opensource.apple.com/source/xnu/xnu-1504.3.12/bsd/kern/syscalls.master  
Apple shifts the syscall by 0x2000000 see SYSCALL_CLASS_SHIFT: https://opensource.apple.com/source/xnu/xnu-792.13.8/osfmk/mach/i386/syscall_sw.h  

If discussion interests you:  
apple syscall shift - https://stackoverflow.com/questions/48845697/macos-64-bit-system-call-table/53905561#53905561  
ld on mac - https://stackoverflow.com/questions/52830484/nasm-cant-link-object-file-with-ld-on-macos-mojave/52830915#52830915  


# Steps to Run
1. Install nasm

2. Assemble file with nasm.  
nasm -f \<systemExecutableFormat\> \<fileName\>.asm  
Assemble a file using Macho since that's Mac's underlying kernel.  
Also, use the 64 bit version since 32 bit is being deprecated by Apple/mac.  
On linux ELF format would likely be used since it is a standard executable format.  
Example: 
```shell
nasm -f macho64 hello.asm  
```

3. Link file using ld. (It's needed to use system libraries.)  
ld -arch \<systemArchitecture\> -o <fileName(Out)> \<fileName\>.o  
Link Program using the system's architecture using assembled object file.  
man ld to find your supported archs.  
Example[^*]:
```
ld -e _main -arch x86_64 -macosx_version_min 12.6.0 -L$(xcode-select -p)/SDKs/MacOSX.sdk/usr/lib -lSystem -o hello hello.o -no_pie
```
This is extra long since Apple has strict requirements.  
[^*]: Note: -no_pie is deprecated on newer mac targets. It'll require a position-independent code update  

4. Execute program
./hello
