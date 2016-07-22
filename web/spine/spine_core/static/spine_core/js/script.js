$(function() {

    // Make panels that have content automatically collapsible.
    // Also add little expand/collapse control widgets to them.

    $('.panel-heading').each(function() {
        if($(this).siblings().size()) {
            $(this).prepend('<i class="fa fa-minus-square"></i>');
        }
    });

    $('.panel-heading i.fa').on('click', function() {
        $(this).parent().nextAll().toggle();
        $(this).toggleClass("fa-minus-square fa-plus-square");
    });

    // Make textarea boxes auto-resize to fit their content.
    // Also account for the browser window being resized.

    function textarea_update(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight+2) + 'px';
    }

    $('textarea').each(function() {
        this.style.resize = 'none';
        this.style.overflowX = 'hidden';
        this.style.overflowY = 'hidden';
        textarea_update(this);
    }).on('input', function() {
        textarea_update(this);
    });

    $(window).on('resize', function(){
        $('textarea').each(function() {
            textarea_update(this);
        });
    });

    // This is the process for deleting an existing comment.
    // Provide a modal dialog box to confirm the deletion.

    $('.confirm_comment_delete').click(function(event) {
        event.preventDefault();
        var answer = confirm('Are you sure you want to delete this comment?');
        if (answer) {
            $.post(location.pathname, {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').attr('value'),
                delete_comment: $(this).attr('data-id')
            }).always(function() {
                location.reload(true);
            });
        }
    });

});