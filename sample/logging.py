import logging

# 创建日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建日志处理器并设置级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将格式器添加到处理器
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 记录日志
logger.debug('这是一个debug级别的日志')
logger.info('这是一个info级别的日志')
logger.warning('这是一个warning级别的日志')
logger.error('这是一个error级别的日志')
logger.critical('这是一个critical级别的日志')
