# -*- coding: utf-8 -*-

import pytest

from PyQt5.QtWidgets import QAction, QApplication, QWidgetAction
from PyQt5 import QtCore

from loge.gui.main_window import MainWindow
from loge.gui.main_menu import MainMenuBar
from loge.gui.main_toolbar import MainToolBar

#QApplication instance for GUI tests
app = QApplication([])

@pytest.fixture()
def main_window():
    return MainWindow('test','0.0.0')

@pytest.fixture()
def main_actions():
    actions_expected = ['file_new','file_open','file_openreadonly','file_save','file_saveas'
                        ,'reload_script_file','file_edit','show_html','show_markdown'
                        ,'save_markdown','preview_markdown','show_source','show_loge','print','help','about'
                        ,'floatprecision','syntax','tutorial']
    actions_expected.sort()
    return actions_expected

class TestMainWindow:


    def test_init_main_window(self,main_window,main_actions):
        #title
        assert 'test (0.0.0)' == main_window.windowTitle()
        #minimum size
        min_size = main_window.minimumSize()
        assert 100 == min_size.height()
        assert 100 == min_size.width()

        #actions dictionary
        actions = main_window.actions
        actions_keys = list(actions.keys())
        actions_keys.sort()
        
        #check actions names
        assert not actions_keys is None #checking if a sort result is right
        assert not main_actions is None #checking if a sort result is right
        assert main_actions == actions_keys
        #check all actions type
        for (k,v) in actions.items():
            assert isinstance(v, QAction), "Argument '{}' of wrong type!".format(k)

    def test_set_action_slot_wrong_action_name_keyerror(self,main_window):
        with pytest.raises(KeyError) as exc_info:
            main_window.set_action_slot(None,None)
        assert 'None' in str(exc_info.value)
        
        with pytest.raises(KeyError) as exc_info:
            action_name = 'no_action'
            main_window.set_action_slot(action_name,None)
        assert action_name in str(exc_info.value)

    def test_set_action_slot_wrong_slot(self,main_window):
        with pytest.raises(TypeError) as exc_info:
            main_window.set_action_slot('file_new',None)
        assert 'NoneType' in str(exc_info.value)

    def test_set_action_slot(self,main_window,capsys):

        action_name = 'file_new'

        def fake_slot_undecorated():
            print('fake slot undecorated - trigger signal received')

        main_window.set_action_slot(action_name,fake_slot_undecorated)
        #emit the signal
        main_window.actions[action_name].activate(QAction.Trigger)
        #disconnect slot
        main_window.actions[action_name].disconnect()
        out, err = capsys.readouterr()
        assert out.rstrip() == 'fake slot undecorated - trigger signal received'
        assert err == ''

        @QtCore.pyqtSlot()
        def fake_slot_decorated():
            print('fake slot decorated - trigger signal received')

        main_window.set_action_slot(action_name,fake_slot_decorated)
        #emit the signal
        main_window.actions[action_name].activate(QAction.Trigger)
        #disconnect slot
        main_window.actions[action_name].disconnect()
        out, err = capsys.readouterr()
        assert out.strip() == 'fake slot decorated - trigger signal received'
        assert err == ''

#----------------------------------------------------------------------------
# Main Menu Tests
#----------------------------------------------------------------------------

@pytest.fixture()
def main_menu_bar():
    return MainMenuBar(None)

