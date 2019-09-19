function DownloadPlugin(pluginName, full_system){
    $('#dim_screen').show();
    input = $("#" + pluginName + "_control");
    $("#" + pluginName + "_control > input").prop('disabled', true);
    $("button").prop("disabled", true);
    $.ajax({
        type: 'GET',
        url: '/download_plugin?name=' + pluginName,
        input: input,
        pluginName: pluginName,
        success: function(data) {
            this.input.html(data);
            alert(this.pluginName + " Downloaded");
            count = parseInt($("#plugin_count").val());
            count++;
            $("#plugin_count").val(count);
            if (count == 0){
                $("button").prop("disabled", false);
            }else{
                $("button").prop("disabled", true);
            }
            $('#dim_screen').hide();
        }
   });
}

function RemovePlugin(pluginName){
    $('#dim_screen').show();
    input = $("#" + pluginName + "_control");
    $.ajax({
        type: 'GET',
        url: '/remove_plugin?name=' + pluginName,
        input: input,
        pluginName: pluginName,
        success: function(data) {
            this.input.html(data);
            count = parseInt($("#plugin_count").val());
            count--;
            $("#plugin_count").val(count);
            if (count == 0){
                $("button").prop("disabled", false);
            }else{
                $("button").prop("disabled", true);
            }
            $('#dim_screen').hide();
        }
   });
}