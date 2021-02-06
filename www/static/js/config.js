(function () {

    $(() => {
        new Config();
        createEvents();
    });

    function createEvents()
    {
        $('.modal').on('show.bs.modal', function (e) {
            $(this).find(":disabled").prop('disabled', false);
        });

        $("form").submit(function () {

            let this_master = $(this);

            this_master.find('input[type="checkbox"]').each( function () {
                let checkbox_this = $(this);

                if( checkbox_this.is(":checked") == true ) {
                    checkbox_this.attr('value','1');
                } else {
                    checkbox_this.prop('checked',true);
                    checkbox_this.attr('value','0');
                }
            });
            return true;
        });
    }

    class Config
    {
        constructor()
        {
            let obj = this;

            $("[data-click-show]").each(function(index, element) {
                $(element).on('click', Config.show);
                if (obj.doICallTheClick(element)) {
                    $(element).click();
                }
            }.bind(obj));

            $("[data-click-hide]").each(function(index, element) {
                $(element).on('click', Config.hide);
                if (obj.doICallTheClick(element)) {
                    $(element).click();
                }
            }.bind(obj));

            $("[data-toggle-panel]").each(function(index, element) {
                $(element).on('change', Config.togglePanel);
                if (!obj.doICallTheClick(element)) {
                    $(element).click();
                }
            }.bind(obj));

            $("[data-click-action]").each(function(index, element) {
                $(element).on('click', Config[$(element).data("action")]);
            });
        }

        doICallTheClick(element)
        {
            return $(element).is(':selected') || $(element).is(':checked');
        }

        static show()
        {
            $(this).data("click-show").split(",").forEach(function(entry) {
                if (entry.endsWith("section") || entry.endsWith("panel")) {
                    $("#" + entry).show();
                } else {
                    $("#" + entry).closest(".item").show();
                }
            });

        }
        static hide()
        {
            $(this).data("click-hide").split(",").forEach(function(entry) {
                if (entry.endsWith("section") || entry.endsWith("panel")) {
                    $("#" + entry).hide();
                } else {
                    $("#" + entry).closest(".item").hide();
                }
            });
        }

        static togglePanel()
        {
            $(this).closest("section").find(".section").toggle();
        }

        static generateAPIKey()
        {
            let num = Math.random().toString(36).substring(2, 12);
            num += Math.random().toString(36).substring(2, 12);
            num += Math.random().toString(36).substring(2, 12);
            num += Math.random().toString(36).substring(2, 12);
            $('#' + $(this).data("input")).val(num);
        }

        static addMulti()
        {
            let $elem = $(this);
            let target = $(this).data("target");
            let $modalRoot = $(`#${target}_modal`);
            let $input = $modalRoot.find("input[type=text],select");
            let data = target.split("_");
            let plugin_name = data[2];
            let plugin_type = data[1];
            let instance = $input.val().toLowerCase();

            $input.prop("disabled", true);
            $elem.prop("disabled", true);
            $modalRoot.find("small").html("");

            $.ajax({
                type: 'POST',
                url: '/api/admin/addMulti/',
                data: {
                    plugin_type: plugin_type,
                    plugin_name: plugin_name,
                    instance: $input.val()
                },
                target: target,
                success: function(json)
                {
                    if (json.success) {
                        $(`#${target}_tab`).append(json.html);
                        let $panel = $(`#plugins_${plugin_type}_${plugin_name}_${instance}_panel`);
                        $panel.find("[type=checkbox]").bootstrapToggle();
                        $panel.find("[data-action=deleteMulti]").on("click", Config.deleteMulti);
                        $modalRoot.modal('hide');
                    } else {
                        $modalRoot.find("small").html(json.error);
                        $elem.prop("disabled", false);
                        $input.prop("disabled", false);
                    }
                }
            });
        }

        static deleteMulti()
        {
            let $elem = $(this);

            let plugin_type = $(this).data("plugin-type");
            let plugin_name = $(this).data("plugin-name");
            let instance = $(this).data("plugin-instance");

            $elem.prop("disabled", true);

            $.ajax({
                type: 'POST',
                url: '/api/admin/deleteMulti/',
                data: {
                    plugin_type: plugin_type,
                    plugin_name: plugin_name,
                    instance: instance
                },
                $elem: $elem,

                success: function(json)
                {
                    if (json.success) {
                        $(`#plugins_${plugin_type}_${plugin_name}_${instance}_panel`).remove();
                    }
                }
            });
        }
    }
})();
