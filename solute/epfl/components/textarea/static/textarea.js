epfl.TextArea = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    var change = function (event) {
        epfl.FormInputBase.on_change(compo, $(selector).val(), cid, enqueue_event);
    };

    $(selector).blur(change).change(change);
};

epfl.TextArea.inherits_from(epfl.ComponentBase);
