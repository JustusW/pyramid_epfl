epfl.Popover = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $('#'+cid+"_popover").popover();
    $('#'+cid+"_popover").on("remove", function () {
        $('#'+cid+"_popover").popover('destroy');
    })
};

epfl.Popover.inherits_from(epfl.ComponentBase);


