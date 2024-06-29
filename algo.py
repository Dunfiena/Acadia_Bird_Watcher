import Bird


def clean_slate(bird):
    bird_copy = bird
    birds_return = []
    for check in bird:
        double_flag = False
        for b in bird_copy:
            if b.getX() == check.getX() and b.getY() == check.getY() and b.getAge() == check.getAge():
                if not double_flag:
                    birds_return.append(check)
                    bird_copy.remove(b)
                    double_flag = True
                else:
                    bird.remove(b)


    return birds_return
