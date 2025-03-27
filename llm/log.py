import logging

# 調整 cmd 預設 log 資訊
def init_logging():
    # 取得 log
    logger = logging.getLogger("uvicorn")
    logger.handlers = []

    # 定義輸出等級，僅有大於等於輸出等級的會有輸出顯示，也可以用數字替代
    # NOTSET = 0, 全部輸出
    # DEBUG = 10, 除錯資訊
    # INFO = 20, 正常資訊
    # WARNING = 30, 警告資訊
    # ERROR = 40, 錯誤資訊
    # CRITICAL = 50, 嚴重錯誤資訊
    logger.setLevel(logging.INFO)

    # console handler
    ch = logging.StreamHandler()
    # file handler
    fh = logging.FileHandler(filename='logs/logger.log')
    # rotating file handler
    # 限制 log 檔案大小，及備份，若超過指定數量則會自動刪除最舊的 log。
    # rh = logging.handlers.RotatingFileHandler('logs/rotatingfile', maxBytes=2000, backupCount=3)
    # 基於時間建立檔案，可以指定每周、每月、每年等等。
    th = logging.handlers.TimedRotatingFileHandler('logs/log.log', when='W0', interval=1,
                                                  backupCount=5)

    formatter = logging.Formatter("[%(asctime)s][%(name)-5s][%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d)", 
                                  datefmt="%Y-%m-%d %H:%M:%S"
                                )

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # rh.setFormatter(formatter)
    th.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    # logger.addHandler(rh)
    logger.addHandler(th)

    return logger