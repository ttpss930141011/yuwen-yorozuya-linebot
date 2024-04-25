from unittest import mock

from src.interactor.use_cases.message.cor import ReplyMessagesCOR


def test_reply_message_cor_initial(mocker: mock):
    container_mock = mocker.MagicMock()
    muting_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.MutingHandler")
    default_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.DefaultHandler")
    # addition_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.AdditionHandler")
    window_mutable_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.WindowMutableHandler")
    viki_handler_mock = mocker.patch("src.interactor.use_cases.message.cor.VikiHandler")

    muting_handler_mock_instance = muting_handler_mock.return_value
    # addition_handler_mock_instance = addition_handler_mock.return_value
    default_handler_mock_instance = default_handler_mock.return_value
    window_mutable_handler_mock_instance = window_mutable_handler_mock.return_value
    viki_handler_mock_instance = viki_handler_mock.return_value

    reply_messages_cor = ReplyMessagesCOR(container_mock)

    viki_handler_mock_instance.set_successor.assert_called_once_with(window_mutable_handler_mock_instance)
    window_mutable_handler_mock_instance.set_successor.assert_called_once_with(muting_handler_mock_instance)
    muting_handler_mock_instance.set_successor.assert_called_once_with(default_handler_mock_instance)
    default_handler_mock_instance.set_successor.assert_not_called()

    assert reply_messages_cor._chain == viki_handler_mock_instance


def test_reply_message_cor_handle(mocker: mock):
    container_mock = mocker.MagicMock()
    input_dto = mocker.MagicMock()

    reply_messages_cor = ReplyMessagesCOR(container_mock)

    reply_messages_cor._chain.handle = mocker.Mock()

    reply_messages_cor.handle(input_dto)
    reply_messages_cor._chain.handle.assert_called_once_with(input_dto)
