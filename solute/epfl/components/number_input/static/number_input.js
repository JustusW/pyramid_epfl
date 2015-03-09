epfl.NumberInput = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var selector = "#" + cid + "_input";
    var compo = this;
    compo.strg = false;
    var enqueue_event = !params["fire_change_immediately"];
    var validation_type = $(selector).data('validation-type');
    var allowed_keys = [46, 8, 9, 27, 13, 110, 35, 36, 37, 38, 39, 40, 189];
    if(validation_type === "float"){
        allowed_keys.push(190);
    }

    var change = function (event) {
        epfl.FormInputBase.on_change(compo, $(selector).val(), cid, enqueue_event);
    };

    $(selector).keydown(function (event) {
        if (event.keyCode === 17) {
            compo.strg = true
        }
        if ((event.keyCode < 48 || event.keyCode > 57) &&
            allowed_keys.indexOf(event.keyCode) === -1) {
            if (compo.strg && [65, 67, 86, 88].indexOf(event.keyCode) !== -1) {
            } else {
                event.preventDefault();
                return;
            }
        }
    }).keyup(function (event) {
        if (event.keyCode === 17) {
            compo.strg = false;
        }
    }).blur(change).change(change);
};

epfl.NumberInput.inherits_from(epfl.ComponentBase);
