from typing import TypedDict, Tuple

SplitInfo = TypedDict(
    'SplitInfo', 
    full_size=int, stripe_size=int, 
    stripe_number=int, overlay_factor=float,
    )


def calaculate_stripe_pos(full_size:int, stripe_size, x):
    M = 1.0 * full_size / stripe_size
    factor = 1 - (1.0*(x - M)/(x - 1))
    pos = [ int(factor * stripe_size * i) for i in range(x)]
    pos = [ p if p + stripe_size <= full_size else full_size - stripe_size for p in pos ]
    return pos

    
def calaculate_stripe_number(full_size:int, stripe_size:int, overlay_range:Tuple[int,int]):
    if full_size < stripe_size:
        return (1, 0.0)

    M = 1.0 * full_size / stripe_size
    m = int(M)
    
    if m == 1:
        r = [2, 4]
    else:
        r = [m, m * 3]

    for x in range(*r):
        factor = 1.0*(x - M)/(x - 1)
        # print(f'{x} -> {factor:.3f}')
        if factor >= overlay_range[0]:
            if factor <= overlay_range[1] and x % 2 == 0:
                x = x + 1
                factor = 1.0*(x - M)/(x - 1)
                return (x, factor)
            return (x, factor)


def _exam(full_size, stripe_size, overlay_min, overlay_max):
    n, factor = calaculate_stripe_number(full_size, stripe_size, (overlay_min, overlay_max))
    print(f'{full_size}/{stripe_size} -> {n}/{factor:.3f} ')
    pos = calaculate_stripe_pos(full_size, stripe_size, n)
    print(','.join([str(p) for p in pos]))

def main():
    _exam(650, 640, 0.5, 0.95)
    _exam(1200, 640, 0.5, 0.95)
    _exam(1600, 640, 0.5, 0.95)
    _exam(6400, 640, 0.5, 0.95)

if __name__ == '__main__':
    main()