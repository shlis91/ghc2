from math import ceil

def scorer(score_loc, full_time):
    f = open(world_loc, 'r')
    s = f.read()
    f.close()

    score = 0
    lines = s.split('\n')
    for line in lines[1:]:
        command = lines.split()
        if ('D' in command) & (len(command) == 5):
            score += int(ceil((full_time - int(command[-1])) / float(full_time)))

    return score


