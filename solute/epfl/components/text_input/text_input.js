epfl.init_component("{{compo.cid}}",
                    "TextInput", {"fire_change_immediately": {{ compo.fire_change_immediately|format_bool }},
                                  "submit_form_on_enter": {{ compo.submit_form_on_enter|format_bool }},
                                  "typeahead": {{ compo.typeahead|format_bool }},
                                  "date": {{ compo.date|format_bool }},
                                  {% if compo.type_func %}
                                      "type_func": {{ compo.type_func|tojson }},
                                  {% endif %}
                                  {% if compo.max_length is not none %}
                                    "max_length": {{ compo.max_length|int }},
                                  {% endif %}
                                  "show_count": {{ compo.show_count|format_bool }}});
