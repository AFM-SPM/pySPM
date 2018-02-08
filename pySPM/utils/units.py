import sys
import math

_SI_units = ['kg','m','s','A','K','cd','mol']

_units = {
    'V':{'kg':1,'m':2,'s':-3,'A':-1,'K':0,'cd':0,'mol':0},
    'N':{'kg':1,'m':1,'s':-2,'A':0,'K':0,'cd':0,'mol':0},
    'J':{'kg':1,'m':2,'s':-2,'A':0,'K':0,'cd':0,'mol':0},
    'W':{'kg':1,'m':2,'s':-3,'A':0,'K':0,'cd':0,'mol':0},
    'Pa':{'kg':1,'m':-1,'s':-2,'A':0,'K':0,'cd':0,'mol':0},
    }
    
_unit_scale = {
    'y':-24,'z':-21,'a':-18,'f':-15,'p':-12,'n':-9,'u':-6,'m':-3,'c':-2,'d':-1,
    'h':2,'k':3,'M':6,'G':9,'T':12,'P':15,'E':18,'Z':21,'Y':24,'':0}
    
    
class UnitMissmatch(Exception):
    pass

class InvalidUnit(Exception):
    pass
    
class SIunit:
    def __init__(self, value=1, **kargs):
        self.units = {u:0 for u in _SI_units}
        self.value = value
        for x in kargs:
            if x in _SI_units:
                self.units[x] += kargs[x]
            elif x in _units:
                self.units = {y: self.units[y]+kargs[x]*_units[x][y] for y in self.units}
            elif x[0] in _unit_scale and x[1:] in _SI_units:
                self.value *= 10**(_unit_scale[x[0]])
                self.units[x[1:]] += kargs[x]
            elif x[0] in _unit_scale and x[1:] in _units:
                self.value *= 10**(_unit_scale[x[0]])
                self.units = {y: self.units[y]+kargs[x]*_units[x][y] for y in self.units}
            elif x[-1] == 'g' and x[:-1] in _unit_scale:
                self.units['kg'] += kargs[x]
                self.value *= 10**(_unit_scale[x[:-1]]-3)
            else:
                raise InvalidUnit
                
    def __add__(self, B):
        for x in self.units:
            if self.units[x]!=B.units[x]:
                raise UnitMissmatch
        return SIunit(self.value+B.value,**self.units)
        
    def __sub__(self, B):
        for x in self.units:
            if self.units[x]!=B.units[x]:
                raise UnitMissmatch
        return SIunit(self.value-B.value,**self.units)
       
    def __mul__(self, B):
        return SIunit(self.value*B.value, **{x:self.units[x]+B.units[x] for x in self.units})
        
    def __pow__(self, N):
        return SIunit(self.value**N, **{x:self.units[x]*N for x in self.units})
    
    def get_unit(self):
        return '*'.join([(['{unit}','{unit}^{N}'][self.units[x]!=1]).format(unit=x,N=self.units[x]) for x in self.units if self.units[x]!=0])
        
    def __repr__(self):
        return '{value:.3e} ('.format(value=self.value)+self.get_unit()+')'
    
    def sqrt(self):
        return SIunit(self.value**.5,**{x:self.units[x]/2 for x in self.units})
    
    def log(self):
        for x in self.units:
            if self.units[x] !=0:
                raise InvalidUnit
        return SIunit(math.log(self.value))