import Bird


def clean_handler(bird, bird_saved):
    bird_saved = sort_index(bird_saved)
    bird = clean_index(bird, bird_saved)

    return bird


def clean_slate(bird):
    bird = sort_index(bird)

    for check in bird:
        for b in bird:
            if (b.getX() == check.getX() and b.getY() == check.getY()
                    and b.getAge() == check.getAge() and b.getId() != check.getId()):
                bird.remove(b)

    return bird


def sort_index(bird):
    for x in bird:
        for y in bird:
            if x.getId() < y.getId():
                tmp = x.getId()
                x.setId(y.getId())
                y.setId(tmp)

    return bird


def clean_index(bird, bird_saved):
    if len(bird_saved) > 0:
        last_index = bird_saved[-1].getId()
    else:
        last_index = 0

    for x in bird:
        if x.getId() > last_index:
            last_index += 1
            x.setId(last_index)

    return bird


def end_run_clean_index(birds):
    index = 0
    for x in birds:
        x.setId(index)
        index += 1

    return birds
