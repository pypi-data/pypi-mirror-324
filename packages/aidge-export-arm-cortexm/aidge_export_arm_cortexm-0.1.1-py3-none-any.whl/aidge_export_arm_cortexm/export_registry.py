from aidge_core.export_utils import ExportLib
from aidge_export_arm_cortexm.utils import ROOT

class ExportLibAidgeARM(ExportLib):
    _name="aidge_arm"
    def __init__(self, operator):
        super(ExportLibAidgeARM, self).__init__(operator)
        self.forward_template = str(ROOT / "_Aidge_Arm" / "templates" / "forward_call" / "forward.jinja")
    

class ExportLibCMSISNN(ExportLib):
    _name="export_cmsisnn"
    
