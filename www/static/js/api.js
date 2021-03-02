function Call_API(callType, url){
    $.ajax({
        type: callType,
        url: ROOT + 'api/%%WEBKEY%%/' + url,
        success: function(return_string) {
            data = JSON.parse(return_string);
        },
    });
}
