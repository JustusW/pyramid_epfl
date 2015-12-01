epfl.Toggle = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    $(selector).attr('checked', $(selector).val() == 'True');
    $(selector).bootstrapSwitch('state');
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];

    $(selector).on('switchChange.bootstrapSwitch', function (event, state) {
        var val = $(this).closest("div").parent().hasClass("bootstrap-switch-on");
        epfl.FormInputBase.on_change(compo, val, cid, enqueue_event);
    });
};

epfl.Toggle.inherits_from(epfl.ComponentBase);
