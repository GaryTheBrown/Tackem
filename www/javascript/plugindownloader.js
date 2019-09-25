$(function() {
    $(".pluginbutton").on("click", function() {
        var elem = $(this);
        elem.prop('disabled', true);
        $("button").prop("disabled", true);
        pluginName = elem.data('plugin');

        switch(elem.val()){
            case "Add":
                downloadPlugin(elem, pluginName);
                break;
            case "Remove":
                removePlugin(elem, pluginName);
                break;
            // case "Reload":
            //     break;
            // case "Clear Config":
            // case "Clear Database":
            // case "Start":
            // case "Stop":
            default:
                alert(elem.val() + " Not Programed Yet")
                counter(0);
                break;
        }

    });
});

function downloadPlugin(elem, pluginName){
    $.ajax({
        type: 'GET',
        url: '/download_plugin?name=' + pluginName,
        elem: elem,
        pluginName: pluginName,
        success: function(data) {
            if (data != "true") {
                alert(data);
            } else {
                elem.val("Remove");
                alert(this.pluginName + " Downloaded");
                counter(+1);
                elem.prop('disabled', false);
            }
        }
    });
}

function removePlugin(elem, pluginName){
    $.ajax({
        type: 'GET',
        url: '/remove_plugin?name=' + pluginName,
        elem: elem,
        pluginName: pluginName,
        success: function(data) {
            elem.val("Add");
            alert(this.pluginName + " Removed");
            counter(-1);
            elem.prop('disabled', false);
        }
   });
}

function counter(value){
    count = parseInt($("#plugin_count").val());
    count += value;
    $("#plugin_count").val(count);
    if (count == 0){
        $("button").prop("disabled", true);
    }else{
        $("button").prop("disabled", false);
    }

}
