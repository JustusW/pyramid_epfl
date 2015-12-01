from solute import epfl

epfl.epflutil.Discover()

for compo_cls in epfl.epflutil.Discover.discovered_components:
    module, cls = compo_cls.__module__, compo_cls.__name__
    if not module.startswith('solute.epfl.components'):
        continue

    full_cls = "solute.epfl.components." + cls
    with file('_autodoc/' + module + '.rst', "w") as f:
        f.write("""{cls}
{subline}

.. autoclass:: {module}.{cls}
    :members:
    :private-members:
    :special-members:
    :show-inheritance:

""".format(module=module, cls=cls, full_cls=full_cls, subline="=" * len(cls)))