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
            $section.find("[type=button]").prop('disabled', true);

            $.ajax({
                type: 'POST',
                url: '/api/admin/plugin/' + action,
                data: {
                    plugin_name: pluginName,
                    plugin_type:pluginType
                },
                section: $section,
                success: function(json)
                {
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

                    if(json.message){
                        alert(message);
                    }
                }
            })
        }
    }
})();
