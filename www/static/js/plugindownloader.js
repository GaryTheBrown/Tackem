(function() {

    $(() => {
        new PluginDownloader();
    });

    class PluginDownloader
    {
        constructor()
        {
            $("[data-action]").on('click', this.getData);
        }

        getData()
        {
            let $elem = $(this);
            let $section = $elem.closest("section");
            let action = $elem.data("action");
            let pluginName = $section.data('pluginname');
            let pluginType = $section.data('plugintype');
            $elem.prop('disabled', true);

            $.ajax({
                type: 'POST',
                url: '/api/admin/plugin/' + action,
                data: {
                    plugin_name: pluginName,
                    plugin_type:pluginType
                },
                elem: $elem,
                section: $section,
                success: function(json)
                {
                    console.log(json);
                    if (json.actions) {
                        if (json.actions.enable){
                            json.actions.enable.forEach(function(item) {
                                let $prop = $section.find(`[data-action='${item}']`);
                                $prop.prop("disabled", false);
                            });
                        }
                        if (json.actions.disable){
                            json.actions.disable.forEach(function(item) {
                                let $prop = $section.find(`[data-action='${item}']`);
                                $prop.prop("disabled", true);
                            });
                        }
                    }
                    console.log(`${json.error_number}:${json.error}`);

                    if(json.message){
                        alert(message);
                    }
                }
            })
        }

    }
//     $(".pluginbutton").on("click", function() {
//         var elem = $(this);
//         elem.prop('disabled', true);
//         $("button").prop("disabled", true);
//         pluginName = elem.data('plugin');
//         action = elem.val().toLowerCase().replace(/\s/g, "");

//         $.ajax({
//             type: 'GET',
//             url: '/plugin_control?action=' + action + '&name=' + pluginName,
//             elem: elem,
//             action: action,
//             pluginName: pluginName,
//             success: function(return_string) {
//                 data = JSON.parse(return_string);
//                 switch(this.elem.val()){
//                     case "Add":
//                         if (data['success'] == true) {
//                             this.elem.val("Remove");
//                             this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', false);
//                             this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', false);
//                             alert(this.pluginName + " Downloaded");
//                         } else {
//                             alert(data["message"]);
//                             if (data['code']){
//                                 this.elem.val("Remove");
//                                 this.elem.parent().parent().find("input[value='Reload']").show();
//                                 break;
//                             }
//                         }
//                         this.elem.prop('disabled', false);
//                         break;
//                     case "Remove":
//                         if (data['success'] == true) {
//                             this.elem.val("Add");
//                             this.elem.parent().parent().find("input[value='Reload']").hide();
//                             this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', true);
//                             this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', true);
//                             alert(this.pluginName + " Removed");
//                         } else {
//                             alert(data["message"]);
//                         }
//                         this.elem.prop('disabled', false);
//                         break;
//                     case "Reload":
//                         if (data['success'] == true) {
//                             this.elem.hide();
//                             alert(this.pluginName + " Reloaded");
//                         } else {
//                             alert(data["message"]);
//                         }
//                         this.elem.prop('disabled', false);
//                         break;
//                     case "Clear Config":
//                         if (data['success'] == true) {
//                             this.elem.prop("disabled", true);
//                             alert(this.pluginName + " Config Cleared");
//                         } else {
//                             alert(data["message"]);
//                         }
//                         break;
//                     case "Clear Database":
//                         if (data['success'] == true) {
//                             this.elem.prop("disabled", true);
//                             alert(this.pluginName + " Database Cleared");
//                         } else {
//                             alert(data["message"]);
//                         }
//                         break;
//                     case "Start":
//                         if (data['success'] == true) {
//                             this.elem.val("Stop");
//                             alert(this.pluginName + " Started");
//                             this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', true);
//                             this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', true);
//                         } else {
//                             alert(data["message"]);
//                         }
//                         this.elem.prop('disabled', false);
//                         break;
//                     case "Stop":
//                         if (data['success'] == true) {
//                             this.elem.val("Start");
//                             alert(this.pluginName + " Stopped");
//                             this.elem.parent().parent().find("input[value='Clear Config']").prop('disabled', false);
//                             this.elem.parent().parent().find("input[value='Clear Database']").prop('disabled', false);
//                         } else {
//                             alert(data["message"]);
//                         }
//                         this.elem.prop('disabled', false);
//                         break;
//                     default:
//                         alert(this.elem.val() + " Not Programed Yet")
//                         this.elem.prop('disabled', false);
//                         break;
//                 }
//             },
//         });
//     });
})();
