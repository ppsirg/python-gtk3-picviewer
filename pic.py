#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" my small picviewer """
# TODO: if pic < win don't change dimensions
# caching of next and previous pic
import sys
import lib
import os
from gi.repository import Gtk, Gdk, GLib, GObject, GdkPixbuf, Gio, Pango

DIA = 5  # diashow timer in seconds

class PicViewer(Gtk.Window):
    """ small gtk-pic-viewer main class """
    def __init__(self):
        Gtk.Window.__init__(self)

        # Properties
        self.is_fullscreen = False
        self.is_dia = False
        self.dim = (500, 400)

        # Globals
        self.pix = None
        self.ani = False
        self.files = []
        self.index = 0
        self.image = Gtk.Image()
        #self.prev_img = gtk.Image()
        #self.post_img = gtk.Image()
        #self.dim = self.window.get_size()
        #print self.get_allocation()

        # Window stuff
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(self.dim[0], self.dim[1])

        # Events
        self.connect('button-press-event', self.on_double_click)
        self.connect('destroy', Gtk.main_quit)
        self.connect('key-press-event', self.on_key)
        self.connect('configure-event', self.on_config)
        #self.connect('scroll-event', self.on_scroll)

        # Functions
        self.files = lib.load_file_list(sys.argv[1], lib.PIC)
        if self.files == []:
            print("no images found")
            sys.exit(1)
        self.load_pic()
        self.update_image()

        # Drawing the Window
        self.add(self.image)
        self.show_all()

        # Start in Fullscreen mode
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.fullscreen_toggle()

        # Start with Diashow
        if self.is_dia:
            glib.timeout_add_seconds(DIA, self.on_tick)

    def on_config(self, widget, event):
        """ call if window geometry changes """
        if self.dim != self.get_size():
            self.dim = self.get_size()
            self.update_image()

    def load_pic(self):
        """ load new pictures in buffer """
        self.ani = self.files[self.index].lower().endswith(".gif")
        if self.ani:
            self.pix = GdkPixbuf.PixbufAnimation.new_from_file(self.files[self.index])
        else:
            self.pix = GdkPixbuf.Pixbuf.new_from_file(self.files[self.index])
        self.set_title(self.files[self.index])

    def update_image(self):
        """ update picture """
        if self.ani:
            self.image.set_from_animation(self.pix)
        else:
            test = lib.scale(self.pix.get_width(), self.pix.get_height(), \
                self.dim[0], self.dim[1])
            newpix = self.pix.scale_simple(test[0], test[1], \
                GdkPixbuf.InterpType.BILINEAR)
            self.image.set_from_pixbuf(newpix)

    def update_pic(self):
        """ update picture if changes """
        if len(self.files) == 0:
            Gtk.main_quit()
        else:
            self.index = self.index % len(self.files)
            self.load_pic()
            self.update_image()

    def fullscreen_toggle(self):
        """ fullscreen function """
        if self.is_fullscreen:
            self.unfullscreen()
            self.modify_bg(Gdk.CrossingMode.NORMAL, None)
            #self.window.set_cursor(None)
            self.is_fullscreen = False
        else:
            self.fullscreen()
            #pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
            color = Gdk.Color(0, 0, 0)  # creates black background
            #cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
            #self.window.set_cursor(cursor)
            self.modify_bg(Gdk.CrossingMode.NORMAL, color)
            self.is_fullscreen = True

    def on_key(self, widget, event):
        """ keyboard shortcuts """
        if event.keyval == Gdk.keyval_from_name("Right"):
            self.index += 1
            self.update_pic()
        elif event.keyval == Gdk.keyval_from_name("Left"):
            self.index -= 1
            self.update_pic()
        elif event.keyval == Gdk.keyval_from_name("Escape"):
            if self.is_fullscreen:
                self.fullscreen_toggle()
            else:
                Gtk.main_quit()
        elif event.keyval == Gdk.keyval_from_name("q"):
            Gtk.main_quit()
        elif event.keyval == Gdk.keyval_from_name("F11") \
            or event.keyval == Gdk.keyval_from_name("f"):
            self.fullscreen_toggle()
        elif event.keyval == Gdk.keyval_from_name("space"):
            # XXX: HACK
            self.is_dia ^= True
            if self.is_dia:
                GLib.timeout_add_seconds(DIA, self.on_tick)
        elif event.keyval == Gdk.keyval_from_name("Delete"):
            os.remove(self.files[self.index])
            del self.files[self.index]
            self.update_pic()
        elif event.keyval == Gdk.keyval_from_name("Up"):
            if not self.ani:
                self.pix = self.pix.rotate_simple( \
                    GdkPixbuf.PixbufRotation.CLOCKWISE)
                self.update_image()
        elif event.keyval == Gdk.keyval_from_name("Down"):
            if not self.ani:
                self.pix = self.pix.rotate_simple( \
                    GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)
                self.update_image()

    def on_tick(self):
        """ diashow """
        if self.is_dia:
            self.index += 1
            self.update_pic()
        return self.is_dia

    def on_double_click(self, widget, event):
        """ doubleclick """
        if event.button == 1 and event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            self.fullscreen_toggle()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python {} <pic>".format(sys.argv[0]))
        sys.exit(1)
    PicViewer()
    Gtk.main()
