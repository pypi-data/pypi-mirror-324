a = [{"role": "system"}]

def test(a):
    a[-1] = 2

test(a)
print(a)