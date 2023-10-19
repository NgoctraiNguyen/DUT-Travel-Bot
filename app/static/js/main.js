$(document).ready(function(){
    $('#action_menu_btn').click(function(){
        $('.action_menu').toggle();
    });
});

$('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);