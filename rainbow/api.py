
def deploy():
    print "deploying artifact"
    pass

def _roll_to_release(release):
    print "cutting-over to release: {release}".format(release=release)

def roll_to_next_release():
    _roll_to_release("next")

def roll_to_prev_release():
    _roll_to_release("prev")
