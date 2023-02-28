import logging
import logging.handlers

log = logging.getLogger('snowdeer_log')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) > %(message)s')

fileHandler = logging.FileHandler('./log.txt')
streamHandler = logging.StreamHandler()

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

log.addHandler(fileHandler)
log.addHandler(streamHandler)

if __name__ == '__main__':
    error = 'eft'
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')

    for i in range(100):
        if i%3 == 0:
            log.error(f'error {error}')
        else:
            log.debug('debug')

    
