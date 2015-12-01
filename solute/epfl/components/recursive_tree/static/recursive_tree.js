epfl.RecursiveTree = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var selector = '[epflid=' + cid + ']';

    var compo = this;

    var elm = $(selector);
    var label = $(selector + ' > span');
    var icon = $(selector + ' > i');

    var scrollTimeout = null;

    label.click(function () {
        epfl.send(compo.make_event('click_label'));
    });

    icon.click(function () {
        epfl.send(compo.make_event('click_icon'));
    });

    $(selector).scroll(function () {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function () {
            epfl.enqueue(compo.make_event('scroll', {scroll_pos: $(selector).scrollTop()}));
        }, 250);
    });

    if (params["scroll_position"] !== "None") {
        $(selector).scrollTop(params["scroll_position"]);
    }
};

epfl.RecursiveTree.inherits_from(epfl.ComponentBase);
