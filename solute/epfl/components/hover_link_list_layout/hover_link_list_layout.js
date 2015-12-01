{% for compo_obj in compo.components %}
$('[epflid={{ compo_obj.cid }}]').hover(function (e) {
    if (e.type == 'mouseleave') {
        $('#hover_element{{ compo_obj.cid }}').remove();
    } else if (e.type == 'mouseenter') {
        $('<div id="hover_element{{ compo_obj.cid }}">')
            .css('position', 'absolute')
            .css('top', e.pageY + 'px')
            .css('left', (e.pageX + 10) + 'px')
            .css('z-index', '100')
            .append('<img src="{{ compo_obj.src }}" class="img-thumbnail" />')
            .appendTo(document.body);
    }
})
    .click(function () {
        $('#hover_element{{ compo_obj.cid }}').remove();
    });
{% endfor %}
