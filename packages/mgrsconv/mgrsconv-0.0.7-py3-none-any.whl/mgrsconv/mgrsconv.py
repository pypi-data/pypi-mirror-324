import math

def dd2mgrs(Lat, Long):
    if Lat < -80:
        return 'Too far South'
    if Lat > 84:
        return 'Too far North'

    c = 1 + math.floor((Long + 180) / 6)
    e = c * 6 - 183
    k = Lat * math.pi / 180
    l = Long * math.pi / 180
    m = e * math.pi / 180
    n = math.cos(k)
    o = 0.006739496819936062 * math.pow(n, 2)
    p = 40680631590769 / (6356752.314 * math.sqrt(1 + o))
    q = math.tan(k)
    r = q * q
    s = (r * r * r) - math.pow(q, 6)
    t = l - m
    u = 1.0 - r + o
    v = 5.0 - r + 9 * o + 4.0 * (o * o)
    w = 5.0 - 18.0 * r + (r * r) + 14.0 * o - 58.0 * r * o
    x = 61.0 - 58.0 * r + (r * r) + 270.0 * o - 330.0 * r * o
    y = 61.0 - 479.0 * r + 179.0 * (r * r) - (r * r * r)
    z = 1385.0 - 3111.0 * r + 543.0 * (r * r) - (r * r * r)
    aa = p * n * t + (p / 6.0 * math.pow(n, 3) * u * math.pow(t, 3)) + (
            p / 120.0 * math.pow(n, 5) * w * math.pow(t, 5)) + (p / 5040.0 * math.pow(n, 7) * y * math.pow(t, 7))
    ab = 6367449.14570093 * (k - (0.00251882794504 * math.sin(2 * k)) + (0.00000264354112 * math.sin(4 * k)) - (
            0.00000000345262 * math.sin(6 * k)) + (0.000000000004892 * math.sin(8 * k))) + (
                 q / 2.0 * p * math.pow(n, 2) * math.pow(t, 2)) + (
                 q / 24.0 * p * math.pow(n, 4) * v * math.pow(t, 4)) + (
                 q / 720.0 * p * math.pow(n, 6) * x * math.pow(t, 6)) + (
                 q / 40320.0 * p * math.pow(n, 8) * z * math.pow(t, 8))
    aa = aa * 0.9996 + 500000.0
    ab = ab * 0.9996
    if ab < 0.0:
        ab += 10000000.0
    ad = 'CDEFGHJKLMNPQRSTUVWXX'[math.floor(Lat / 8 + 10)]
    ae = math.floor(aa / 100000)
    af = ['ABCDEFGH', 'JKLMNPQR', 'STUVWXYZ'][(c - 1) % 3][ae - 1]
    ag = math.floor(ab / 100000) % 20
    ah = ['ABCDEFGHJKLMNPQRSTUV', 'FGHJKLMNPQRSTUVABCDE'][(c - 1) % 2][ag]

    def pad(val):
        if val < 10:
            val = '0000' + str(val)
        elif val < 100:
            val = '000' + str(val)
        elif val < 1000:
            val = '00' + str(val)
        elif val < 10000:
            val = '0' + str(val)
        return val

    aa = math.floor(aa % 100000)
    aa = pad(aa)
    ab = math.floor(ab % 100000)
    ab = pad(ab)

    return f'{c}{ad} {af}{ah} {aa} {ab}'

# Function to convert MGRS to Latitude and Longitude
def mgrs2dd(mgrs):
    try:
        b = mgrs.strip().split()
        if not b or len(b) != 4:
            return False, None, None

        c = b[0][0] if len(b[0]) < 3 else b[0][:2]
        d = b[0][1] if len(b[0]) < 3 else b[0][2]
        e = (int(c) * 6 - 183) * math.pi / 180

        f = ["ABCDEFGH", "JKLMNPQR", "STUVWXYZ"][(int(c) - 1) % 3].find(b[1][0]) + 1
        g = "CDEFGHJKLMNPQRSTUVWXX".find(d)

        h = ["ABCDEFGHJKLMNPQRSTUV", "FGHJKLMNPQRSTUVABCDE"][(int(c) - 1) % 2].find(b[1][1])
        i = [1.1, 2.0, 2.8, 3.7, 4.6, 5.5, 6.4, 7.3, 8.2, 9.1, 0, 0.8, 1.7, 2.6, 3.5, 4.4, 5.3, 6.2, 7.0, 7.9]
        j = [0, 2, 2, 2, 4, 4, 6, 6, 8, 8, 0, 0, 0, 2, 2, 4, 4, 6, 6, 6]
        k = i[g]
        l = j[g] + h / 10

        if l < k:
            l += 2

        m = f * 100000.0 + int(b[2])
        n = l * 1000000 + int(b[3])
        m -= 500000.0

        if d < 'N':
            n -= 10000000.0

        m /= 0.9996
        n /= 0.9996

        o = n / 6367449.14570093
        p = o + (0.0025188266133249035 * math.sin(2.0 * o)) + (0.0000037009491206268 * math.sin(4.0 * o)) + (
                0.0000000074477705265 * math.sin(6.0 * o)) + (0.0000000000170359940 * math.sin(8.0 * o))
        q = math.tan(p)
        r = q * q
        s = r * r
        t = math.cos(p)
        u = 0.006739496819936062 * t ** 2
        v = 40680631590769 / (6356752.314 * math.sqrt(1 + u))
        w = v
        x = 1.0 / (w * t)
        w *= v
        y = q / (2.0 * w)
        w *= v
        z = 1.0 / (6.0 * w * t)
        w *= v
        aa = q / (24.0 * w)
        w *= v
        ab = 1.0 / (120.0 * w * t)
        w *= v
        ac = q / (720.0 * w)
        w *= v
        ad = 1.0 / (5040.0 * w * t)
        w *= v
        ae = q / (40320.0 * w)

        lat = p + y * (-1.0 - u) * (m ** 2) + aa * (
                    5.0 + 3.0 * r + 6.0 * u - 6.0 * r * u - 3.0 * (u * u) - 9.0 * r * (u * u)) * (m ** 4) + ac * (
                          -61.0 - 90.0 * r - 45.0 * s - 107.0 * u + 162.0 * r * u) * (m ** 6) + ae * (
                          1385.0 + 3633.0 * r + 4095.0 * s + 1575 * (s * r)) * (m ** 8)
        lng = e + x * m + z * (-1.0 - 2 * r - u) * (m ** 3) + ab * (
                    5.0 + 28.0 * r + 24.0 * s + 6.0 * u + 8.0 * r * u) * (m ** 5) + ad * (
                          -61.0 - 662.0 * r - 1320.0 * s - 720.0 * (s * r)) * (m ** 7)

        return True, lat * 180 / math.pi, lng * 180 / math.pi

    except Exception as e:
        print(f"Error converting MGRS: {e}")
        return False, None, None

