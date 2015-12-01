.. _rendering:

Rendering an EPFL Page
======================

.. graphviz::

    digraph overview {
        "Page" -> "ComponentBase.render()";
        "ComponentBase.render()" -> "Page";
        "ComponentBase.render()" -> "Template.render()";
        "Template.render()" -> "ComponentBase.render()";

        "get_render_environment()" -> "ComponentRenderEnvironment";
        "ComponentRenderEnvironment" -> "CallWrap";
        "CallWrap" -> "Template.render()";
        "Template.render()" -> "CallWrap";
        "CallWrap" -> "ComponentRenderEnvironment";
        "ComponentRenderEnvironment" -> "ComponentBase.render()";


        subgraph clusterPage {
            style = dotted;
            labeljust = l;
            label = "epflpage";
            "Page";
        }

        subgraph clusterComponentBase {
            style = dotted;
            labeljust = l;
            label = "epflcomponentbase";
            "ComponentBase.render()";
            "ComponentBase.render()" -> "get_render_environment()";
        }

        subgraph clusterComponentRenderEnvironment {
            style = dotted;
            labeljust = l;
            label = "ComponentRenderEnvironment";
            "ComponentRenderEnvironment";
            "CallWrap"
        }

        subgraph clusterJinja2Template {
            style = dotted;
            labeljust = l;
            label = "jinja2";
            "Template.render()";
        }
    }
