# -*- coding: utf-8 -*-

def filtration(spec, objs):
    if spec:
        result = []
        for obj in objs:
            take = True
            for key in spec.keys():
                if getattr(obj, key) != spec[key]:
                    take = False
                    break
            if take:
                result.append(obj)
        return result
    else:
        return objs
