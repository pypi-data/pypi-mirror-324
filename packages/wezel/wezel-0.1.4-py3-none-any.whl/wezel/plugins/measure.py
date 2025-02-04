
from wezel.gui import Menu
from wezel.plugins import (
    skimage,
    scipy,
    vreg,
)

menu = Menu('Measure')
menu.add(skimage.action_volume_features)
menu.add(vreg.action_roi_statistics)
menu.add(vreg.action_roi_histogram)
menu.add(scipy.action_roi_curve)

    




