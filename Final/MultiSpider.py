import time
from multiprocessing import Process
from threading import Thread

from Final import Spider

class MultiSpider:

    processList = []

    def digikeySpider(self):
        spider = Spider.DigiKeySpider()

        spider.catchData()

    def multiProcess(self):

        for i in range(4):
            i = Process(target=self.digikeySpider)
            i.start()
            self.processList.append(i)
            i.join(timeout=10000)
