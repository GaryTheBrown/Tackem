$(function() {
    $(".pluginbutton").on("click", function(){
        action = $(this).data("action");
        plugin_type = $(this).data("plugin_type");
        plugin_name = $(this).data("plugin_name");
        url = action + "/" + plugin_type + "/" + plugin_name + "/";
        Call_API('GET', url);
    });
});


function Call_API(callType, url){
    $.ajax({
        type: callType,
        url: '%%BASEURL%%/api/%%WEBKEY%%/' + url,
        success: function(return_string) {
            data = JSON.parse(return_string);
        },
    });
}
