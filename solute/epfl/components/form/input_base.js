$(function () {
	 epfl.init_component("{{ compo.cid }}"
                      , "FormInputBase",
                      { "submit_form_on_enter": {{ compo.submit_form_on_enter|format_bool }},
                      	"input_focus": {{ compo.input_focus|format_bool }},
                      	"fire_change_immediately": {{ compo.fire_change_immediately|format_bool }},
                        "label_style": "{{compo.label_style }}",
                        "input_style": "{{compo.input_style }}",
});
});
