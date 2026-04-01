import socket
p10=[3,5,2,7,4,10,1,9,8,6]
p8=[6,3,7,4,8,5,10,9]
ip=[2,6,3,1,4,8,5,7]
ip1=[4,1,3,5,7,2,8,6]
ep=[4,1,2,3,2,3,4,1]
p4=[2,4,3,1]
s0=[[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
s1=[[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
def perm(x,t):
    return ''.join(x[i-1] for i in t)
def ls(x,n):
    return x[n:]+x[:n]
def ks(k):
    print("\nSubkey Generation:")
    k=perm(k,p10)
    print("After P10:", k)
    l,r=k[:5],k[5:]
    l,r=ls(l,1),ls(r,1)
    print("After LS-1:", l, r)
    k1=perm(l+r,p8)
    print("K1:", k1)
    l,r=ls(l,2),ls(r,2)
    print("After LS-2:", l, r)
    k2=perm(l+r,p8)
    print("K2:", k2)
    return k1,k2
def sb(x,s):
    r=int(x[0]+x[3],2)
    c=int(x[1]+x[2],2)
    return format(s[r][c],'02b')
def fk(x,k):
    l,r=x[:4],x[4:]
    t=perm(r,ep)
    t=format(int(t,2)^int(k,2),'08b')
    t=sb(t[:4],s0)+sb(t[4:],s1)
    t=perm(t,p4)
    l=format(int(l,2)^int(t,2),'04b')
    return l+r
def enc(p,k1,k2):
    print("\nIntermediate Results:")
    print("Plaintext:", p)
    x=perm(p,ip)
    print("After Initial Permutation (IP):", x)
    x=fk(x,k1)
    print("After Round 1:", x)
    x=x[4:]+x[:4]
    print("After Swap:", x)
    x=fk(x,k2)
    print("After Round 2:", x)
    ct=perm(x,ip1)
    print("Cipher Text:", ct)
    return ct

print("\nEncryption Side of SDES")
pt=input("Message / Plaintext (8-bit): ")
k=input("Key (10-bit): ")

k1,k2=ks(k)
ct=enc(pt,k1,k2)

s=socket.socket()
s.connect(("127.0.0.1",5006))
s.send((ct+"|"+k).encode())
s.close()
