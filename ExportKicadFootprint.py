#!/usr/bin/env python3
import inkex
import sys
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
        data = "(module logo_sam (layer F.Cu) (tedit 6006CE23)" +
               " (fp_text reference REF** (at 0 0.5) (layer F.SilkS) hide" +
               "     (effects (font (size 1 1) (thickness 0.15)))" +
               " )" +
               " (fp_text value logo_sam (at 0 -0.5) (layer F.Fab)" +
               "     (effects (font (size 1 1) (thickness 0.15)))" +
               " )"

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
            break
        else:
            inkex.errormsg(_("Please select some paths. And don't forget to convert objects to paths."))
            return

        ext = 'kicad_mod'
        ftypes = [('KiCad Footpring', '*.' + ext)]
        with filedialog.asksaveasfile(filetypes=ftypes, defaultextension=ext) as file:
            file.write(data)

TemplateEffect().run()
sys.exit(0) #helps to keep the selection
