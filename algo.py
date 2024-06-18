import Bird


def clean_slate(bird):
    sort(bird)
    birds_return = []
    for check in bird:
        for b in bird:
            if (b.getX() == check.getX() and b.getY() == check.getY and b.getAge() == check.getAge()):
                birds_return.append(b)
                bird.remove(b)

    return birds_return

def sort(bird):
    return bird