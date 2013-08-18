import threading, time, random
import time


class CandidateEventProcesser(threading.Thread):
    def __init__(self, classifier, document_interface):
        self._classifier = classifier
        self._document_interface = document_interface
        self._stop = threading.Event()
        #self._lastTime = 
        super(CandidateEventProcesser, self).__init__()

    def stop(self):
        self._stop.set()

    def run(self):
        while not self._stop.isSet():
            time.sleep(2)
            print time.time()


def main():
    cep = CandidateEventProcesser(None, None)
    cep.start()
    cep.stop()


if __name__ == '__main__':
    main()