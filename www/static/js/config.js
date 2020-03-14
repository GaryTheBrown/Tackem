(function () {

    $(() => {
        new Config();
        createEvents();
    })

    function createEvents()
    {
        $('.modal').on('show.bs.modal', function (e) {
            $(this).find(":disabled").prop('disabled', false);
        });
    }

    class Config
    {
        constructor()
        {
            let obj = this;

            $("[data-show]").each(function(index, element){
                $(element).on('click', Config["show"]);
                if (obj.doICallTheClick(element)){
                    $(element).click();
                }
            }.bind(obj));

            $("[data-hide]").each(function(index, element){
                $(element).on('click', Config["hide"]);
                if (obj.doICallTheClick(element)){
                    $(element).click();
                }
            }.bind(obj));

            $("[data-action]").each(function(index, element){
                $(element).on('click', Config[$(element).data("action")]);
            });
        }

        doICallTheClick(element)
        {
            return $(element).is(':selected') || $(element).is(':checked')
        }

        static show()
        {
            $(this).data("show").split(",").forEach(function(entry) {
                $("#" + entry).show();
            });

        }
        static hide()
        {
            $(this).data("hide").split(",").forEach(function(entry) {
                $("#" + entry).hide();
            });
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
            let target = $(this).data("target")
            let $modalRoot = $(`#${target}_modal`);
            let $input = $modalRoot.find("input[type=text],select");
            let data = target.split("_");

            $input.prop("disabled", true)
            $elem.prop("disabled", true);
            $modalRoot.find("small").html("");

            $.ajax({
                type: 'POST',
                url: '/api/admin/addMulti/',
                data: {
                    plugin_name: data[2],
                    plugin_type: data[1],
                    instance: $input.val()
                },
                target: target,
                success: function(json)
                {
                    if (json.success) {
                        $(`#${target}_tab`).append(json.html);
                        $("[type=checkbox]").bootstrapToggle();
                        $("[value=Delete]").on("click", Config.deleteMulti);
                        $modalRoot.modal('hide');
                    } else {
                        $modalRoot.find("small").html(json.error);
                        $elem.prop("disabled", false);
                        $input.prop("disabled", false);
                    }
                }
            })
        }

        static deleteMulti()
        {
            let $elem = $(this);

            let plugin_type = $(this).data("plugin_type");
            let plugin_name = $(this).data("plugin_name");
            let instance = $(this).data("plugin_instance");

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
                        $elem.find("section").remove();
                    }
                }
            })
        }
    }

})();
