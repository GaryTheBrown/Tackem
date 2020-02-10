$(function () {

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

            $("[data-action]").each(function(){
                if ($(this).data("action") in Config){
                    $(this).on('click', Config[$(this).data("action")]);
                }
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
            });;

        }
        static hide()
        {
            $(this).data("hide").split(",").forEach(function(entry) {
                $("#" + entry).hide();
            });;
        }

        static generateAPIKey()
        {
            let num = Math.random().toString(36).substring(2, 12);
            num += Math.random().toString(36).substring(2, 12);
            num += Math.random().toString(36).substring(2, 12);
            num += Math.random().toString(36).substring(2, 12);
            $('#' + $(this).data("input")).val(num);
        }

    }

    let config = new Config();

});
