from unittest.mock import Mock

from src.t_menu.menu import Menu


def test_single_menu(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1')

    the_function = Mock()

    title = 'The Menu'
    m = Menu(1, title, the_function)
    m.run()

    out, err = capsys.readouterr()
    assert title in out

    the_function.assert_called_once()


def test_two_main_menus(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'M2')

    main_function = Mock()
    m1_function = Mock()
    m2_function = Mock()

    main_title = 'Main Menu'
    m = Menu(1, main_title, main_function)

    main_1_tile = 'Main 1'
    m1 = Menu('M1', main_1_tile, m1_function)
    m.add_sub_menu(m1)

    main_2_tile = 'Main 2'
    m2 = Menu('M2', main_2_tile, m2_function)
    m.add_sub_menu(m2)

    m.run()

    out, err = capsys.readouterr()
    assert main_title in out
    assert main_1_tile in out
    assert m1.id in out
    assert main_2_tile in out
    assert m2.id in out

    m1_function.assert_not_called()
    m2_function.assert_called_once()


def test_with_sub_menu(capsys, monkeypatch):
    def inputs():
        yield '2'  # Select 'Main 2'
        yield '21'  # Select 'Sub 21'

    user_inputs = inputs()
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    m11_function = Mock()
    m21_function = Mock()
    m22_function = Mock()

    main_title = 'Main Menu'
    m = Menu('root', main_title)

    main1_tile = 'Main 1'
    m1 = Menu('1', main1_tile)
    m.add_sub_menu(m1)

    main2_title = 'Main 2'
    m2 = Menu('2', main2_title)
    m.add_sub_menu(m2)

    sub11_title = 'Sub 11'
    s11 = Menu('11', sub11_title, m11_function)
    m1.add_sub_menu(s11)

    sub21_title = 'Sub 21'
    s21 = Menu('21', sub21_title, m21_function)
    m2.add_sub_menu(s21)

    sub22_title = 'Sub 22'
    s22 = Menu('22', sub22_title, m22_function)
    m2.add_sub_menu(s22)

    m.run()

    out, err = capsys.readouterr()
    assert main_title in out
    assert main1_tile in out
    assert m1.id in out
    assert main2_title in out
    assert m2.id in out
    assert sub11_title not in out
    assert s11.id not in out
    assert sub21_title in out
    assert s21.id in out
    assert sub22_title in out
    assert s22.id in out

    m11_function.assert_not_called()
    m22_function.assert_not_called()
    m21_function.assert_called_once()
