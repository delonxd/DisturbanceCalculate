from src.Module.CircuitBasic import *
from src.ConstantType import *


# 电缆等效电路
class TPortCable(TPortCircuitPi):
    new_table = {
        '电阻': 'R',
        '电感': 'L',
        '电容': 'C',
        '电缆长度': 'length',
    }
    prop_table = TwoPortNetwork.prop_table.copy()
    prop_table.update(new_table)

    # 变量类型
    para_type = {
        'R': Constant,
        'L': Constant,
        'C': Constant,
        'length': Constant}

    def __init__(self, parent_ins, name_base, length, cab_r, cab_l, cab_c):
        TwoPortNetwork.__init__(self, parent_ins, name_base)
        self.R = cab_r
        self.L = cab_l
        self.C = cab_c
        self.length = length

    def get_coeffs(self, freq):
        length = float(self.length)
        w = 2 * np.pi * freq
        z0 = float(self.R) + 1j * w * float(self.L)
        y0 = 10e-10 + 1j * w * float(self.C)
        # y0 = 1j * w * float(self.C)
        zc = np.sqrt(z0 / y0)
        gama = np.sqrt(z0 * y0)
        zii = zc * np.sinh(gama * length)
        yii = (np.cosh(gama * length) - 1) / zc / np.sinh(gama * length)
        # yii = np.imag(yii) * 1j
        # rii = 1/yii
        # rii = np.imag(rii) * 1j
        # yii = 1/rii
        y1 = yii
        y2 = 1 / zii
        y3 = yii
        self.value2coeffs(y1, y2, y3)
        return self.equs
