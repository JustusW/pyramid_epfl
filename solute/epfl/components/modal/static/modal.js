epfl.Modal = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);


    $('#'+cid+'_modal_save').click(function(){
        epfl.dispatch_event(cid, 'save', {});
    });
    $('#'+cid+'_modal_close').click(function(){
        epfl.dispatch_event(cid, 'close', {});
    });
    $('#'+cid).on('shown.bs.modal', function () {
    	$(this).find("input").first().focus();
	});
};
epfl.Modal.inherits_from(epfl.ComponentBase);