$(document).ready(function() {
    $('#query').autoComplete({
        minLength: 2,
        bootstrapVersion: '4',
        noResultsText: "",
        resolverSettings: {
            fail: function() {},
            requestThrottling: 100
        }
    });

    $('#form-search').on('click', '.bootstrap-autocomplete a', function() {
        $('#form-search').submit();
    });

    $('#query').on('click', function() {
        $('#query').autoComplete('show');
    });

    $(window).resize(function(){
        // There is a bug with the plugin that messes up the drop down location 
        // when the window/page resizes. Work around it by resetting the location
        // when the window size changes
        pos = document.getElementById('query').getBoundingClientRect();
        autoCmpElem = document.getElementsByClassName('bootstrap-autocomplete')[0];
        if (autoCmpElem) {
            autoCmpElem.style.top = `${pos.bottom}px`;
            autoCmpElem.style.left = `${pos.left}px`;
            autoCmpElem.style.width = `${pos.width}`;
        }
    });
});



// function searchFunc(){
//     line = document.getElementById('query');
//     qanak = '100%';
//     line.style.width = qanak;
//     console.log('link 100%%%%');
// }
window.onload = function searchFunc(){
    line = document.getElementById('query');
    logo = document.getElementById('logo');

    line.style.width = '90%';
    line.style.border = '1px solid #f48024';

    logo.style.width = '300px'
    logo.style.transform = 'rotate(346deg)'
};