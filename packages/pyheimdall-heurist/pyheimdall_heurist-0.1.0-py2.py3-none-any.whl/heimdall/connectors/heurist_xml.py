# -*- coding: utf-8 -*-
import heimdall as _h
from heimdall.decorators import get_database


@get_database('heurist:xml')
def getDatabase(**options):
    r"""Generates a dummy database.

    The generated datbase contains a single item, and this item contains and a single metadata.
    The generated metadata property identifier is ``message``, and its value is passed as a parameter (default: ``EXAMPLE``).

    :param \**options: Keyword arguments
    :param message: (:py:class:`str`) Text of the single item's metadata
    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`
    """  # nopep8: E501
    message = options.get('message', "TODO")
    tree = _h.util.tree.create_empty_tree()
    _h.createItem(tree, message=message)
    return tree


__version__ = '0.1.0'
__all__ = ['getDatabase', '__version__']
