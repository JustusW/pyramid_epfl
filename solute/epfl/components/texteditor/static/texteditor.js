epfl.TextEditor = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
	var compo = this;
    var selector = "#" + cid + "_texteditor";
    var ed_config = params["editor_config_file"] + '.js';
    var clean_paste = params["clean_paste"];
    clean_paste = (clean_paste === "True") ? true : false;

    var editor = CKEDITOR.replace(cid + "_texteditor", {
    	customConfig: ed_config,
    	forcePasteAsPlainText: clean_paste
    });
    editor.on('change', function (evt) {
        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value:  evt.editor.getData()}), cid + "_change");
    });
}; 
epfl.TextEditor.inherits_from(epfl.ComponentBase);

