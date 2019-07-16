'''
Created on 17 sept. 2016

@author: kengne
'''

class TimeSeries(list):
    
    def __init__(self, name, start, end, step, values, consolidate='average'):
        list.__init__(self, values)
        self.name = name
        self.start = start
        self.end = end
        self.step = step
        self.consolidationFunc = consolidate
        self.valuesPerPoint = 1
        self.options = {}


    def __eq__(self, other):
        
        if isinstance(other, TimeSeries):
            color_check = True
            if hasattr(self, 'color'):
                if hasattr(other, 'color'):
                    color_check = (self.color == other.color)
                else:
                    color_check = False
            elif hasattr(other, 'color'):
                color_check = False
    
            return ((self.name, self.start, self.end, self.step, self.consolidationFunc, self.valuesPerPoint, self.options) ==(other.name, other.start, other.end, other.step, other.consolidationFunc, other.valuesPerPoint, other.options)) and list.__eq__(self, other) and color_check
        return False


    def __iter__(self):
        if self.valuesPerPoint > 1:
            return self.__consolidatingGenerator( list.__iter__(self) )
        else:
            return list.__iter__(self)


    def consolidate(self, valuesPerPoint):
        self.valuesPerPoint = int(valuesPerPoint)


    def __consolidatingGenerator(self, gen):
        buf = []
        for x in gen:
            buf.append(x)
            if len(buf) == self.valuesPerPoint:
                while None in buf: buf.remove(None)
                if buf:
                    yield self.__consolidate(buf)
                    buf = []
                else:
                    yield None
        while None in buf: buf.remove(None)
        if buf: yield self.__consolidate(buf)
        else: yield None
        raise StopIteration


    def __consolidate(self, values):
        usable = [v for v in values if v is not None]
        if not usable: return None
        if self.consolidationFunc == 'sum':
            return sum(usable)
        if self.consolidationFunc == 'average':
            return float(sum(usable)) / len(usable)
        if self.consolidationFunc == 'max':
            return max(usable)
        if self.consolidationFunc == 'min':
            return min(usable)
        raise Exception("Invalid consolidation function: '%s'" % self.consolidationFunc)


    def __repr__(self):
        return 'TimeSeries(name=%s, start=%s, end=%s, step=%s)' % (self.name, self.start, self.end, self.step)


    def getInfo(self):
        """Pickle-friendly representation of the series"""
        return {
          'name' : self.name,
          'start' : self.start,
          'end' : self.end,
          'step' : self.step,
          'values' : list(self),
        }
        