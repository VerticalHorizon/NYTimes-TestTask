from collections.abc import MutableMapping


def flatten(d: MutableMapping, sep: str = ".", parent_key: str = "") -> dict:
    """
    Transforms dict to flatten structure by join all dict keys with ``sep`` until MutableMapping occurs.

    Source dict:

    .. code-block:: python

        {
            "headline":{
               "main":"On EU Tube (LOL!), Sex Sells (Duh!)",
               "kicker":"None",
               "content_kicker":"None",
               "print_headline":"On EU Tube (LOL!), Sex Sells (Duh!)",
               "name":"None",
               "seo":"None",
               "sub":"None"
        },

    Result dict:

    .. code-block:: python

        {
            "headline.main":"On EU Tube (LOL!), Sex Sells (Duh!)",
            "headline.kicker":"None",
            "headline.content_kicker":"None",
            "headline.print_headline":"On EU Tube (LOL!), Sex Sells (Duh!)",
            "headline.name":"None",
            "headline.seo":"None",
            "headline.sub":"None",
        }

    .. warning::
       You shoudn't use ''parent_key''. It's only for recursion purposes.

    :param d: Nested dictionary.
    :type d: dict.
    :param sep: Parent keys separator.
    :type sep: str.
    :param parent_key: You shoudn't use this. Only for recursion purposes.
    :type parent_key: str.
    :returns: dict. Flattened dict.

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, sep=sep, parent_key=new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)
