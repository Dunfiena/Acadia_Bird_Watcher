import Bird


def clean_slate(bird):
    for check in bird:
        for b in bird:
            if (b.getX() == check.getX() and b.getY() == check.getY()
                    and b.getAge() == check.getAge() and b.getId() != check.getId()):
                bird.remove(b)

    return bird
