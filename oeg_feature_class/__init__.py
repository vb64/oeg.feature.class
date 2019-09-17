# coding: utf-8
"""
According http://www.iliassociation.org/documents/industry/POF%20specs%20V3_2%20January%202005.pdf
Газпром 2-2.3-919-2015
"""


class Error(Exception):
    """
    Feature Class exception
    """


class MagnetType:  # pylint: disable=too-few-public-methods,no-init
    """
    Magnet system types
    """
    MFL = 'MFL'  # lengthwise
    TFI = 'TFI'  # diametral
    CAL = 'CAL'  # caliper


class FeatureClass:  # pylint: disable=too-few-public-methods,no-init
    """
    class for given geometry parameters
    """
    AXGR = 'AXGR'  # Axial Grooving (продольная канавка)
    AXSL = 'AXSL'  # Axial Slotting (продольная щель)
    CIGR = 'CIGR'  # Circumferential Grooving (поперечная канавка)
    CISL = 'CISL'  # Circumferential Slotting (поперечная щель)
    GENE = 'GENE'  # General (обширный)
    PINH = 'PINH'  # Pinhole (язва)
    PITT = 'PITT'  # Pitting (каверна)


MIN_PERCENT = {  # пороги обнаружения в % от толщины стенки трубы

  MagnetType.MFL: {
    FeatureClass.GENE: 5,
    FeatureClass.PITT: 10,
    FeatureClass.PINH: 20,
    FeatureClass.AXGR: 20,
    FeatureClass.CIGR: 8,
    FeatureClass.CISL: 8,
  },

  MagnetType.TFI: {
    FeatureClass.GENE: 5,
    FeatureClass.PITT: 10,
    FeatureClass.PINH: 20,
    FeatureClass.CIGR: 20,
    FeatureClass.AXGR: 8,
    FeatureClass.AXSL: 8,
  },
}

LIMITS = {

  MagnetType.MFL: {

    FeatureClass.GENE: lambda thick, length, width, depth: (
      (length - 30, length + 30),  # точность по длине, мм -/+
      (width - 30, width + 30),  # точность по ширине, мм -/+
      (depth - 0.1 * thick, depth + 0.1 * thick),  # точность по глубине, мм -/+
    ),

    FeatureClass.PITT: lambda thick, length, width, depth: (
      (length - 20, length + 20),
      (width - 30, width + 30),
      (depth - 0.1 * thick, depth + 0.1 * thick),
    ),

    FeatureClass.PINH: lambda thick, length, width, depth: (
      (length - 15, length + 15),
      (width - (thick + 30), width + (thick + 30)),
      (depth - 0.2 * thick, depth + 0.2 * thick),
    ),

    FeatureClass.AXGR: lambda thick, length, width, depth: (
      (length - 20, length + 20),
      (width - 30, width + 30),
      (depth - 0.2 * thick, depth + 0.2 * thick),
    ),

    FeatureClass.CIGR: lambda thick, length, width, depth: (
      (length - 20, length + 20),
      (width - (thick + 30), width + (thick + 30)),
      (depth - 0.15 * thick, depth + 0.15 * thick),
    ),

    FeatureClass.CISL: lambda thick, length, width, depth: (
      (length - 20, length + 20),
      (width - (thick + 30), width + (thick + 30)),
      (depth - 0.15 * thick, depth + 0.15 * thick),
    ),

  },

  MagnetType.TFI: {

    FeatureClass.GENE: lambda thick, length, width, depth: (
      (length - 30, length + 30),
      (width - 30, width + 30),
      (depth - 0.1 * thick, depth + 0.1 * thick),
    ),

    FeatureClass.PITT: lambda thick, length, width, depth: (
      (length - 30, length + 30),
      (width - 20, width + 20),
      (depth - 0.1 * thick, depth + 0.1 * thick),
    ),

    FeatureClass.PINH: lambda thick, length, width, depth: (
      (length - (thick + 30), length + (thick + 30)),
      (width - 15, width + 15),
      (depth - 0.2 * thick, depth + 0.2 * thick),
    ),

    FeatureClass.CIGR: lambda thick, length, width, depth: (
      (length - 30, length + 30),
      (width - 20, width + 20),
      (depth - 0.2 * thick, depth + 0.2 * thick),
    ),

    FeatureClass.AXGR: lambda thick, length, width, depth: (
      (length - 30, length + 30),
      (width - 20, width + 20),
      (depth - 0.15 * thick, depth + 0.15 * thick),
    ),

    FeatureClass.AXSL: lambda thick, length, width, depth: (
      (length - 30, length + 30),
      (width - 20, width + 20),
      (depth - 0.15 * thick, depth + 0.15 * thick),
    ),

  },
}


def size_class(length, width, thick):
    """
    calculate feature class for given parameters
    """
    if not all([width, length, thick]):
        raise Error("Wrong FeatureClass params. l={} w={} t={}".format(length, width, thick))

    size1 = thick
    if size1 < 10:
        size1 = 10

    size3 = 3 * size1
    size6 = 6 * size1
    lwr = float(length) / float(width)

    if (width >= size3) and (length >= size3):
        ret = FeatureClass.GENE

    elif (
      (size6 > width >= size1) and
      (size6 > length >= size1) and
      (2.0 > lwr > 0.5)
    ) and not (width >= size3 <= length):
        ret = FeatureClass.PITT

    elif (size3 > width >= size1) and (lwr >= 2.0):
        ret = FeatureClass.AXGR

    elif (size3 > length >= size1) and (lwr <= 0.5):
        ret = FeatureClass.CIGR

    elif (size1 > width > 0) and (size1 > length > 0):
        ret = FeatureClass.PINH

    elif length >= size1 > width > 0:
        ret = FeatureClass.AXSL

    elif width >= size1 > length > 0:
        ret = FeatureClass.CISL

    else:
        raise Error("Wrong FeatureClass params. l={} w={} t={}".format(length, width, thick))

    return ret


def is_detectable(sizes, thick, magnet_type=MagnetType.MFL):
    """
    return True if defekt with given sizes on wallthick more than minimal percent
    """
    length, width, depth = sizes
    cls = size_class(length, width, thick)
    borders = MIN_PERCENT[magnet_type]
    if cls not in borders:
        return False

    if depth < 0:  # through hole
        depth = thick

    min_percent = borders[cls]
    percent = int(round(depth * 100.0 / thick, 0))

    return percent >= min_percent


def is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL):
    """
    return tuple from 3 boolean items, that represent limits by length, width, depth
    """
    limits = LIMITS[magnet_type]
    cls = size_class(real[0], real[1], thick)
    if cls not in limits:
        raise Error("Defect with params {} has class '{}'. Not applicable for method '{}'".format(
          real, cls, magnet_type
        ))

    length_ok, width_ok, depth_ok = False, False, False
    length, width, depth = calcked
    limits_length, limits_width, limits_depth = limits[cls](thick, *real)

    if limits_length[0] <= length <= limits_length[1]:
        length_ok = True

    if limits_width[0] <= width <= limits_width[1]:
        width_ok = True

    if limits_depth[0] <= depth <= limits_depth[1]:
        depth_ok = True

    return (length_ok, width_ok, depth_ok)
