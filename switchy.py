import random

N = 8
n = 2

def generate():
    return [[random.randint(0, 1) for i in range(N)] for i in range(N)]

def switch(grid, x, y, n):
    return [[item ^ (x <= r < x + n and y <= c < y + n) for c, item in enumerate(row)]
        for r, row in enumerate(grid)]

def len_cols(grid):
    return len(grid[0])

def extract_row(grid, r):
    return grid[r]

def extract_col(grid, c):
    return [row[c] for row in grid]

def remove_rows(grid, rows):
    return [row for r, row in enumerate(grid) if r not in rows]

def remove_cols(grid, cols):
    return [[col for c, col in enumerate(row) if c not in cols] for row in grid]

def collapse(grid):
    done = False
    while not done and grid and grid[0]:
        done = True
        for [name, length, extract, remove] in [['row', len, extract_row, remove_rows],
            ['column', len_cols, extract_col, remove_cols]]:
            to_remove = set()
            for i in range(length(grid)):
                if len(set(extract(grid, i))) <= 1:
                    to_remove.add(i)
            if to_remove:
                print('Removing %ss %s...' % (name, ', '.join(map(str, to_remove))))
                grid = remove(grid, to_remove)
                done = False
            if not grid or not grid[0]:
                break
    return grid

def winnable(grid):
    if len(grid) & 1 or len_cols(grid) & 1:
        return True
    if not all(sum(extract_row(grid, r)) & 1 for r in range(len(grid))):
        return True
    if not all(sum(extract_col(grid, c)) & 1 for c in range(len_cols(grid))):
        return True
    return False

def show(grid):
    print('   %s' % ''.join('%2i' % i for i in range(len_cols(grid))))
    border = '   +%s+' % ('-' * (2 * len_cols(grid) - 1))
    print(border)
    print('\n'.join('%2i |%s|' % (x, ' '.join('.#'[i] for i in row)) for x, row in enumerate(grid)))
    print(border)

grid = generate()
while True:
    grid = collapse(grid)

    if not grid or not grid[0]:
        print('WIN!')
        grid = generate()
        continue
    elif not winnable(grid):
        print('LOSE!')
        grid = generate()
        continue

    show(grid)

    while True:
        try:
            cmd = input('> ').strip()
            if cmd == 'n':
                grid = generate()
                show(grid)
                continue
            x, y = [int(i) for i in cmd.split()]
            assert 0 <= x <= len(grid) - n and 0 <= y <= len_cols(grid) - n
        except Exception:
            print('error')
        else:
            break
    grid = switch(grid, x, y, n)
