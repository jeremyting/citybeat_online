from utility.event import Event


class PhotoEvent(Event):
    def __init__(self, event=None):
        # the input argument event should be a dictionary or python object
        super(PhotoEvent, self).__init__(event)


def main():
    p = PhotoEvent()


if __name__ == '__main__':
    main()