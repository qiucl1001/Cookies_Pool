# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import time
import multiprocessing
from cookies_pool.processors.server import app
from cookies_pool.processors.tester import *
from cookies_pool.processors.generator import *
from cookies_pool.settings import CYCLE, TESTER_MAP, API_HOST, API_PORT, API_THREADED, GENERATOR_ENABLED,\
    TESTER_ENABLED, API_ENABLED, IS_WINDOWS, GENERATOR_MAP
from loguru import logger

if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, generator_process, server_process = None, None, None


class Scheduler(object):
    """
    scheduler class
    """
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        """
        valid cookie run
        """
        if not TESTER_ENABLED:
            logger.info(f'tester not enabled, exit!')
            return
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            logger.info(f'cookies检测进程开始进行...')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    loop += 1
                    logger.info(f'cookies检测完成!')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                reason = e.args
                logger.error(f'发生异常...{reason}')

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        """
        get cookie run
        """
        if not GENERATOR_ENABLED:
            logger.info('generator not enabled, exit!')
            return
        loop = 0
        while True:
            logger.debug(f'generator loop {loop} start...')
            logger.info('cookies生成进程开始进行...')
            try:
                for website, cls in GENERATOR_MAP.items():
                    g = eval(cls + '(website="' + website + '")')
                    g.run()
                    loop += 1
                    logger.info('cookies生成完成!')
                    del g
                    time.sleep(cycle)
            except Exception as e:
                reason = e.args
                logger.error(f'发生异常...{reason}')

    @staticmethod
    def api():
        """
        run server for api
        :return:
        """
        if not API_ENABLED:
            logger.info('server not enabled, exit!')
            return
        logger.info('api接口开始运行...')
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)

    def run(self):
        global tester_process, generator_process, server_process
        try:
            logger.info('starting cookies_pool...')
            if TESTER_ENABLED:
                tester_process = multiprocessing.Process(target=Scheduler.valid_cookie)
                logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            if GENERATOR_ENABLED:
                generator_process = multiprocessing.Process(target=Scheduler.generate_cookie)
                logger.info(f'starting generator, pid {generator_process.pid}...')
                generator_process.start()

            if API_ENABLED:
                server_process = multiprocessing.Process(target=Scheduler.api)
                logger.info(f'starting server, pid {server_process.pid}...')
                server_process.start()

            tester_process.join()
            generator_process.join()
            server_process.join()
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            tester_process.terminate()
            generator_process.terminate()
            server_process.terminate()
        finally:
            tester_process.join()
            generator_process.join()
            server_process.join()
            # logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
            logger.info(f'generator is {"alive" if generator_process.is_alive() else "dead"}')
            logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            logger.info('proxy terminated')


if __name__ == '__main__':
    s = Scheduler()
    s.run()
