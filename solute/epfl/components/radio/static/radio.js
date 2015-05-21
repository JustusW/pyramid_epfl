epfl.Radio = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "input[name=" + cid + "]";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];

    $(selector).change(function(){
        epfl.FormInputBase.prototype.on_change(compo, $(this).val(), cid, enqueue_event);
    });

};

epfl.Radio.inherits_from(epfl.ComponentBase);
