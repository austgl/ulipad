#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2006 limodou
#
#	Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	$Id: mLastStatus.py 481 2006-01-17 05:54:13Z limodou $

__doc__ = "Saveing last window status, including position, size, and Maximized or Iconized."

import wx
import wx.stc
from modules import Mixin

def pref_init(pref):
	pref.save_current_status = True
	pref.status_position = (0, 0)
	pref.status_size = (600, 400)
	pref.status = 3	#1 Iconized 2 Maximized 3 normal
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 140, 'check', 'save_current_status', tr('Saves current status when exit the program'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def afterclosewindow(win):
	if win.pref.save_current_status:
#		if win.IsIconized():
#			win.pref.status = 1
		if win.IsMaximized():
			win.pref.status = 2
		else:
			win.pref.status = 3
			saveWindowPosition(win)
		win.pref.save()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

def beforeinit(win):
	if win.pref.save_current_status:
		win.Move(win.pref.status_position)
		win.SetSize(win.pref.status_size)
#		if win.pref.status == 1:
#			win.Iconize()
		if win.pref.status == 2:
			win.Maximize()
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def mainframe_init(win):
	wx.EVT_MAXIMIZE(win, win.OnMaximize)
	wx.EVT_ICONIZE(win, win.OnIconize)
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def OnMaximize(win, event):
	saveWindowPosition(win)
	event.Skip()
Mixin.setMixin('mainframe', 'OnMaximize', OnMaximize)

def OnIconize(win, event):
	saveWindowPosition(win)
	event.Skip()
Mixin.setMixin('mainframe', 'OnIconize', OnIconize)

def saveWindowPosition(win):
	if win.IsIconized() == False and win.IsMaximized() == False:
		win.pref.status_position = win.GetPositionTuple()
		win.pref.status_size = win.GetSizeTuple()
		win.pref.save()