$(document).ready(function() {
    $('.btn-primary').hover(
        function(){
            $(this).css('background-color', 'white');
        },
        function(){
            $(this).css('background-color', '');
        }
    );
});