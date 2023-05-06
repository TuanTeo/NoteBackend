
def verifyProof(z, p, c, h, u, g):
    # print('z', z)
    # print('p', p)
    # print('c', c)
    # print('u', u)
    # print('g', g)

    vt = pow(int(g), int(z), int(p))
    vp = (int(u) * pow(int(h), int(c), int(p))) % int(p)

    # print('vt', vt)
    # print('vp', vp)

    if vt == vp:
        is_verified = True
    else:
        is_verified = False

    # print('is_verified', is_verified)
    return is_verified
