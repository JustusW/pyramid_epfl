epfl.Checkbox = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    $(selector).attr('checked', $(selector).val() == 'True');
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    var change = function (event) {
        epfl.FormInputBase.on_change(compo, $(this).is(':checked'), cid, enqueue_event);
    };

    $(selector).blur(change).change(change);
};

epfl.Checkbox.inherits_from(epfl.ComponentBase);
