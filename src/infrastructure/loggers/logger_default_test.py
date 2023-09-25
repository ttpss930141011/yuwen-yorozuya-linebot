import logging

from src.infrastructure.loggers.logger_default import LoggerDefault


def test_logger_default(mocker):
    mocker.patch.object(logging, "debug")
    logger = LoggerDefault()
    logger.log_debug("testdebug")
    logging.debug.assert_called_once_with("testdebug")

    mocker.patch.object(logging, "info")
    logger = LoggerDefault()
    logger.log_info("testinfo")
    logging.info.assert_called_once_with("testinfo")

    mocker.patch.object(logging, "warning")
    logger = LoggerDefault()
    logger.log_warning("tstwarn")
    logging.warning.assert_called_once_with("tstwarn")

    mocker.patch.object(logging, "error")
    logger = LoggerDefault()
    logger.log_error("testerror")
    logging.error.assert_called_once_with("testerror")

    mocker.patch.object(logging, "critical")
    logger = LoggerDefault()
    logger.log_critical("tcrit")
    logging.critical.assert_called_once_with("tcrit")

    mocker.patch.object(logging, "exception")
    logger = LoggerDefault()
    logger.log_exception("texce")
    logging.exception.assert_called_once_with("texce")
