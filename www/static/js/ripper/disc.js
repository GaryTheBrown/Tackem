(function () {

    $(() => {
        new DiscType();
        createEvents();
    });

    function createEvents()
    {

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

    class DiscType
    {
        constructor()
        {
            let obj = this;
            $("[data-click-action]").each(function(index, element) {
                $(element).on('click', DiscType[$(element).data("click-action")]);
            });
        }

        static chooseDiscType()
        {
            let discType = $(this).data("disc-type");

            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/disc/blank/${discType}`,
                dataType: 'json',
                success: function (result) {
                    let $section = $("#disctypesection");
                    if (result.disc_html) {
                        $section.html(result.disc_html);
                        $section.find("[data-click-action]").each(function(index, element) {
                            $(element).on('click', DiscType[$(element).data("click-action")]);
                        });
                    }
                },
            });
        }

        static reselectDisc()
        {
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/disc/disctypeselect`,
                dataType: 'json',
                success: function (result) {
                    let $section = $("#disctypesection");
                    if (result.disc_html) {
                        $section.html(result.disc_html);
                        $section.find("[data-click-action]").each(function(index, element) {
                            $(element).on('click', DiscType[$(element).data("click-action")]);
                        });
                    }
                    $(".trackripdata").each(function(index, element) {
                        element.html("");
                    });

                },
            });
        }

        static movieSearch()
        {

        }

        static movieSearchIMDBid()
        {

        }

        static movieSearchTMDBid()
        {

        }

        static tvSearch()
        {

        }

        static tvSearchTVDBid()
        {

        }

        static tvSearchTMDBid()
        {

        }

        static docSearch()
        {

        }

        static docSearchIMDBid()
        {

        }

        static docSearchTVDBid()
        {

        }

        static docSearchTMDBid()
        {

        }

    }
})();
