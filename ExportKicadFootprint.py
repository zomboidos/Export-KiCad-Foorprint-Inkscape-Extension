#!/usr/bin/env python3
import inkex
import sys

from os import path as os_path
from tkinter import filedialog
from inkex import paths
from inkex import transforms

inkex.localization.localize()

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class TemplateEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
    def effect(self):
        data = "(module $my_footprint$ (layer F.Cu) (tedit 6006CE23)\n" \
               " (fp_text reference REF** (at 0 0.5) (layer F.SilkS) hide\n" \
               "     (effects (font (size 1 1) (thickness 0.15)))\n" \
               " )\n" \
               " (fp_text value $my_footprint$ (at 0 -0.5) (layer F.Fab)\n" \
               "     (effects (font (size 1 1) (thickness 0.15)))\n" \
               " )\n"

        cu_layer = ""
        mask_layer = ""

        for id, node in self.selected.items():
            if node.tag == inkex.addNS('path','svg'):
                line = "(fp_poly\n\t(pts "
                node.apply_transform()
                d = node.get('d')
                p = paths.CubicSuperPath(d)
                for subpath in p:
                    for csp in subpath:
                        line += "(xy " + str(csp[1][0]) + " " + str(csp[1][1]) + ") "

                cu_layer = line + ")\n\t(layer F.Cu) (width 0.01))\n"
                mask_layer = line + ")\n\t(layer F.Mask) (width 0.01))\n"
                data += cu_layer
                data += mask_layer
        if not self.selected.items():
            inkex.errormsg(_("Please select some paths. And don't forget to convert objects to paths."))
            return

        data += ")\n"
        ext = 'kicad_mod'
        ftypes = [('KiCad Footpring', '*.' + ext)]
        with filedialog.asksaveasfile(filetypes=ftypes, defaultextension=ext) as file:
            filename = os_path.splitext(os_path.basename(file.name))[0]
            file.write(data.replace("$my_footprint$", filename))


TemplateEffect().run()
sys.exit(0) #helps to keep the selection
