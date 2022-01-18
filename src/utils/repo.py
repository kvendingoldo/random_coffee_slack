# -*- coding: utf-8 -*-


def filtration(spec, objs):
    if spec:
        result = []
        for obj in objs:
            take = True
            for key in spec.keys():
                if key == "or":
                    for k_or in spec[key].keys():
                        take = False
                        if getattr(obj, k_or) == spec[key][k_or]:
                            take = True
                            break
                else:
                    if getattr(obj, key) != spec[key]:
                        take = False
                        break
            if take:
                result.append(obj)
        return result
    else:
        return objs


def get_unique_locations(users):
    m_locations = set()
    for user in users:
        m_locations.add(user.meet_loc)
    return list(m_locations)
