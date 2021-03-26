
import logging


def get_logger(name: str, level: int, fmt: str = logging.BASIC_FORMAT):
    logger = logging.getLogger(name)
    # logger.propagate = False
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger



if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    log_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    logger = get_logger('logger1', logging.ERROR, log_format)
    logger2 = get_logger('logger2', logging.WARNING, log_format)

    logger2.warning('dfb;sdfbsdkjf')
    logger.debug('でばぐ')
    logger.info('info')
    logger.warning('w a r n i n g')
    logger.error('it\'s error!!')
    logger.critical('CRITICAAAAAL!!')
