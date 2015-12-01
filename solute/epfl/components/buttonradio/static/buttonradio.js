epfl.ButtonRadio = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "input[type=radio][name=" + cid + "]";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];

    $(selector).change(function(){
        epfl.FormInputBase.on_change(compo, $(this).val(), cid, enqueue_event);
    });

};

epfl.ButtonRadio.inherits_from(epfl.ComponentBase);