class TestMainMenu:

    def test_init_main_menu(self,main_menu_bar):
        mmb = main_menu_bar
        menu_expected = ['&File','&Script','&Help']
        menu_expected.sort()
        menu = []
        for action in mmb.actions():
            assert isinstance(action, QAction)
            menu.append(action.text())
        menu.sort()
        assert menu_expected == menu

    def test_add_menu_items_none_actions(self,main_menu_bar):
        with pytest.raises(ValueError) as exc_info:
            main_menu_bar.add_menu_items(None)
        assert 'An attribute "actions" dictionary can not be empty' == str(exc_info.value)

    def test_add_menu_items_empty_actions(self,main_menu_bar):
        with pytest.raises(ValueError) as exc_info:
            main_menu_bar.add_menu_items({})
        assert 'An attribute "actions" dictionary can not be empty' == str(exc_info.value)

    def test_add_menu_items_not_dict(self,main_menu_bar):
        with pytest.raises(TypeError) as exc_info:
            main_menu_bar.add_menu_items('test')
        assert 'An attribute "actions" should be a dictionary type' == str(exc_info.value)

    def test_add_menu_items_actions(self,main_menu_bar,main_actions):
        """
        tests if menu contains all necessary items (actions)
        """
        file_items_expected = ['file_new','file_open','file_openreadonly'
                            ,'file_save','file_saveas','print']
        file_items_expected.sort()

        script_items_expected = ['file_edit','reload_script_file','show_html'
                            ,'show_markdown','show_loge','floatprecision']
        script_items_expected.sort()

        help_items_expected = ['help','syntax','tutorial'
                            ,'about']
        help_items_expected.sort()

        #menu items will have the same names as keys in an actions dictionary
        actions = {key:QAction(key) for key in main_actions}
        main_menu_bar.add_menu_items(actions)

        file_items = []
        for m_action in main_menu_bar.m_file.actions():
            if not m_action.menu() and not m_action.isSeparator():
                file_items.append(m_action.text())
        file_items.sort()
        assert file_items_expected == file_items

        script_items = []
        for m_action in main_menu_bar.m_script.actions():
            if not m_action.menu() and not m_action.isSeparator():
                script_items.append(m_action.text())
        script_items.sort()
        assert script_items_expected == script_items

        help_items = []
        for m_action in main_menu_bar.m_help.actions():
            if not m_action.menu() and not m_action.isSeparator():
                help_items.append(m_action.text())
        help_items.sort()
        assert help_items_expected == help_items


#----------------------------------------------------------------------------
# Main Toolbar Tests
#----------------------------------------------------------------------------


@pytest.fixture()
def main_tool_bar():
    return MainToolBar(None)

class TestMainToolbar:

    def test_add_toolbar_items_none_actions(self,main_tool_bar):
        with pytest.raises(ValueError) as exc_info:
            main_tool_bar.add_toolbar_items(None)
        assert 'An attribute "actions" dictionary can not be empty' == str(exc_info.value)

    def test_add_toolbar_items_empty_actions(self,main_tool_bar):
        with pytest.raises(ValueError) as exc_info:
            main_tool_bar.add_toolbar_items({})
        assert 'An attribute "actions" dictionary can not be empty' == str(exc_info.value)

    def test_add_toolbar_items_not_dict(self,main_tool_bar):
        with pytest.raises(TypeError) as exc_info:
            main_tool_bar.add_toolbar_items('test')
        assert 'An attribute "actions" should be a dictionary type' == str(exc_info.value)

    def test_add_toolbar_items_actions(self,main_tool_bar,main_actions):
        """
        tests if toolbar contains all necessary items (actions)
        """
        items_expected = ['file_new','file_open','file_save','reload_script_file'
                         ,'file_edit','print','save_markdown','show_source'
                         ,'show_html','show_markdown','show_loge','preview_markdown'
                         ,'syntax']
        items_expected.sort()

        #menu items will have the same names as keys in an actions dictionary
        actions = {key:QAction(key) for key in main_actions}
        main_tool_bar.add_toolbar_items(actions)

        items = []
        for m_action in main_tool_bar.actions():
            print(type(m_action))
            if not m_action.isSeparator() and not isinstance(m_action,QWidgetAction):
                items.append(m_action.text())
        items.sort()
        assert items_expected == items

    #TODO: watch check-box test

        #script_items = []
        #for m_action in main_menu_bar.m_script.actions():
        #    if not m_action.menu() and not m_action.isSeparator():
        #        script_items.append(m_action.text())
        #script_items.sort()
        #assert script_items_expected == script_items

        # help_items = []
        # for m_action in main_menu_bar.m_help.actions():
        #     if not m_action.menu() and not m_action.isSeparator():
        #         help_items.append(m_action.text())
        # help_items.sort()
        # assert help_items_expected == help_items