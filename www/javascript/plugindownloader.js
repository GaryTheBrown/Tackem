$(function() {
    $(".pluginbutton").on("click", function() {
        var elem = $(this);
        elem.prop('disabled', true);
        $("button").prop("disabled", true);
        pluginName = elem.data('plugin');
        action = elem.val();

        $.ajax({
            type: 'GET',
            url: '/plugin_control?action=' + action + '&name=' + pluginName,
            elem: elem,
            action: action,
            pluginName: pluginName,
            success: function(return_string) {
                data = JSON.parse(return_string);
                switch(this.elem.val()){
                    case "Add":
                        if (data['success'] == true) {
                            this.elem.val("Remove");
                            this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', false);
                            this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', false);
                            alert(this.pluginName + " Downloaded");
                            counter(+1);
                        } else {
                            alert(data["message"]);
                            if (data['code']){
                                this.elem.val("Remove");
                                this.elem.parent().parent().find("input[value='Reload']").show();
                                break;
                            }
                        }
                        this.elem.prop('disabled', false);
                        break;
                    case "Remove":
                        if (data['success'] == true) {
                            this.elem.val("Add");
                            this.elem.parent().parent().find("input[value='Reload']").hide();
                            this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', true);
                            this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', true);
                            alert(this.pluginName + " Removed");
                            counter(-1);
                        } else {
                            alert(data["message"]);
                        }
                        this.elem.prop('disabled', false);
                        break;
                    case "Reload":
                        if (data['success'] == true) {
                            this.elem.hide();
                            counter(+1);
                            alert(this.pluginName + " Reloaded");
                        } else {
                            alert(data["message"]);
                        }
                        this.elem.prop('disabled', false);
                        break;
                    case "Clear Config":
                        if (data['success'] == true) {
                            this.elem.prop("disabled", true);
                            counter(+1);
                            alert(this.pluginName + " Config Cleared");
                        } else {
                            alert(data["message"]);
                        }
                        break;
                    case "Clear Database":
                        if (data['success'] == true) {
                            this.elem.prop("disabled", true);
                            counter(+1);
                            alert(this.pluginName + " Database Cleared");
                        } else {
                            alert(data["message"]);
                        }
                        break;
                    case "Start":
                        if (data['success'] == true) {
                            this.elem.val("Stop");
                            alert(this.pluginName + " Started");
                            this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', true);
                            this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', true);
                        } else {
                            alert(data["message"]);
                        }
                        this.elem.prop('disabled', false);
                        break;
                    case "Stop":
                        if (data['success'] == true) {
                            this.elem.val("Start");
                            alert(this.pluginName + " Stopped");
                            this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', false);
                            this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', false);
                        } else {
                            alert(data["message"]);
                        }
                        this.elem.prop('disabled', false);
                        break;
                    default:
                        alert(this.elem.val() + " Not Programed Yet")
                        this.elem.prop('disabled', false);
                        break;
                }
                counter(0)
            },
        });
    });
});

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
