from unittest import mock

from src.interactor.use_cases.message.cor import ReplyMessagesCOR


def test_reply_message_cor_initial(mocker: mock):
    muting_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.MutingHandler")
    default_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.DefaultHandler")
    addition_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.AdditionHandler")

    reply_messages_cor = ReplyMessagesCOR()

    muting_handler_mock.assert_called_once_with(addition_handler_mock.return_value)
    addition_handler_mock.assert_called_once_with(default_handler_mock.return_value)
    default_handler_mock.assert_called_once_with()

    assert reply_messages_cor._chain == muting_handler_mock.return_value


def test_reply_message_cor_handle(mocker: mock):
    mocker.patch("src.interactor.use_cases.message.cor.MutingHandler")
    mocker.patch("src.interactor.use_cases.message.cor.DefaultHandler")
    mocker.patch("src.interactor.use_cases.message.cor.AdditionHandler")

    reply_messages_cor = ReplyMessagesCOR()

    input_dto = mocker.Mock()
    repository = mocker.Mock()
    response = []

    reply_messages_cor._chain.handle = mocker.Mock()

    reply_messages_cor.handle(input_dto, repository)

    reply_messages_cor._chain.handle.assert_called_once_with(input_dto, repository, response)
